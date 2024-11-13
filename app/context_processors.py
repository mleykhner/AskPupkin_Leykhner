from models.popular_tag import mock_popular_tags

def popular_tags(request):
    return { 'popular_tags': mock_popular_tags }