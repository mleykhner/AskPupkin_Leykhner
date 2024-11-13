from django.shortcuts import render

from app.pagination import paginate
from models.answer import get_by_question_id
from models.question import mock_questions, get_by_id, get_by_tag
from models.user import mock_user


def index(request):
    questions = mock_questions
    page = paginate(request, questions)
    return render(
        request,
        'index.html',
        {'questionCards': page.object_list, 'page':page}
    )

def question(request, question_id):
    question = get_by_id(question_id)
    answers = get_by_question_id(question_id)
    page = paginate(request, answers)
    return render(
        request,
        'question.html',
        {'question':question, 'answers':page.object_list, 'page':page}
    )

def tag(request, tag_title):
    questions = get_by_tag(tag_title)
    page = paginate(request, questions)
    return render(
        request, 'tag.html',
        {'tag_name': tag_title, 'questions': page.object_list, "page": page}
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
        context={'user': mock_user}
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
    questions = mock_questions
    questions.reverse()
    page = paginate(request, questions)
    return render(
        request,
        'hot.html',
        context={'questions': page.object_list, "page": page})
