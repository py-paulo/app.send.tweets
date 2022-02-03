from botocore.exceptions import ClientError


def sqs_send_message(sqs, queue_url: str, message_attributes: dict, message_body: dict):
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageAttributes=message_attributes,
            MessageBody=message_body
        ) 
    except ClientError as err:
        raise err
    else:
        return response['MessageId']
