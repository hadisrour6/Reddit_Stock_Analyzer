import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email_with_json(sender_email, sender_password, recipient_email, subject, json_file_path):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the JSON file
    with open(json_file_path, 'rb') as f:
        attached_json = MIMEApplication(f.read(), _subtype="json")
        attached_json.add_header('Content-Disposition', 'attachment', filename=json_file_path.split('/')[-1])
        msg.attach(attached_json)

    # Add a plain text body (optional)
    msg.attach(MIMEText("Please find the attached JSON file.", 'plain'))

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465) # Example for Gmail
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage:
# create a dummy JSON file for testing
dummy_data = {"name": "Test User", "age": 30, "city": "Exampleville"}
with open("data.json", "w") as f:
    json.dump(dummy_data, f)

sender = "your_email@example.com"
password = "your_app_password" # Use an app password for security (e.g., for Gmail)
recipient = "recipient_email@example.com"
subject = "JSON File Attachment"
json_file = "data.json"

send_email_with_json(sender, password, recipient, subject, json_file)