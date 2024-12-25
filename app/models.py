import os
import uuid
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Case, When, Count, Max, ExpressionWrapper, FloatField, F, IntegerField
from django.db.models.functions import Cast


class QuestionManager(models.Manager):
    def with_votes(self):
        return self.annotate(
            votes_total=Sum(
                Case(
                    When(votes__is_negative=False, then=1),
                    When(votes__is_negative=True, then=-1),
                    default=0,
                    output_field=models.IntegerField()
                )
            )
        )

    def hot(self):
        return self.with_votes().order_by('-votes')

    def new(self):
        return self.with_votes().order_by('-created_at')

    def with_tag(self, tag_name):
        return self.with_votes().filter(tags__name__contains=tag_name)

    def get_by_id(self, question_id):
        return self.with_votes().get(id=question_id)

class ProfileManager(models.Manager):
    def best_members(self):
        return self.annotate(answers_count=Count('answers')).order_by('-answers_count')[:10]

class TagManager(models.Manager):

    def get_popular(self):
        tags_with_question_count = self.annotate(
            questions_count=Count('questions')
        ).order_by('-questions_count')[:10]

        max_questions_count = tags_with_question_count.first().questions_count

        return tags_with_question_count.annotate(
            normalized_size=ExpressionWrapper(
                F('questions_count') / max_questions_count,
                output_field=FloatField()
            )
        ).annotate(
            size=Cast(F('normalized_size') * 8 + 8, IntegerField())
        )

class Tag(models.Model):
    name = models.CharField(max_length=30)
    objects = TagManager()
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to=".", null=True, blank=True)
    objects = ProfileManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            avatar_path = self.avatar.path
            image = Image.open(avatar_path)

            if image.mode != 'RGB':
                image = image.convert('RGB')

            width, height = image.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2
            image = image.crop((left, top, right, bottom))

            filename = f"{uuid.uuid4()}.jpeg"

            image = image.resize((250, 250))

            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)

            self.avatar.save(filename, ContentFile(buffer.read()), save=False)
            buffer.close()

            if os.path.exists(avatar_path):
                os.remove(avatar_path)

            super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuestionManager()
    def __str__(self):
        return self.title





class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    def __str__(self):
        return self.text

class QuestionVote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='question_votes')
    is_negative = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.voter} - { 'downvote' if self.is_negative else 'upvote' }: {self.question.id}"

class AnswerVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answer_votes')
    is_negative = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.voter} - { 'downvote' if self.is_negative else 'upvote' }: {self.answer.id}"