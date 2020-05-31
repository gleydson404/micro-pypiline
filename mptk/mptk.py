import logging
from sys import exit as sexit

from mptk.queue_broker import get_queue_broker
from settings import QUEUE_BROkER_NAME

from importlib import import_module

def get_messages():

    try:
        qbroker = get_queue_broker(QUEUE_BROkER_NAME)
    except AttributeError:
        logging.error('BROKER NOT FOUND')
        sexit()

    return qbroker.get_messages()

def apply_step(step, obj, step_config):
    logging.info('applying step %s', str(step))
    return step(obj, step_config)


def run(*, pipeline, messages):
    for msg in messages:
        obj = msg.body
        step_config = {}
        for step in pipeline:
            module_imported = import_module(f'steps.{step}')
            func_step = module_imported.execute_step
            obj, step_config = apply_step(func_step, obj, step_config)
