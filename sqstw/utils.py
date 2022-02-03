

def tweet_in_message_attributes_sqs(tw: dict):
    return { 
        "created_at": {
            "StringValue": tw['created_at'],
            "DataType": "String"
        },
        "id": {
            "StringValue": tw['id'],
            "DataType": "Number"
        }
    }
 