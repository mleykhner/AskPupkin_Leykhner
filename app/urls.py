from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask', views.ask, name='ask'),
    path('question/<int:question_id>', views.question, name='question'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('tag/<str:tag_name>', views.tag, name='tagged'),
    path('profile/edit', views.settings, name='settings'),
    path('hot', views.hot, name='hot'),
    path('answer/mark_correct/', views.mark_correct_answer, name='mark_correct_answer'),
    path('question/vote/', views.vote_question, name='vote_question'),
    path('answer/vote/', views.vote_answer, name='vote_answer'),

]