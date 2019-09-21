class MockContext:
    """
    A class to simulate a Lambda context

    Excludes mobile app fields
    """

    def __init__(self):
        self.aws_request_id = 'a3de505e-f16b-42f4-b3e6-bcd2e4a73903'
        self.client_context = None
        self.function_name = 'lambda_handler'
        self.function_version = 1
        self.identity = None
        self.invoked_function_arn = \
            f'arn:aws:lambda:eu-west-2:410954063198:function:lambda_handler:{self.function_version}'
        self.log_group_name = 'log:group:name'
        self.log_stream_name = 'log:stream:name'
        self.memory_limit_in_mb = 128

    @staticmethod
    def get_remaining_time_in_millis():
        return 1234567890

    @staticmethod
    def log(message):
        print(message)
