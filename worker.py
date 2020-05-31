from mptk.mptk import run
from mptk.mptk import get_messages

PIPELINE = [
    'step1',
    'step2'
]


run(pipeline=PIPELINE, messages=get_messages())
