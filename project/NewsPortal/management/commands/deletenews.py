from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from NewsPortal.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление новостей из какой либо категории'
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True  # напоминать о миграциях

    def add_arguments(self, parser):
        # parser.add_argument('argument', nargs='+', type=int)
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(
            f'Вы правда хотите удалить все статьи в '
            f'категории {options["category"]}? (yes/no)\n')
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(postCategory=category).delete()
            self.stdout.write(self.style.SUCCESS(
                # при неправильном подтверждении в доступе будет отказано
                f'Все новости из категории {category.name} были удалены.'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'Не удалось найти категорию '))
