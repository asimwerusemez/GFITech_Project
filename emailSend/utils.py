import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def SendMessageEmail(subject: str, receivers: list, template: str, context: dict):
    try:
        message = render_to_string(template, context)
        email_sent = send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            receivers,  # Fix: Swap the order of sender and receivers
            fail_silently=False,
            html_message=message
        )
        if email_sent:
            logger.info(f"Email sent to {', '.join(receivers)}")
            return True
        else:
            logger.error(f"Failed to send email to {', '.join(receivers)}")
            return False
    except Exception as e:
        logger.error(e)
        return False