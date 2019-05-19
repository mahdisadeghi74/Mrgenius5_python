from django.contrib import admin
from .models import Player, Question, WordList, QuestionPlayer, TowQuestionPlayer
# Register your models here.

admin.site.register(Player)
admin.site.register(Question)
admin.site.register(WordList)
admin.site.register(QuestionPlayer)
admin.site.register(TowQuestionPlayer)