import json

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect

from AskPupkin_Leykhner.settings import CENTRIFUGO_API_URL, CENTRIFUGO_API_KEY
from app import models
from app.forms import UserRegistrationForm, ProfileForm, ProfileEditForm, QuestionForm, AnswerForm
from app.models import Tag, Question, QuestionVote, Answer, AnswerVote
from app.pagination import paginate

from cent import Client, PublishRequest


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

            data = {
                "question_id": question_id,
                "answer_id": answer.id,
                "avatar_url": answer.author.avatar.url,
                "text": answer.text,
                "votes_total": 0
            }

            answer_json = json.dumps(data)

            api_url = CENTRIFUGO_API_URL
            api_key = CENTRIFUGO_API_KEY

            try:
                client = Client(api_url=api_url, api_key=api_key)
                r = PublishRequest(channel=str(question_id), data=json.loads(answer_json))
                result = client.publish(r)
            except Exception as e:
                print(f"Error while publishing to Centrifugo: {e}")

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

@login_required
def mark_correct_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_id = request.POST.get('answer_id')

        found_question = models.Question.objects.get_by_id(question_id)
        found_answer = found_question.answers.get(id=answer_id)

        if found_question.author.user != request.user:
            return JsonResponse({'error': 'Only the author of the question can mark the correct answer'}, status=403)

        found_question.answers.update(is_correct=False)
        found_answer.is_correct = True
        found_answer.save()

        return JsonResponse({'success': True, 'correct_answer_id': found_answer.id})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def vote_question(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        is_negative = request.POST.get('is_negative') == 'true'
        try:
            question = Question.objects.get(id=question_id)
            vote, created = QuestionVote.objects.get_or_create(
                question=question,
                voter=request.user.profile,
                defaults={'is_negative': is_negative}
            )
            if not created:
                if vote.is_negative == is_negative:
                    vote.delete()
                else:
                    vote.is_negative = is_negative
                    vote.save()
            total_votes = question.votes.filter(is_negative=False).count() - question.votes.filter(is_negative=True).count()
            return JsonResponse({'success': True, 'total_votes': total_votes})
        except Question.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Question not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def vote_answer(request):
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        is_negative = request.POST.get('is_negative') == 'true'
        try:
            answer = Answer.objects.get(id=answer_id)
            vote, created = AnswerVote.objects.get_or_create(
                answer=answer,
                voter=request.user.profile,
                defaults={'is_negative': is_negative}
            )
            if not created:
                if vote.is_negative == is_negative:
                    vote.delete()
                else:
                    vote.is_negative = is_negative
                    vote.save()
            total_votes = answer.votes.filter(is_negative=False).count() - answer.votes.filter(is_negative=True).count()
            return JsonResponse({'success': True, 'total_votes': total_votes})
        except Answer.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Answer not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})