from lib.queue_brokers.SQS import factory_sqs



def get_queue_broker(qbroker_name):

    def queue_broker_dict():
        return {
            'SQS': factory_sqs()
        }
    broker = queue_broker_dict().get(qbroker_name)
    if not broker:
        raise AttributeError("Broker not Found. Check settings.py \
                and verify if you put a valid queue_broker in \
                QUEUE_BROkER")
    return broker
