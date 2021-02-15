# -*- coding: utf-8 -*-

import json


sqs_event = {
  "Records": [
    {
      "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb77",
      "receiptHandle": "MessageReceiptHandle",
      "body": json.dumps({
        "Destination": {
            "BccAddresses": [
            ],
            "CcAddresses": [
            ],
            "ToAddresses": [
                "alek.cora.glez@gmail.com"
            ]
        },
        "Message": {
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": "Test. https://as.com"
                },
                "Text": {
                    "Charset": "UTF-8",
                    "Data": "XYZ"
                }
            },
            "Subject": {
                "Charset": "UTF-8",
                "Data": "Test email"
            }
        },
        "Source": "alek.cora.glez@gmail.com",
        "ConfigurationSetName": "EmailServiceConfigurationSet"
      }),
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1523232000000",
        "SenderId": "123456789012",
        "ApproximateFirstReceiveTimestamp": "1523232000001"
      },
      "messageAttributes": {},
      "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
      "awsRegion": "us-west-2"
    },
    {
      "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
      "receiptHandle": "MessageReceiptHandle",
      "body": json.dumps({
        "Destination": {
            "BccAddresses": [
            ],
            "CcAddresses": [
            ],
            "ToAddresses": [
                "alek.cora.glez@gmail.com"
            ]
        },
        "Message": {
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": "Test. https://as.com"
                },
                "Text": {
                    "Charset": "UTF-8",
                    "Data": "XYZ"
                }
            },
            "Subject": {
                "Charset": "UTF-8",
                "Data": "Test email"
            }
        },
        "Source": "alek.cora.glez@gmail.com",
        "ConfigurationSetName": "EmailServiceConfigurationSet",
        "Attachments": [
            {
                "Bucket": "email-service-bucket",
                "Key": "ticket.pdf",
                "Name": "ticket",
                "Ext": "pdf"
            }
        ]
      }),
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1523232000000",
        "SenderId": "123456789012",
        "ApproximateFirstReceiveTimestamp": "1523232000001"
      },
      "messageAttributes": {},
      "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
      "awsRegion": "us-west-2"
    }
  ]
}
