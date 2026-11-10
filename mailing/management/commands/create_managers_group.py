from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailing.models import Mailing
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Создает группу Менеджеры с нужными правами'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Менеджеры')

        # 1. Право на отключение/изменение рассылки
        mailing_ct = ContentType.objects.get_for_model(Mailing)
        perm_change_mailing = Permission.objects.get(codename='change_mailing', content_type=mailing_ct)

        # 2. Право на блокировку пользователя
        user_ct = ContentType.objects.get_for_model(CustomUser)
        perm_change_user = Permission.objects.get(codename='change_customuser', content_type=user_ct)

        group.permissions.add(perm_change_mailing, perm_change_user)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана!'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Менеджеры" уже существует. Права обновлены.'))
