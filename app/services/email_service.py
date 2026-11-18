
import os
import smtplib
from pathlib import Path
from email.message import EmailMessage
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def send_lead_notification(lead):
    message = EmailMessage()
    message["Subject"] = "New Website Chatbot Lead"
    message["From"] = os.getenv("SMTP_FROM_EMAIL")
    message["To"] = os.getenv("LEAD_NOTIFICATION_EMAIL")

    message.set_content(f"""
New lead received from the MoinSystems chatbot.

Name: {lead.full_name}
Email: {lead.email}
Phone: {lead.phone}
Company: {lead.company or 'Not provided'}

Project details:
{lead.project_details or 'Not provided'}
""")

    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "465"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")

    if not all([host, username, password, message["From"], message["To"]]):
        raise ValueError("SMTP configuration is incomplete.")

    with smtplib.SMTP_SSL(host, port, timeout=20) as server:
        server.login(username, password)
        server.send_message(message)
