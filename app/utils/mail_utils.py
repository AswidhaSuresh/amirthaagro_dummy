def send_password_reset_email(email, token):
    """
    Sends password reset email via MailJS.

    Args:
        email (str): Recipient email
        token (str): Reset token (JWT)
    """
    reset_link = f"https://yourdomain.com/reset-password?token={token}"

    # Compose message
    subject = "Reset Your Password"
    message = f"Hi,\n\nUse the link below to reset your password:\n{reset_link}\n\nThis link will expire soon."

    # You can replace this with MailJS or logging
    print(f"Sending password reset email to {email}:\n{message}")
