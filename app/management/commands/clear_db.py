from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from progress.bar import IncrementalBar

from app.models import Question, Answer, Tag, QuestionVote, AnswerVote, Profile

class Command(BaseCommand):
    help = 'Clears the database.'

    def handle(self, *args, **options):
        tables = [User, Profile, Question, Answer, Tag, QuestionVote, AnswerVote]
        deletion_bar = IncrementalBar('Removing data', max=len(tables))
        for table in tables:
            table.objects.all().delete()
            deletion_bar.next()
        deletion_bar.finish()
        self.stdout.write(self.style.SUCCESS('All data cleared.'))