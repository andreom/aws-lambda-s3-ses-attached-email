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


## Deployment project

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


## Amazon S3 Trigger Tutorial

This text summarizes the tutorial "Tutorial: Using an Amazon S3 trigger to invoke a Lambda function" found at [https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html). The tutorial demonstrates how to configure a Lambda function to be triggered by Amazon S3 events, specifically when objects are added to an S3 bucket.

# Tutorial: Using an Amazon S3 Trigger to Invoke a Lambda Function

## Description

This tutorial will guide you through creating a Lambda function that is triggered whenever an object is added to your Amazon S3 bucket. The Lambda function retrieves the object type and logs this information to Amazon CloudWatch Logs.

## Prerequisites

* **AWS Account:** Make sure you have an AWS account. If you don't have one, you can create one at [https://portal.aws.amazon.com/billing/signup](https://portal.aws.amazon.com/billing/signup).
* **Administrative User:** For security purposes, it's recommended to create and use an administrative user instead of the root user for everyday tasks.
* **AWS IAM Identity Center:** Enable IAM Identity Center and grant administrative access to a user.

## Steps

1. **Create an Amazon S3 Bucket:**
    * Open the Amazon S3 console.
    * Select "Buckets" and choose "Create bucket".
    * Enter a globally unique bucket name and choose an AWS Region.
    * Leave the other options as default and create the bucket.

2. **Upload a Test Object to the Bucket:**
    * Open the Buckets page in the S3 console and select the bucket you created.
    * Choose "Upload", add files, and select an object to upload.
    * Upload the object. This object will be used to test the Lambda function later.

3. **Create a Permissions Policy:**
    * Create a policy in IAM that allows Lambda to get objects from S3 and write to CloudWatch Logs.
    * The policy should include permissions for `logs:PutLogEvents`, `logs:CreateLogGroup`, `logs:CreateLogStream`, and `s3:GetObject`.

4. **Create an Execution Role:**
    * Create an execution role in IAM to grant the Lambda function the necessary permissions.
    * The role should use the policy created in the previous step.

5. **Create the Lambda Function:**
    * Open the Lambda console and choose "Create function".
    * Select "Author from scratch", provide a function name, and choose the Python 3.12 runtime.
    * Select the execution role created previously.
    * Create the function.

6. **Deploy the Function Code:**
    * The tutorial provides example code in Python, but also includes examples for other runtimes.
    * Copy the appropriate code and paste it into the code editor in the Lambda console.
    * Deploy the function code.

7. **Create the Amazon S3 Trigger:**
    * In the "Function overview" pane for the Lambda function, choose "Add trigger".
    * Select "S3", choose the bucket created earlier, and select "All object create events" under "Event types".
    * Create the trigger.

8. **Test the Lambda Function:**
    * You can test the Lambda function using a dummy event in the Lambda console. The tutorial provides a sample test event.
    * Replace the placeholder values in the test event with the actual values for your bucket and object.
    * Save and test the function. The execution results will be displayed in the "Execution results" tab.

9. **Test with the S3 Trigger:**
    * Upload an object to the S3 bucket to trigger the Lambda function.
    * Check the CloudWatch Logs to confirm that the function was invoked and logged the object type.

10. **Clean up the Resources:**
    * Delete the Lambda function, execution role, and S3 bucket when they are no longer needed to avoid unnecessary charges.



References:
https://medium.com/snowflake/automating-snowpipe-with-aws-eventbridge-a5ef27504949
https://aws.amazon.com/pt/blogs/messaging-and-targeting/forward-incoming-email-to-an-external-destination/
https://docs.aws.amazon.com/ses/latest/dg/policy-anatomy.html
https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html

## License

This project is licensed under the MIT License.