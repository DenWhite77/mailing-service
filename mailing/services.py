import logging
from django.core.mail import send_mail
from django.utils import timezone
from .models import Mailing, MailingAttempt

logger = logging.getLogger(__name__)

def send_mailing(mailing_id):
    """
    Сервисная функция для отправки рассылки.
    Проверяет время, проходит по получателям, отправляет письма и логирует попытки.
    """
    try:
        mailing = Mailing.objects.get(id=mailing_id)
    except Mailing.DoesNotExist:
        logger.error(f"Рассылка с ID {mailing_id} не найдена.")
        return False

    # Проверка времени (если время старта в будущем — не отправляем)
    if mailing.start_time > timezone.now():
        logger.info(f"Рассылка {mailing_id} ещё не наступила.")
        return False

    # Проверка статуса (чтобы не отправить дважды)
    if mailing.status == 'completed':
        logger.info(f"Рассылка {mailing_id} уже завершена.")
        return False

    # Меняем статус на "Запущена"
    mailing.status = 'started'
    mailing.save()

    recipients = mailing.recipients.all()
    if not recipients:
        logger.warning(f"У рассылки {mailing_id} нет получателей.")
        mailing.status = 'completed'
        mailing.save()
        return False

    success_count = 0

    for client in recipients:
        try:
            # Отправляем письмо
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email='noreply@mailing-service.local',
                recipient_list=[client.email],
                fail_silently=False,
            )
            # Логируем успех
            MailingAttempt.objects.create(
                mailing=mailing,
                status='success',
                server_response='250 OK (Отправлено)'
            )
            success_count += 1
        except Exception as e:
            # Логируем ошибку
            MailingAttempt.objects.create(
                mailing=mailing,
                status='failed',
                server_response=str(e)
            )
            logger.error(f"Ошибка отправки на {client.email}: {e}")

    # Завершаем рассылку
    mailing.status = 'completed'
    mailing.save()
    logger.info(f"Рассылка {mailing_id} завершена. Успешно: {success_count} из {recipients.count()}")
    return True
