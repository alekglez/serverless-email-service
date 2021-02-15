# -*- coding: utf-8 -*-

import json
from unittest import TestCase
from unittest.mock import Mock, patch

from email_service.lambda_send_to_ses.main import lambda_handler
from .events import sqs_event


class SendEmailTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.aws_client_patcher = patch("botocore.client.BaseClient._make_api_call")
        cls.aws_client_mock = cls.aws_client_patcher.start()
        cls.aws_client_mock.side_effect = cls._make_api_call

    @classmethod
    def tearDownClass(cls) -> None:
        cls.aws_client_mock.stop()

    @staticmethod
    def _make_api_call(operation_name, api_params):
        mock = Mock()
        mock.read.return_value = "SomeData"

        if operation_name == "GetObject":
            return {
                "Body": mock
            }

        elif operation_name in ["SendEmail", "SendRawEmail"]:
            return {
                "MessageId": "000-000-0001"
            }

    def test_successful_execution(self):
        response = lambda_handler(sqs_event, None)
        self.assertEqual(response, {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Were sent {len(sqs_event.get('Records', []))} emails!"
            })
        })

    def test_failed_execution(self):
        with patch("botocore.client.BaseClient._make_api_call", side_effect=Exception("Errror")):
            with self.assertRaises(Exception):
                response = lambda_handler(sqs_event, None)
                self.assertEqual(response, None)

    def test_empty_execution(self):
        event = sqs_event.copy()
        event["Records"] = []

        response = lambda_handler(event, None)
        self.assertEqual(response, {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Were sent 0 emails!"
            })
        })
