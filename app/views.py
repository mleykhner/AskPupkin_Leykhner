from django.shortcuts import render

from app import models
from app.pagination import paginate


def index(request):
    questions = models.Question.objects.new()
    page = paginate(request, questions)
    return render(
        request,
        'index.html',
        {'questionCards': page.object_list, 'page': page}
    )

def not_found(request, exception):
    return render(request, 'not_found.html')


def question(request, question_id):
    q = models.Question.objects.get_by_id(question_id)
    answers = q.answers.all()
    page = paginate(request, answers)
    return render(
        request,
        'question.html',
        {'question': q, 'answers': page.object_list, 'page': page}
    )


def tag(request, tag_name):
    questions = models.Question.objects.with_tag(tag_name)
    page = paginate(request, questions)
    return render(
        request, 'tag.html',
        {'tag_name': tag_name, 'questions': page.object_list, "page": page}
    )


def ask(request):
    return render(
        request,
        'ask.html'
    )


def settings(request):
    return render(
        request,
        'settings.html',
        # context={'user': mock_user}
    )


def login(request):
    return render(
        request,
        'login.html'
    )


def signup(request):
    return render(
        request,
        'signup.html'
    )


def hot(request):
    questions = models.Question.objects.hot()
    page = paginate(request, questions)
    return render(
        request,
        'hot.html',
        context={'questions': page.object_list, "page": page}
    )
