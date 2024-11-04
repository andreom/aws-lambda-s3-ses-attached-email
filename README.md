# S3 Event Triggered Email Sender with CSV Attachment

This project provides a serverless solution using AWS Lambda to automatically send emails with CSV attachments via Amazon SES. The Lambda function is triggered by new object creation events in an S3 bucket.  CloudWatch is used for logging and monitoring.

## Overview

The workflow is as follows:

1. **File Upload:** A CSV file is uploaded to a designated S3 bucket.
2. **S3 Event Notification:** An S3 event notification is triggered upon file upload.
3. **Lambda Trigger:** The S3 event notification triggers the Lambda function.
4. **File Download & Rename:** The Lambda function downloads the CSV, renames it based on the previous day's date, and saves it to the `/tmp` directory.
5. **Email Sending:** The function then sends an email via Amazon SES with the renamed CSV file as an attachment.
6. **Logging:** All function activity is logged to CloudWatch for monitoring and troubleshooting.


## Prerequisites

* An AWS Account
* AWS SES configured
* AWS S3 bucket configured
* Python 3.9 or later


## Deployment

1. **Create an IAM Role:**  Create an IAM role with the following two policies attached. This ensures the Lambda function has necessary permissions to interact with S3 and SES:

    * **`lambda-function-policy.json`**: Allows Lambda invocation. Replace placeholders `<aws_region>`, `<aws_account_id>`, and `<lambda_function_name>` with your specific values.
    * **`s3-ses-policy.json`**:  Allows interaction with S3 (get object, list bucket) and sending emails via SES. Replace the placeholders  `<s3_bucket_name>`, `<aws_region>`, `<aws_account_id>`, and `<sender_email_domain>` with your specific values.


2. **Create Lambda Function:**
    - In the AWS Lambda console, create a new Lambda function.
    - Use Python 3.9 or later as the runtime.
    - Choose the IAM role created in the previous step.
    - Paste the code from `lambda_function.py` into the function's editor.
    - Replace placeholders `<sender_email>`, `<recipient_email>`, `<cc_email>`, and `<aws_region>` with your specific values.
    - Save the function.

3. **Configure S3 Event Trigger:**
    - In the S3 console, navigate to the desired bucket.
    - Go to "Properties" > "Event notifications".
    - Create a new event notification.
    - Select "All object create events".  
    - Choose the Lambda function you created as the destination.
    - Save the event notification.



## License

This project is licensed under the MIT License.