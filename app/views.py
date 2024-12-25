from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from app import models
from app.forms import UserRegistrationForm, ProfileForm, ProfileEditForm, QuestionForm, AnswerForm
from app.models import Tag
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

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.profile
            answer.question = q
            answer.save()

            return redirect(f"{request.path}#answer-{answer.id}")
    else:
        form = AnswerForm()

    answers = q.answers.all()
    page = paginate(request, answers)
    return render(
        request,
        'question.html',
        {'question': q, 'answers': page.object_list, 'page': page, 'form': form}
    )


def tag(request, tag_name):
    questions = models.Question.objects.with_tag(tag_name)
    page = paginate(request, questions)
    return render(
        request, 'tag.html',
        {'tag_name': tag_name, 'questions': page.object_list, "page": page}
    )

@login_required(redirect_field_name='continue')
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.author = request.user.profile
            new_question.save()

            tags = form.cleaned_data['tags']
            for tag_name in tags:
                new_tag, created = Tag.objects.get_or_create(name=tag_name)
                new_question.tags.add(new_tag)

            messages.success(request, "Your question has been posted successfully!")
            return redirect('question', question_id=new_question.id)
    else:
        form = QuestionForm()

    return render(request, 'ask.html', {'form': form})

def hot(request):
    questions = models.Question.objects.hot()
    page = paginate(request, questions)
    return render(
        request,
        'hot.html',
        context={'questions': page.object_list, "page": page}
    )


def signup_view(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})

def login_view(request):
    continue_url = request.GET.get('continue', '/')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(continue_url)
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(redirect_field_name='continue')
def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(redirect_field_name='continue')
def settings(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=user)
        print(form)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if email and email != user.email:
                user.email = email
                user.save(update_fields=['email'])

            nickname = form.cleaned_data.get('nickname')
            if nickname and nickname != profile.nickname:
                profile.nickname = nickname

            avatar = form.cleaned_data.get('avatar')
            if avatar and avatar != profile.avatar:
                profile.avatar = avatar

            profile.save()

            messages.success(request, 'Ваш профиль был успешно обновлен.')
            return redirect('settings')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = ProfileEditForm(instance=profile, user=user)

    return render(request, 'settings.html', {'form': form, 'user': user, 'profile': profile})