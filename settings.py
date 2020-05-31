from collections import namedtuple
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# use AWS SQS
QUEUE_BROkER_NAME = 'SQS'


def get_broker_config(broker_name=QUEUE_BROkER_NAME):
    brokers_config = {
        'SQS': {
            'QUEUE_NAME': getenv('QUEUE_NAME'),
            'QUEUE_BATCH_SIZE': getenv('QUEUE_BATCH_SIZE'),
            'VISIBILITY_TIMEOUT': getenv('VISIBILITY_TIMEOUT'),
            'AWS_REGION': getenv('AWS_REGION'),
            'AWS_ACCESS_KEY_ID': getenv('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': getenv('AWS_SECRET_ACCESS_KEY')
            }
    }
    return brokers_config.get(broker_name)

def factory_settings():
    Settings = namedtuple('Settings', 'get_broker_config')
    return Settings(get_broker_config=get_broker_config)

