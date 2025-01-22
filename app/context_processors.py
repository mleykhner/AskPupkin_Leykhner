# from models.popular_tag import mock_popular_tags
from app import models
from app.models import Profile
import jwt
import time
from AskPupkin_Leykhner.settings import CENTRIFUGO_SECRET_KEY, CENTRIFUGO_WS_URL

def get_centrifugo_info(request):
    secret = CENTRIFUGO_SECRET_KEY
    ws_url = CENTRIFUGO_WS_URL
    claims = {"sub": str(request.user.id), "exp": int(time.time()) + 5*60}
    token = jwt.encode(claims, secret, algorithm="HS256")
    return {"token": token, "ws_url": ws_url}

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