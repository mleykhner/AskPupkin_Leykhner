import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from progress.bar import IncrementalBar

from app.models import Question, Answer, Tag, QuestionVote, AnswerVote, Profile


class Command(BaseCommand):
    help = 'Fill the database with test data based on the specified ratio.'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The coefficient for the amount of data to generate')

    def handle(self, *args, **options):
        ratio = options['ratio']

        tables = [User, Profile, Question, Answer, Tag, QuestionVote, AnswerVote]
        deletion_bar = IncrementalBar('Removing data', max=len(tables))
        for table in tables:
            table.objects.all().delete()
            deletion_bar.next()
        deletion_bar.finish()
        self.stdout.write(self.style.SUCCESS('All data cleared.'))

        users = []
        users_bar = IncrementalBar('Generating users', max=ratio)
        for i in range(1, ratio + 1):
            user = User(username=f'user{i}', email=f'user{i}@example.com')
            users.append(user)
            users_bar.next()
        User.objects.bulk_create(users)
        users_bar.finish()

        profiles = []
        profiles_bar = IncrementalBar('Generating users', max=len(users))
        for user in users:
            profile = Profile(user=user)
            profiles.append(profile)
            profiles_bar.next()
        Profile.objects.bulk_create(profiles)
        profiles_bar.finish()

        tags = []
        tags_bar = IncrementalBar('Generating tags', max=ratio)
        for i in range(ratio):
            tag = Tag(name=f'Tag{i}')
            tags.append(tag)
            tags_bar.next()
        Tag.objects.bulk_create(tags)
        tags_bar.finish()

        questions = []
        questions_bar = IncrementalBar('Generating questions', max=ratio * 10)
        for i in range(ratio * 10):
            question = Question(
                title=f'Question Title {i}',
                text=f'Body of question {i}',
                author=random.choice(profiles),
                created_at=timezone.now()
            )
            questions.append(question)
            questions_bar.next()
        Question.objects.bulk_create(questions)
        questions_bar.finish()

        question_tags_bar = IncrementalBar('Connecting questions with tags', max=len(questions))
        for question in questions:
            question.tags.set(random.sample(tags, k=min(3, len(tags))))
            question_tags_bar.next()
        question_tags_bar.finish()

        answers = []
        answers_bar = IncrementalBar('Generating answers', max=ratio * 100)
        for i in range(ratio * 100):
            answer = Answer(
                text=f'Content of answer {i}',
                question=random.choice(questions),
                author=random.choice(profiles),
            )
            answers.append(answer)
            answers_bar.next()
        Answer.objects.bulk_create(answers)
        answers_bar.finish()

        question_votes = set()
        question_votes_count = min(len(questions) * len(profiles), ratio * 100)
        questions_votes_bar = IncrementalBar('Generating question votes', max=question_votes_count)
        while len(question_votes) < question_votes_count:
            question = random.choice(questions)
            user = random.choice(profiles)
            question_votes.add((question, user))
        QuestionVote.objects.bulk_create(list(
            map(lambda ql: QuestionVote(question=ql[0], voter=ql[1], is_negative=bool(random.getrandbits(1))),
                question_votes)))
        questions_votes_bar.finish()

        answer_votes = set()
        answer_votes_count = min(len(questions) * len(profiles), ratio * 100)
        answer_votes_bar = IncrementalBar('Generating answers votes', max=question_votes_count)
        while len(answer_votes) < answer_votes_count:
            answer = random.choice(answers)
            user = random.choice(profiles)
            answer_votes.add((answer, user))
            answer_votes_bar.next()
        AnswerVote.objects.bulk_create(list(
            map(lambda ql: AnswerVote(answer=ql[0], voter=ql[1], is_negative=bool(random.getrandbits(1))),
                answer_votes)))

        self.stdout.write(self.style.SUCCESS('\nDatabase filled successfully.'))
