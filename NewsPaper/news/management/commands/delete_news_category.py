from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет посты указанной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', nargs='+', type=str)

    def handle(self, *args, **options):
        if options['category'][0] not in Category.objects.values_list('name', flat=True):
            self.stdout.write(f"Нет такой категории {options['category'][0]}")
            return

        self.stdout.readable()
        self.stdout.write(f"Удалить все посты категории {options['category'][0]}? yes/no")
        answer = input()
        if answer == 'yes':
            Post.objects.filter(category__name=options['category'][0]).delete()
            self.stdout.write(self.style.SUCCESS(f"Посты категории {options['category'][0]} удалены"))
            return
        self.stdout.write(self.style.ERROR('Нет прав доступа'))

