import os
import logging
from typing import Optional

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
except ImportError:
    SendGridAPIClient = None
    Mail = None

logger = logging.getLogger(__name__)


def send_email(subject: str, to_email: str, content: str) -> bool:
    """
    Envia email via SendGrid. Retorna True se enviado, False se falhar.
    Se SENDGRID_API_KEY ou SendGrid não estiver disponível, retorna False.
    """
    api_key = os.environ.get("SENDGRID_API_KEY")
    from_email = os.environ.get("SENDGRID_FROM")

    if not api_key or not from_email or SendGridAPIClient is None:
        logger.warning("Envio de email não configurado; pulando envio.")
        return False

    try:
        sg = SendGridAPIClient(api_key)
        message = Mail(from_email=from_email, to_emails=to_email, subject=subject, html_content=content)
        sg.send(message)
        logger.info(f"Email enviado para {to_email}")
        return True
    except Exception as e:
        logger.error(f"Falha ao enviar email: {e}")
        return False


def build_frontend_url(path: str) -> str:
    frontend_base = os.environ.get("FRONTEND_URL", "https://financeia20.vercel.app")
    return frontend_base.rstrip("/") + path


def send_verification_email(to_email: str, token: str) -> bool:
    link = build_frontend_url(f"/verify-email?token={token}")
    subject = "Confirme seu email"
    body = f"""
    <p>Olá!</p>
    <p>Clique no link para confirmar seu email: <a href="{link}">{link}</a></p>
    <p>Se você não solicitou, ignore este email.</p>
    """
    return send_email(subject, to_email, body)


def send_reset_email(to_email: str, token: str) -> bool:
    link = build_frontend_url(f"/reset-password?token={token}")
    subject = "Redefinir senha"
    body = f"""
    <p>Olá!</p>
    <p>Clique no link para redefinir sua senha: <a href="{link}">{link}</a></p>
    <p>Se você não solicitou, ignore este email.</p>
    """
    return send_email(subject, to_email, body)




