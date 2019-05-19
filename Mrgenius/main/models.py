from django.db import models
from django.utils import timezone


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField("User Name", max_length=20, unique=True)
    password = models.CharField("password", max_length=20)
    email = models.EmailField("Email", unique=True, max_length=60)
    coin = models.IntegerField("Coin", default=100)
    brain_score = models.IntegerField("Brain", default=0)
    validity = models.IntegerField("Validity", default=0)

    def __str__(self):
        return "{}".format(self.username)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    question_content = models.TextField("Text", max_length=150)
    answer = models.CharField("Answer", max_length=25)
    wiki_doc = models.TextField("wiki_doc", null=True, blank=True)
    difficulty = models.FloatField("difficulty", default=0)
    activity = models.BooleanField("Activity")
    category = models.CharField("category", max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    fk_maker = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{}".format(self.id)


class WordList(models.Model):
    word = models.CharField("Word", max_length=20)
    fk_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    similarity_percent = models.FloatField("Similarity Percent")

    def __str__(self):
        return "{}".format(self.word)

    class Meta:
        unique_together = (("word", "fk_question"),)


class QuestionPlayer(models.Model):
    fk_player = models.ForeignKey(Player, on_delete=models.CASCADE,)
    fk_question = models.ForeignKey(Question, on_delete=models.CASCADE, )
    answer_status = models.BooleanField("Answer Status")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    is_playing = models.BooleanField("Is PLaying?", default=False)

    class Meta:
        unique_together = (("fk_player", "fk_question"),)


class FilteredWord(models.Model):
    word = models.CharField("Word", max_length=20, primary_key=True)


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    fk_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    report_status = models.IntegerField("report Status", default=0)


class TowQuestionPlayer(models.Model):
    id = models.AutoField(primary_key=True)
    fk_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    fk_player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    fk_player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)ss')
    is_playing = models.BooleanField("is_playing", default=True)


class Winner(models.Model):
    fk_two_question_player = models.ForeignKey(TowQuestionPlayer, on_delete=models.CASCADE)
    winner = models.IntegerField("Winner", default=0)
    score = models.FloatField("score", default=0)
