from email.message import EmailMessage

import aiosmtplib
from fastapi.templating import Jinja2Templates

from config import settings

templates = Jinja2Templates(directory="templates")

async def send_email(to_email: str, subject: str, plain_text: str, html_content: str | None) -> None:
    message = EmailMessage()
    message["From"] = settings.mail_from
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content(plain_text)

    if html_content:
        message.add_alternative(html_content, subtype="html")
    
    await aiosmtplib.send(
        message,
        hostname=settings.mail_server,
        port=settings.mail_port
    )


async def send_password_reset_email(to_email: str, username: str, token: str) -> None:
    reset_url = f"{settings.frontend_url}/reset-password?token={token}"

    template = templates.env.get_template("email/password_reset.html")
    html_content = template.render(reset_url=reset_url, username=username)

    plain_text = f"""Hi {username},

    You requested to reset your password. Click the link below to set a new password:

    {reset_url}

    This link will expire in 30 minutes.

    If you didn't request this, you can safely ignore this email.

    Best Regards,
    The Cenetlab Team
    """

    await send_email(to_email=to_email, subject="Reset Your Password - Cenetlab Blog", plain_text=plain_text, html_content=html_content)
