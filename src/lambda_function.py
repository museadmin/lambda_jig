"""
A Lambda that can be run / debugged locally while developing
in an IDE like Pycharm
"""
from __future__ import print_function
import boto3


def use_sdk():
    """
    Describe any ec2 volumes in the target environment to prove
    we can use the boto3 SDK from within the lambda handler.
    Authentication is achieved by setting the AWS credentials in a run config:
    AWS_SESSION_TOKEN=
    AWS_SECRET_ACCESS_KEY=
    AWS_ACCESS_KEY_ID=
    """
    print('VOLUMES -------------------------------------')
    ec2 = boto3.client('ec2')
    for volume in ec2.describe_volumes()['Volumes']:
        print(f"Volume found: {volume['VolumeId']}")


def logging(context):
    """
    Use the context log() method instead of printing directly
    :param context: class
    :return:
    """
    print('LOGGING -------------------------------------')
    print("INFO: Logging from inside the lambda_handler")
    context.log('INFO: Using the context logger method')
    print('\n')


def show_context(context):
    """
    Print out the public methods and object type of the context
    :param context: class
    """
    print('CONTEXT -------------------------------------')
    print(f'Context is object of type ({type(context)})')
    methods = [method_name for method_name in dir(context)
               if callable(getattr(context, method_name))]
    for method in methods:
        print(f'Context method: {method}')

    for attr in context.__dict__:
        print(f'Context property ({attr})')
    print('\n')


def show_event(event):
    """
    Print out the public methods and object type of the event
    :param event: dict
    """
    print('EVENT ---------------------------------------')
    print(f'Event is an object of type ({type(event)})')
    methods = [method_name for method_name in dir(event)
               if callable(getattr(event, method_name))]
    for method in methods:
        print(f'Event method: {method}')
    print('\n')


def lambda_handler(event, context):
    """
    The Lambda Handler called by AWS or the simulator.

    This function is the entry point for your Lambda Code

    :param event: dict passed by the triggering event
    :param context: Get metadata about this function, see -
        https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    :return: Whatever it is you want to return from your Lambda
    """

    # Print out the event and context attributes and methods
    show_event(event)
    show_context(context)
    logging(context)
    use_sdk()

    print('\nRESULT -------------------------------------')

    return event.get("key1")


# Everything in __main__ block is ignored by AWS as it is only
# called when run from the command line.
if __name__ == "__main__":

    # Imported here to prevent import from within AWS lambda
    import mock_context
    import mock_event

    # Create an event and context mock
    te = mock_event.event
    tc = mock_context.MockContext()

    # Wrap the call to the lambda in a print statement
    print(f'Lambda result is: {lambda_handler(te, tc)}')
