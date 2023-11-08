# GPTAssistantManager

## Overview
GPTAssistantManager is a Python application designed to interface with OpenAI's GPT models. It facilitates the management of assistant workflows, including creating assistants, managing conversation threads, and handling responses asynchronously.

## Features
- Initialization of assistant workflows with custom configuration
- Creation and management of conversation threads
- Asynchronous handling of assistant responses
- Dedicated logging for monitoring activities

## Prerequisites
- Python 3.6+
- openai API library
- asyncio for asynchronous tasks
- Environment variables set for OpenAI API key

## Setup
Ensure that you have Python installed on your system and the necessary environment variables configured. Install the required packages by running:

```sh
pip install openai
```

## Usage
The GPTAssistantManager can be used by importing the class and creating an instance. Here's a quick example to get started:

```python
from classes.GPTAssistantManager import GPTAssistantManager
import asyncio

# Initialize the manager
assistant_manager = GPTAssistantManager()

# Start the assistant workflow
assistant_manager.initialize_assistant_workflow(
    assistant_name='YourAssistantName',
    assistant_instructions='YourInstructions'
)

# Run the assistant
response = asyncio.run(assistant_manager.demo_workflow())
print(response)
```

## Configuration
Settings and configurations are managed by the `config.py` module.

### Configuration Module (`config.py`)
The `config.py` module is responsible for loading configuration parameters from both environment variables and YAML files.

#### Features
- Loads environment variables from `.env` files for secure access to sensitive information such as API keys.
- Parses configuration settings from YAML files to easily manage application settings.

#### Usage
To use the configuration module:

```python
from my_modules import config

# Load environment variables
config.load_env()

# Load YAML configuration
yaml_data = config.load_yaml()
```

## Logging
Application logging is handled by the `my_logging.py` module.

### Logging Module (`my_logging.py`)
The `my_logging.py` module provides a configurable logger for the application, allowing for consistent logging across all components of the system.

#### Features
- Configurable log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- Log output to both file and console
- Customizable log formatting
- Automatic log directory creation

#### Usage
To initialize the logger:

```python
from my_modules.my_logging import my_logger

# Set up logging
logger = my_logger(
    dirname='log',
    logger_name='your_logger_name',
    debug_level='DEBUG',
    mode='a',
    stream_logs=True
)
```

#### Configuration
- `dirname`: The directory where log files will be stored.
- `logger_name`: A unique name for the logger instance. If not specified, it defaults to the module name.
- `debug_level`: The log level to capture. Can be `DEBUG`, `INFO`, `WARNING`, or `ERROR`.
- `mode`: The file mode, `w` for overwrite and `a` for append.
- `stream_logs`: If `True`, logs will also be printed to the console.
- `encoding`: The encoding for the log file, defaults to `UTF-8`.

#### Customization
You can customize the log format by modifying the formatter in the `my_logger` function:

```python
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

#### Tips
- Always specify a `logger_name` when initializing `my_logger` to avoid conflicts between different logging instances.
- Adjust the `debug_level` according to the verbosity you need for different environments, such as development or production.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Acknowledgments
- Hat tip to anyone whose code was used
- Inspiration
- etc
