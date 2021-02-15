# -*- coding: utf-8 -*-

import json
from unittest import TestCase
from unittest.mock import Mock, patch

from email_service.lambda_track_events.main import lambda_handler
from .events import ses_events


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
        mock.Table = Mock()
        mock.read.return_value = "SomeData"

    def test_successful_execution(self):
        for event in ses_events:
            event["eventType"] = event["notificationType"]
            response = lambda_handler({"Records": [{"body": json.dumps(event)}]}, None)

            self.assertEqual(response, {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Events updated!"
                })
            })
