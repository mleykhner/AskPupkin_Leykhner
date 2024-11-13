from django.contrib import admin

from app.models import Tag, Profile, Question, Answer, QuestionVote, AnswerVote

admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionVote)
admin.site.register(AnswerVote)