# from models.popular_tag import mock_popular_tags
from app import models
from app.models import Profile


def popular_tags(request):
    popular = models.Tag.objects.get_popular()
    return { 'popular_tags': popular }

def best_members(request):
    best = models.Profile.objects.best_members()
    return { 'members': best }

def user_navbar(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            return {
                'nickname': profile.nickname,
                'avatar_url': profile.avatar.url if profile.avatar else None,
            }
        except Profile.DoesNotExist:
            return {
                'nickname': request.user.username,
                'avatar_url': None,
            }
    return {
        'nickname': '',
        'avatar_url': None,
    }