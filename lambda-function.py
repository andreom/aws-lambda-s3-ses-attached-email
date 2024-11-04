import os.path
import boto3
import email
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import date
from datetime import timedelta

# Get today's date
today = date.today()

# Calculate yesterday's date
yesterday = today - timedelta(days=1)

# formatted yesterday date to format dd/mm/yyyy
yesterday_formatted = yesterday.strftime("%d%m%Y")

# Create an S3 client
s3 = boto3.client("s3")

def lambda_handler(event, context):
    """
    Main function executed by Lambda.

    Args:
        event: Event that triggered the Lambda.
        context: Lambda context object.
    """

    print(event)

    # Define email configuration
    SENDER = "<sender_email>"  # Replace with your sender email
    RECIPIENT = "<recipient_email>"  # Replace with the recipient email
    RECIPIENT2 = "<cc_email>"  # Replace with a CC recipient (optional)
    AWS_REGION = "<aws_region>"
    SUBJECT = f"Report for {yesterday_formatted}.csv"

    # Get information from the event
    FILEOBJ = event["Records"][0]
    BUCKET_NAME = str(FILEOBJ['s3']['bucket']['name'])
    KEY = str(FILEOBJ['s3']['object']['key'])
    FILE_NAME = os.path.basename(KEY)
    TMP = '/tmp/'
    TMP_FILE_NAME = '/tmp/' + FILE_NAME
    
    # Download the file from S3
    try:
        s3.download_file(BUCKET_NAME, KEY, TMP_FILE_NAME)
    except ClientError as e:
                return {
            'statusCode': 500,
            'body': f'Error downloading the file from S3.: {e}'
        }
    
     # Rename the file to the name of the variable yesterday_formatted
    NEW_FILE_NAME = '/tmp/' + yesterday_formatted + '.csv'
    os.rename(TMP_FILE_NAME, NEW_FILE_NAME)

    # Define the attachment with the new file name
    ATTACHMENT = NEW_FILE_NAME
    
    # Define the email body
    BODY_TEXT = f"Attached is the report created based on {yesterday}."

    # Create an SES client
    client = boto3.client('ses', region_name=AWS_REGION)

    # Create the message
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg['Cc'] = RECIPIENT2

    # Add the email body
    textpart = MIMEText(BODY_TEXT)
    msg.attach(textpart)

    # Add the attachment
    try:
        with open(ATTACHMENT, 'rb') as f:
            att = MIMEApplication(f.read())
            att.add_header('Content-Disposition', 'attachment', filename=ATTACHMENT)
            msg.attach(att)
    except Exception as e:
        print(f"Error adding the attachment: {e}")
        return {
            'statusCode': 500,
            'body': f'Error adding the attachment.: {e}'
        }

    # Send the email
    try:
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[RECIPIENT, RECIPIENT2],
            RawMessage={'Data': msg.as_string()}
        )
    except ClientError as e:
        print(f"Error sending the email: {e}")
        return {
            'statusCode': 500,
            'body': 'Error sending the email.'
        }

    print("Email sent! Message ID:", response['MessageId'])

    return {
        'statusCode': 200,
        'body': 'Email sent successfully.'
    }
