# Micro Pypeline

This project is just an example of a final result of MPTK  creation command.

The idea here is to show a way to simplify the construction of a project to be executed as kubernetes parallel job.

## What is MPTK?

MPTK is a framework that aims to improve the way, we build kuberkentes parallel jobs
applications.

## Why use MPTK

If you already have to write a project to run in a parallel job, you probably know that you have to write some code that makes an interface with a message broker. Once you have written this part of the project, you will write code on your own to achieve your go. No problem, except if you need to write jobs at a certain frequency.

MPTK provides a skeleton for your application, abstracting the interaction with a message broker and offer a way to write pipeline as code ( Yes, I take some inspiration on AirFlow ).

## Can I use this?

You shouldn't, but you can.
For now, this project only works with AWS SQS. Once you have filled your queue, follow the steps below.

### 1 - Create a .env file with the content below filled
```
QUEUE_NAME=
QUEUE_BATCH_SIZE=10
VISIBILITY_TIMEOUT=60
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

```
`QUEUE_NAME` -> put here the name of your queue;

`QUEUE_BATCH_SIZE` -> put here the max batch size for your queue. SQS max is 10;

`VISIBILITY_TIMEOUT`-> put here the visibility timeout for your queue. This parameter is something like the time of worker needs to handle the task on the message. It's in seconds. Try 60 and group up this value if you have errors to delete messages because the token has expired.

`AWS_REGION`-> put here the AWS region for your queue;

`AWS_ACCESS_KEY_ID` -> put here your AWS access key id;

`AWS_SECRET_ACCESS_KEY` -> put here your AWS secret access key;

### 2 - Write your steps

A step in MPTK is just a python module in `steps folder with the method `def execute_step(obj, step_config):  return obj, step_config`.

This is necessary because every step must have enough inputs for the next one.

Example.:
step1.py
```
def execute_step(obj, step_config):
    # do your stuff here
    print('step1 executed')
    return obj, step_config

```

### 3 - Configure your worker
At this point, you can choose the sequence of your steps in a sort of pipeline like in the example below. The strings on `PIPELINE` are the names of the scripts in `steps` folder.

worker.py
```
from mptk.mptk import run
from mptk.mptk import get_messages

PIPELINE = [
    'step1',
    'step2'
]

run(pipeline=PIPELINE, messages=get_messages())
```

Now, you just need to point your container entrypoint tho this worker.

## Where is MPTK?

MPTK is being developed. Once I have an alfa version, I will update this readme with the link.

This project is right in the beginning if you have ideas to improve, feel free to open an issue.

Regards!

