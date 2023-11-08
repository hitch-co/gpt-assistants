import os
from my_modules.my_logging import my_logger

# Set up logging
logger = my_logger(dirname='log', 
                   logger_name='logger_yaml_env', 
                   debug_level='DEBUG', 
                   mode='a',
                   stream_logs=False)

#Load parameters from config.yaml
def load_yaml(yaml_filename='config.yaml', yaml_dirname='config', is_testing=False):

    """
    Load parameters from a YAML file.

    Parameters:
    - yaml_filename (str): Name of the YAML file to be loaded.
    - yaml_dirname (str): Directory path containing the YAML file.
    - is_testing (bool): Flag to indicate if the function is being run for testing purposes.

    Returns:
    dict: Dictionary containing parameters loaded from the YAML file.
    """
    import yaml
    import os

    # use the argument instead of hardcoding the path
    yaml_filepath = os.path.join(os.getcwd(), yaml_dirname, yaml_filename)
    with open(yaml_filepath, 'r') as file:
        yaml_config = yaml.safe_load(file)
        logger.info('LOG: YAML contents loaded successfully.')
        
    return yaml_config


#Loads environment variables from config.env
def load_env(env_filename='config.env', env_dirname='config', is_testing=False):
    import dotenv
    """
    Load environment variables from a .env file.

    Parameters:
    - env_filename (str): Name of the .env file.
    - env_dirname (str): Directory path containing the .env file.
    - is_testing (bool): Flag to indicate if the function is being run for testing purposes.
    """
    
    #is_testing = True
    if is_testing ==True:
        env_filename='config.env' 
        env_dirname='C:\_repos\chatforme_bots\config'

    env_filepath = os.path.join(os.getcwd(), env_dirname, env_filename)
    if dotenv.load_dotenv(env_filepath):
        logger.info('LOG: Environment file loaded successfully.')
    else:
        logger.error('LOG: Failed to load environment file.')

def main():
    load_env()
    yaml_data = load_yaml()
    return yaml_data

if __name__ == "__main__":
    main()
