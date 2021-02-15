# -*- coding: utf-8 -*-

import json
import os

import boto3

dynamo = boto3.resource('dynamodb')
dynamo_table = dynamo.Table(os.environ.get("DYNAMO_TABLE"))


def lambda_handler(event, context):
    """ Receive Events notifications from SES """

    for record in event.get("Records", []):
        body = record.get("body", "{}")
        if body:
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                # SNS could sent messages like below:
                # Successfully validated SNS topic for Amazon SES event publishing.
                return

            message_id = body["mail"]["messageId"]
            event_type = body["eventType"]

            function = event_mapper.get(event_type)
            if function:
                data = function(body) or {}
                data.update({"message_id": message_id, "event_type": event_type})
                dynamo_table.put_item(Item=data)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Events updated!"
        })
    }


def _send(message_data: dict):
    mail_data = message_data["mail"]
    return {
        "timestamp": mail_data["timestamp"],
        "destination": mail_data["destination"]
    }


def _delivery(message_data: dict):
    event_data = message_data["delivery"]
    return {
        "timestamp": event_data["timestamp"],
        "processing_time_millis": event_data["processingTimeMillis"],
        "recipients": event_data["recipients"],
        "smtp_response": event_data["smtpResponse"],
        "reporting_mta": event_data["reportingMTA"]
    }


def _open(message_data: dict):
    event_data = message_data["open"]
    return {
        "timestamp": event_data["timestamp"],
        "userAgent": event_data["userAgent"],
        "ipAddress": event_data["ipAddress"]
    }


def _click(message_data: dict):
    event_data = message_data["click"]
    return {
        "ip_address": event_data["ipAddress"],
        "timestamp": event_data["timestamp"],
        "link": event_data["link"],
        "link_tags": event_data["linkTags"],
        "user_agent": event_data["userAgent"]
    }


def _reject(message_data: dict):
    event_data = message_data["reject"]
    return {
        "reason": event_data["reason"]
    }


def _bounce(message_data: dict):
    event_data = message_data["bounce"]
    return {
        "bounce_type": event_data["bounceType"],
        "bounce_subtype": event_data["bounceSubType"],
        "bounced_recipients": event_data["bouncedRecipients"]
    }


def _complaint(message_data: dict):
    event_data = message_data["complaint"]
    return {
        "complained_recipients": event_data["complainedRecipients"],
        "timestamp": event_data["timestamp"],
        "feedback_id": event_data["feedbackId"],
        "user_agent": event_data["userAgent"],
        "complaint_feedback_type": event_data["complaintFeedbackType"],
        "arrival_date": event_data["arrivalDate"]
    }


def _rendering_failure(message_data: dict):
    event_data = message_data["failure"]
    return {
        "error_message": event_data["errorMessage"],
        "template_name": event_data["templateName"]
    }


def _delivery_delay(message_data: dict):
    event_data = message_data["deliveryDelay"]
    return {
        "timestamp": event_data["timestamp"],
        "delay_type": event_data["delayType"],
        "expiration_time": event_data["expirationTime"],
        "delayed_recipients": event_data["delayedRecipients"]
    }


event_mapper = {
    "Bounce": _bounce,
    "Complaint": _complaint,
    "Delivery": _delivery,
    "Send": _send,
    "Reject": _reject,
    "Open": _open,
    "Click": _click,
    "Rendering Failure": _rendering_failure,
    "DeliveryDelay": _delivery_delay,
}
