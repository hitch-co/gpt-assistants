import openai
import os 
import asyncio

from my_modules import config
from my_modules.my_logging import my_logger

root_logger = my_logger(dirname='log', 
                        logger_level='INFO',
                        logger_name='root_GPTAssistantManager',
                        stream_logs=False
                        )

class GPTAssistantManager:
    def __init__(self) -> None:
        """
        Initializes the GPTAssistantManager instance.
        
        The instance uses a dedicated logger and loads configuration from environment variables
        and a YAML file. It sets up the assistant type and model based on the YAML configuration 
        by default, but these can be overridden during the assistant workflow initialization.
        """
        self.logger = my_logger(
            debug_level='INFO', 
            logger_name='logger_GPTAssistantManager', 
            mode='w', 
            stream_logs=True
            )
        
        self.lock = asyncio.Lock() # Lock for async operations

        config.load_env() # Load environment variables
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        self.yaml_data = config.load_yaml() # Load assistant configuration from a YAML file
        self.assistant_type=self.yaml_data['openai-api']['assistant_type']
        self.assistant_model=self.yaml_data['openai-api']['assistant_model']
        
    def _create_gpt_client(self):
        #Create client
        gpt_client = openai.OpenAI()       
        self.gpt_client = gpt_client
        return gpt_client

    def _create_gpt_assistant(self, 
                             assistant_name, 
                             assistant_instructions,
                             assistant_type=None,
                             assistant_model=None
                             ):
            
        # Check if args provided and if not, fall back to instance defaults
        if assistant_type is None:
            assistant_type = self.assistant_type
        if assistant_model is None:
            assistant_model = self.assistant_model

        assistant = self.gpt_client.beta.assistants.create(
            name=assistant_name,
            instructions=assistant_instructions,
            tools=[{"type": self.assistant_type}],
            model=self.assistant_model
        )
        self.assistant = assistant
        return assistant
    
    #A Thread represents a conversation. We recommend creating one Thread per user as soon as the user initiates the 
    # conversation. Pass any user-specific context and files in this thread by creating Messages.
    def _create_gpt_thread(self):
        thread = self.gpt_client.beta.threads.create()
        self.thread = thread
        return thread
    
    def _run_gpt_assistant(self,
                          assistant_instructions = 'Please address the user as Jane Doe. The user has a premium account.'
                          ):
        run = self.gpt_client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=assistant_instructions
            )
        self.run = run
        return run
    
    #This creates a Run in a queued status. You can periodically retrieve the Run to check on its status to see if it 
    # has moved to completed.
    async def _get_gpt_assistant_response(self, polling_seconds=1):
        async with self.lock:
            while True:
                gpt_assistant_response = self.gpt_client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=self.run.id
                    )

                self.gpt_assistant_response = gpt_assistant_response
                status = gpt_assistant_response.status
                self.logger.info(status)

                if status == 'completed':
                    return gpt_assistant_response
                else:
                    await asyncio.sleep(polling_seconds)

    async def _get_gpt_assistant_messages_list(self):
        gpt_response = self.gpt_client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        self.gpt_response = gpt_response
        return gpt_response

    def initialize_assistant_workflow(self, 
                                      assistant_name, 
                                      assistant_instructions, 
                                      assistant_type=None, 
                                      assistant_model=None):
        self._create_gpt_client()
        self._create_gpt_assistant(
            assistant_name=assistant_name, 
            assistant_instructions=assistant_instructions,
            assistant_type=assistant_type,
            assistant_model=assistant_model
            )
        self._create_gpt_thread()
    
    def add_message_to_gpt_thread(self, 
                                  message_content:str="Let the user know they should set the message_content variable",
                                  role:str='user'
                                  ):
        message_object = self.gpt_client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=message_content
            )
        self.message_object = message_object

        self.logger.debug(f"message_object (type: {type(message_object)})")
        self.logger.debug(message_object)
        return message_object
    
    async def get_assistant_response_thread_messages(self, assistant_instructions):
        self._run_gpt_assistant(assistant_instructions)
        
        # Await the response from the assistant
        await self._get_gpt_assistant_response()
        
        # Retrieve and return the message list, which should include the assistant's response
        response_thread_messages = await self._get_gpt_assistant_messages_list()

        self.logger.info(f"gpt_assistant_messages (type: {type(response_thread_messages)})")
        self.logger.info(response_thread_messages)
        return response_thread_messages
    
    def extract_latest_response_from_thread_message(self, response_thread_messages):
        # Sort the messages by 'created_at' in descending order
        sorted_response_thread_messages = sorted(response_thread_messages.data, key=lambda msg: msg.created_at, reverse=True)

        # Find the most recent message with role 'assistant'
        for message in sorted_response_thread_messages:
            if message.role == 'assistant':
                for content in message.content:
                    if content.type == 'text':
                        return content.text.value
        return None

async def demo_workflow():
    """
    A simple demonstration of the GPTAssistantManager class functionality.
    This async function initializes the assistant workflow, adds a message to the GPT thread, and processes the thread.

    Workflow:
    1. Initialize the assistant workflow using configuration defaults or provided arguments.
    2. Add a user message to the GPT thread.
    3. Process the thread to get the assistant's response.
    """
    assistant_manager = GPTAssistantManager()

    # Initialize workflow
    assistant_manager.initialize_assistant_workflow(
        assistant_name='assistant1',
        assistant_instructions="You're an assistant that tells jokes"
    )

    # Add FIRST message to instance thread
    assistant_manager.add_message_to_gpt_thread(
        message_content="what's a good one about fridges"
        )
    
    # process the thread
    response_thread_messages = await assistant_manager.get_assistant_response_thread_messages(
        assistant_instructions='Please address the user as Optimus'
    )
    #print(f"LENGTH: {len(response_thread_messages)}")
    response_text = assistant_manager.extract_latest_response_from_thread_message(response_thread_messages)

    # Add SECOND message to instance thread
    assistant_manager.add_message_to_gpt_thread(
        message_content="what's a good one about fridges"
        )
    
    # re-process to get the new  the thread to include a response for the added message
    response_thread_messages = await assistant_manager.get_assistant_response_thread_messages(
        assistant_instructions='Please address the user as Optimus'
    )
    response_text = assistant_manager.extract_latest_response_from_thread_message(response_thread_messages)
    
    return response_text

if __name__ == "__main__":
    response_text = asyncio.run(demo_workflow())
    print(f"THIS IS THE FINAL response_text: {response_text}")