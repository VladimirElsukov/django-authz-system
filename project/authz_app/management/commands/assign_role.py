# authz_app/management/commands/assign_role.py
from django.core.management.base import BaseCommand
from authz_app.models import CustomUser, Role

class Command(BaseCommand):
    help = 'Назначает роль пользователю.'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Адрес электронной почты пользователя.')
        parser.add_argument('--role', type=str, help='Название роли.')

    def handle(self, *args, **options):
        email = options['email']
        role_name = options['role']
        user = CustomUser.objects.get(email=email)
        user.assign_role(role_name)
        self.stdout.write(self.style.SUCCESS(f'Роль "{role_name}" назначена пользователю {email}.'))