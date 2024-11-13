# from models.popular_tag import mock_popular_tags
from app import models


def popular_tags(request):
    popular = models.Tag.objects.get_popular()
    return { 'popular_tags': popular }

def best_members(request):
    best = models.Profile.objects.best_members()
    return { 'members': best }