import unittest
import mock_context
import mock_event
import lambda_function


class TestStringMethods(unittest.TestCase):
    """
    Example unit test framework asserts against the context simulator
    """
    def setUp(self):
        self.cntxt = mock_context.MockContext()
        self.event = mock_event.event
        self.ver = self.cntxt.function_version
        self.lambda_function = lambda_function

    def test_function_name(self):
        self.assertEqual(self.cntxt.function_name, 'lambda_handler')

    def test_function_version(self):
        self.assertEqual(self.ver, 1)

    def test_invoked_function_arn(self):
        self.assertEqual(
            self.cntxt.invoked_function_arn,
            f'arn:aws:lambda:eu-west-2:410954063198:function:lambda_handler:{self.ver}'
        )

    def test_lambda(self):
        self.assertEqual(
            self.lambda_function.lambda_handler(self.event, self.cntxt),
            'value1'
        )


if __name__ == '__main__':
    unittest.main()
