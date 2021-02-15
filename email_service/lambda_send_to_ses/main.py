# -*- coding: utf-8 -*-

import json
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3

ses = boto3.client("ses")
s3 = boto3.client("s3")


def lambda_handler(event: dict, context):
    print("Starting send email process...")
    records = event.get("Records", [])
    if not records:
        print("No records found!")

    for record in records:
        data = record.get("body")
        if data:
            data = json.loads(data)
            destination = data.get("Destination")
            message = data.get("Message")
            source = data.get("Source")

            args = {
                "Source": source,
                "Destination": destination,
                "ConfigurationSetName": data.get("ConfigurationSetName"),
                "Message": message
            }

            # Because these parameters can not be empty...
            not_none_parameters = [
                "ReturnPath", "SourceArn",
                "ReturnPathArn", "ReplyToAddresses",
                "ConfigurationSetName", "Tags"
            ]

            for id_ in not_none_parameters:
                if data.get(id_):
                    args[id_] = data[id_]

            contains_attachment = data.get("Attachments", [])
            if contains_attachment:
                raw_message = MIMEMultipart()
                raw_message['Subject'] = message["Subject"]["Data"]
                raw_message['From'] = source

                destinations = destination.get("ToAddresses") + \
                               destination.get("CcAddresses") + \
                               destination.get("BccAddresses")

                raw_message["To"] = ', '.join(destinations)
                part = MIMEText(message["Body"]["Html"]["Data"], 'html')
                raw_message.attach(part)

                for attachment in data["Attachments"]:
                    file_ = s3.get_object(
                        Bucket=attachment.get("Bucket"),
                        Key=attachment.get("Key"))

                    file_data = file_["Body"].read()
                    part = MIMEApplication(file_data)
                    part.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=f"{attachment['Name']}.{attachment['Ext']}"
                    )

                    raw_message.attach(part)

                args.update({
                    "Destinations": destinations,
                    "RawMessage": {
                        "Data": raw_message.as_string()
                    }
                })

                del args["Message"]
                del args["Destination"]

            try:
                method = getattr(ses, "send_raw_email" if contains_attachment else "send_email")
                response = method(**args)
                print(f"Message: {response.get('MessageId')} successfully sent!")

            except Exception as error:
                print(error)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Were sent {len(records)} emails!"
        })
    }
