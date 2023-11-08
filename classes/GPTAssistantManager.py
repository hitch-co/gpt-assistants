import openai
import os 

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
        
        #Create client
        gpt_client = openai.OpenAI()       
        self.gpt_client = gpt_client
        return gpt_client

    def create_gpt_assistant(self, 
                             assistant_name, 
                             assistant_instructions,
                             assistant_type="code_interpreter",
                             assistant_model="gpt-4-1106-preview"
                             ):
        assistant = self.gpt_client.beta.assistants.create(
            name=assistant_name,
            instructions=assistant_instructions,
            tools=[{"type": assistant_type}],
            model=assistant_model
        )
        self.assistant = assistant
        return assistant
    
    #A Thread represents a conversation. We recommend creating one Thread per user as soon as the user initiates the 
    # conversation. Pass any user-specific context and files in this thread by creating Messages.
    def create_gpt_thread(self):
        thread = self.gpt_client.beta.threads.create()
        self.thread = thread
        return thread
    
    def add_message_to_gpt_thread(self, 
                                  message_content:str = "I need to solve the equation `3x + 11 = 14`. Can you help me?"
                                  ):
        message = self.gpt_client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message_content
            )
        self.message = message
        return message
    
    def run_gpt_assistant(self,
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
    def check_gpt_assistant_response_status(self):
        gpt_response_status = self.gpt_client.beta.threads.runs.retrieve(
            thread_id=self.thread.id,
            run_id=self.run.id
            )
        print(type(gpt_response_status))
        self.gpt_response_status = gpt_response_status
        return gpt_response_status

    def get_gpt_asisstant_response(self):
        gpt_response = self.gpt_client.beta.threads.messages.list(
            thread_id=self.thread.id
            )
        self.gpt_response = gpt_response
        return gpt_response

if __name__ == "__main__":
    assistant_manager = GPTAssistantManager()

    ############################################################################
    #Below is a workflow that will likely run once per instance of
    # GPTAssistantManager().  This creates the client, creates the assistant,
    # and finally creates an empty thread

    #create client
    gpt_client = assistant_manager.create_gpt_client()

    #Create assistnat
    assistant_manager.create_gpt_assistant(
        assistant_name='assistant1', 
        assistant_instructions="You're an assistant that tells jokes",
        assistant_type="code_interpreter",
        assistant_model="gpt-4-1106-preview"
        )
    
    #Creatre GPT thread
    gpt_thread = assistant_manager.create_gpt_thread()

    ############################################################################
    #Everything below will be done in a workflow to continuously add messages to
    # the thread and change system messages as necessary to chnage the output

    #Add message
    gpt_thread_message = assistant_manager.add_message_to_gpt_thread(
        message_content="what's a good one about fridges"
        )
    
    #Run assistant
    gpt_assistant_run = assistant_manager.run_gpt_assistant(
        assistant_instructions = 'Please address the user as Prime'
        )
    
    #Check GPT Response
    gpt_assistant_response_status = assistant_manager.check_gpt_assistant_response_status()
    print(gpt_assistant_response_status)
    print(gpt_assistant_response_status.status)

    #Get response
    gpt_assistant_response = assistant_manager.get_gpt_asisstant_response()