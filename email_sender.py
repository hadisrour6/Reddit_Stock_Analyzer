import os
import ssl
import smtplib
import glob
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def build_message(sender, recipient, subject, body, *attachments):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    # Loop through each attachment path
    for attachment_path in attachments:
        if not os.path.exists(attachment_path):
            raise FileNotFoundError(f"{attachment_path} not found")

        with open(attachment_path, "rb") as f:
            data = f.read()

        filename = os.path.basename(attachment_path)
        msg.add_attachment(
            data,
            maintype="application",
            subtype="json",
            filename=filename
        )
    return msg

def send_email(msg, server, port, username, password):
    port = int(port)
    if port == 465:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(server, port, context=context) as smtp:
            smtp.login(username, password)
            smtp.send_message(msg)
    else:
        # Assume STARTTLS (e.g., port 587)
        with smtplib.SMTP(server, port) as smtp:
            smtp.ehlo()
            smtp.starttls(context=ssl.create_default_context())
            smtp.ehlo()
            smtp.login(username, password)
            smtp.send_message(msg)

def send_updates():
    json1 = "results.json"
    json2 = "big_movement.json"

    server = os.getenv("SMTP_SERVER")
    port = os.getenv("SMTP_PORT", "465")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM", username)
    email_to = os.getenv("EMAIL_TO")
    subject = "Reddit Stock Analyzer daily update"

    # Quick sanity checks
    missing = [k for k, v in {
        "SMTP_SERVER": server,
        "SMTP_PORT": port,
        "SMTP_USERNAME": username,
        "SMTP_PASSWORD": password,
        "EMAIL_TO": email_to
    }.items() if not v]
    if missing:
        raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")

    body = (
        f"Hey handsome,\n\n"
        f"These are the results for Reddit Stock Analyzer from.\n\n"
        f"results.json and big_movement.json\n"
        f"— Automated sender"
    )

    msg = build_message(email_from, email_to, subject, body, json1, json2)
    send_email(msg, server, port, username, password)

