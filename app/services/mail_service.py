# app/services/mail_service.py
# ------------------------------------------------------------
# MailJS integration for sending password setup/reset links
# ------------------------------------------------------------

import requests
from app.config.config_loader import config_loader

MAILJS_URL = "https://api.mailjs.dev/send"
MAILJS_TOKEN = config_loader.config.get("mailjs", {}).get("access_token")
SENDER_EMAIL = config_loader.config.get("mailjs", {}).get("from_email", "admin@aswe.com")


def send_password_setup_email(to_email, party_id, token):
    link = f"https://dashboard.agri.com/password-setup?token={token}"
    subject = "🔐 Set Your Password for Agri Dashboard"
    body = f"""
        Hi {party_id},

        Please click the link below to set your password:
        {link}

        This link will expire in 1 hour.

        Regards,
        Admin Team
    """

    payload = {
        "to": to_email,
        "from": SENDER_EMAIL,
        "subject": subject,
        "text": body
    }

    headers = {"Authorization": f"Bearer {MAILJS_TOKEN}"}

    response = requests.post(MAILJS_URL, json=payload, headers=headers)
    return response.status_code == 200