from collections import namedtuple

import boto3

from settings import factory_settings


def default_aws_config(broker_config):
    aws_access_key_id = broker_config.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = broker_config.get('AWS_SECRET_ACCESS_KEY')
    region_name = broker_config.get('REGION_NAME')
    AWSConfig = namedtuple(
        'AWSConfig',
        'aws_access_key_id aws_secret_access_key region_name',
    )
    return AWSConfig(
        aws_access_key_id,
        aws_secret_access_key,
        region_name
    )

def default_queue_config():
    QueueConfig = namedtuple(
        'QueueConfig',
        'batch_size visibility_timeout, attribute_names message_attribute_names, wait_time_seconds',
    )

    return QueueConfig(10, 60, ["body"], ['ALL'], 0)

def get_queue_name(broker_config):
    return broker_config.get('QUEUE_NAME')

def load_broker_config(func):
    def inner(*args, **kwargs):
        broker_config = factory_settings().get_broker_config()
        kwargs['aws_config'] = default_aws_config(broker_config)
        kwargs['queue_name'] = get_queue_name(broker_config)
        return func(*args, **kwargs)
    return inner


@load_broker_config
def create_sqs(aws_config, queue_name):
    return boto3.resource(
        'sqs',
        aws_access_key_id=aws_config.aws_access_key_id,
        aws_secret_access_key=aws_config.aws_secret_access_key,
        region_name=aws_config.region_name
    ).get_queue_by_name(QueueName=queue_name)


def sqs(func):
    def inner(*args, **kwargs):
        queue = create_sqs(**kwargs)
        kwargs['queue'] = queue
        return func(*args, **kwargs)
    return inner


@sqs
def get_messages(queue, queue_config=default_queue_config()):
    return queue.receive_messages(
        AttributeNames=queue_config.attribute_names,
        MaxNumberOfMessages=queue_config.batch_size,
        MessageAttributeNames=queue_config.message_attribute_names,
        VisibilityTimeout=queue_config.visibility_timeout,
        WaitTimeSeconds=queue_config.wait_time_seconds
    )



@sqs
def send_msg(queue, message, msg_group_id):
    queue.send_message(
        MessageBody=message,
        MessageGroupId=msg_group_id
    )
    return True


@sqs
def send_msg_batch(queue, messages, msg_group_id):
    batch = []
    for index, item in enumerate(messages):
        msg = {
            'Id': str(index),
            'MessageBody': item.replace('\n', ''),
            'MessageGroupId': msg_group_id
        }
        print("add line: " + str(index))

        if index % 10 == 0:
            batch.append(msg)
            queue.send_messages(Entries=batch)
            batch.clear()
        else:
            batch.append(msg)
    if batch:
        queue.send_messages(Entries=batch)


def factory_sqs():
    SQS = namedtuple('SQS', 'send_msg_batch send_msg get_messages')
    return SQS(
        send_msg_batch=send_msg_batch,
        send_msg=send_msg,
        get_messages=get_messages
        )
