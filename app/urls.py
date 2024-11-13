from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask', views.ask, name='ask'),
    path('question/<int:question_id>', views.question, name='question'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('tag/<str:tag_title>', views.tag, name='tagged'),
    path('settings', views.settings, name='settings'),
    path('hot', views.hot, name='hot'),
]