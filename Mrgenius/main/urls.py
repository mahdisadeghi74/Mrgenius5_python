from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('add_question/', views.add_question, name="add_question"),
    path('get_question/', views.get_question, name="get_question"),
    path('get_words/', views.get_words, name="get_words"),
    path('get_summary/', views.get_summary, name="get_summary"),
    path('get_info/', views.get_Info, name="get_info"),
    path('answer_the_question/', views.answer_the_question, name="answer_the_question"),
    path('get_answer_two_player/', views.get_answer_two_player, name="get_answer_two_player"),
    path('wiki_test/<str:word1>/<str:word2>/', views.wiki_test, name="wiki_test"),
    path('semantic/<str:word>/', views.semantic_similarity, name="semantic_similarity")
]
