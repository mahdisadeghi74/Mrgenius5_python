from idlelib.MultiCall import r

from bs4 import BeautifulSoup
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from hazm import stopwords_list
from nltk import word_tokenize, collections
from nltk.corpus import stopwords
from wikipedia import wikipedia

from .functions import CheckWord
from .models import Question, Player, QuestionPlayer, WordList, TowQuestionPlayer
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
# from .functions import CheckWord
# Create your views here.


@csrf_exempt
def register(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']


    try:
        if Player.objects.filter(username=username):
            return JsonResponse({'result': 'username'})
        elif Player.objects.filter(email=email):
            return JsonResponse({'result': 'email'})
        Player.objects.create(username=username, password=password, email=email)
        return JsonResponse({'result': 'true'})
    except:
        return JsonResponse({'result': 'false'})


@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']

    try:
        query = Player.objects.filter(username=username, password=password)
        id = list(query.values_list('id', flat=True))
        coin = list(query.values_list('coin', flat=True))
        validity = list(query.values_list('validity', flat=True))
        brain_score = list(query.values_list('brain_score', flat=True))
        if len(coin) > 0:
            return JsonResponse({'result': 'true', 'id': "{}".format(id[0]), 'coin': "{}".format(coin[0]),
                                 'validity': "{}".format(validity[0]), 'brain_score': "{}".format(brain_score[0])})
        else:
            return JsonResponse({'result': 'false'})
    except:
        return JsonResponse({'result': 'data base error'})


@csrf_exempt
def add_question(request):

    question_content = request.POST["question_content"]
    answer = request.POST["answer"]
    activity = request.POST["activity"]
    category = request.POST["category"]
    player = request.POST["player_id"]
    maker = get_object_or_404(Player, id=player)


    if Question.objects.create(question_content=question_content, category=category, answer=answer, activity=True, fk_maker=maker):
        question_id = list(Question.objects.filter(question_content=question_content,
                                                   answer=answer).values_list('id', flat=True))

        if CheckWord.add_to_database(answer, question_id[0]):
            return JsonResponse({'result': "true"})
        else:
            return JsonResponse({'result': "false"})
    else:
        return JsonResponse({'result': "true"})

@csrf_exempt
def get_question(request):
    player_id = request.POST["player_id"]

    ###if player playing one Question return this###
    query_isplaying = QuestionPlayer.objects.filter(fk_player=player_id, is_playing=True)
    if query_isplaying:
        qid = list(query_isplaying.values_list('fk_question', flat=True))
        question_query = Question.objects.filter(id=qid[0])
        question_content = list(question_query.values_list('question_content', flat=True))
        result = {'id': "{}".format(qid[0]), 'question_content': "{}".format(question_content[0])}
        return JsonResponse(result)

    ###else if player dont play one Question return this###
    question_id = list(Question.objects.all().order_by('?')[:10].values_list('id', flat=True))
    for id in question_id:
        if Player.objects.filter(id=player_id):
            query_question_player = QuestionPlayer.objects.filter(fk_question=id, fk_player=player_id)
            if not query_question_player:
                query = Question.objects.filter(id=id)
                question_content = list(query.values_list('question_content', flat=True))
                player = get_object_or_404(Player, id=player_id)
                question = get_object_or_404(Question, id=id)
                QuestionPlayer.objects.create(fk_player=player, fk_question=question, answer_status=False,
                                               is_playing=True)

                result = {'id': "{}".format(int(id)), 'question_content': "{}".format(question_content[0])}
                return JsonResponse(result)
            elif not list(query_question_player.values_list('answer_status', flat=True)):
                query = Question.objects.filter(id=id)
                question_content = list(query.values_list('question_content', flat=True))
                QuestionPlayer.objects.filter(fk_question=question_id, fk_player=player_id).update(is_playing=True)

                result = {'id': "{}".format(int(id)), 'question_content': "{}".format(question_content[0])}
                return JsonResponse(result)
    # send_question(request)
    return JsonResponse({'id': -1, 'question_content': "error"})


@csrf_exempt
def semantic_similarity(request, word):
    query = Question.objects.all();
    questions = list(query.values_list('wiki_doc', flat=True))
    content = list(query.values_list('question_content', flat=True))
    contents = {}
    for question in questions:


    return HttpResponse(contents[1])

@csrf_exempt
def get_words(request):
    question_id = request.POST["question_id"]

    query = WordList.objects.filter(fk_question=question_id)
    words = list(query.values_list('word', flat=True))
    result = {'result': "true", 'words': words}

    return JsonResponse(result)


@csrf_exempt
def get_summary(request):
    question_id = request.POST["question_id"]
    player_id = request.POST["player_id"]

    query = QuestionPlayer.objects.filter(fk_player=player_id, fk_question=question_id, is_playing=True)
    is_playing = list(query.values_list('is_playing', flat=True))
    if len(is_playing) > 0:
        query = Question.objects.filter(id=question_id)
        answer = list(query.values_list('answer', flat=True))
        summary = CheckWord.wikipedia_summary(answer[0])
        result = {"result": summary}
        return JsonResponse(result)

    return JsonResponse({"result": "error"})


@csrf_exempt
def get_Info(request):
    question_id = request.POST["question_id"]
    player_id = request.POST["player_id"]

    query = QuestionPlayer.objects.filter(fk_player=player_id, fk_question=question_id, is_playing=True)
    is_playing = list(query.values_list('is_playing', flat=True))

    if len(is_playing) > 0:
        query = Question.objects.filter(id=question_id)
        answer = list(query.values_list('answer', flat=True))
        result = CheckWord.get_info(answer[0])
        return JsonResponse({"result": result})

    return JsonResponse({"result": "error"})


@csrf_exempt
def answer_the_question(request):
    answer = request.POST["answer"]
    question_id = request.POST["question_id"]
    player_id = request.POST["player_id"]

    if QuestionPlayer.objects.filter(fk_question=question_id, fk_player=player_id, is_playing=True):
        query = Question.objects.filter(id=question_id)
        real_answer = list(query.values_list('answer', flat=True))

        if real_answer[0] == answer:
            QuestionPlayer.objects.filter(fk_question=question_id, fk_player=player_id)\
                                   .update(answer_status=True, is_playing=False)
            result = {'result': "True", 'similarity_percent': "100"}
            return JsonResponse(result)
        else:
            seq = CheckWord.check_similarity(answer, real_answer[0])
            result = {'result': "False", 'similarity_percent': seq}
            return JsonResponse(result)


@csrf_exempt
def get_answer_two_player(request):
    player_id = request.POST["player_id"]

    ###if player playing one Question return this###
    query_isplaying = TowQuestionPlayer.objects.filter(fk_player1=player_id, is_playing=True)
    if query_isplaying:
        qid = list(query_isplaying.values_list('fk_question', flat=True))
        question_query = Question.objects.filter(id=qid[0])
        question_content = list(question_query.values_list('question_content', flat=True))
        result = {'id': "{}".format(qid[0]), 'question_content': "{}".format(question_content[0])}
        return JsonResponse(result)

    query_isplaying = TowQuestionPlayer.objects.filter(fk_player2=player_id, is_playing=True)
    if query_isplaying:
        qid = list(query_isplaying.values_list('fk_question', flat=True))
        question_query = Question.objects.filter(id=qid[0])
        question_content = list(question_query.values_list('question_content', flat=True))
        result = {'id': "{}".format(qid[0]), 'question_content': "{}".format(question_content[0])}
        return JsonResponse(result)


    ###else if player dont play one Question return this###
    question_id = list(Question.objects.all().order_by('?')[:10].values_list('id', flat=True))
    for id in question_id:
        if Player.objects.filter(id=player_id):
            query_question_player1 = TowQuestionPlayer.objects.filter(fk_question=id, fk_player1=player_id)
            query_question_player2 = TowQuestionPlayer.objects.filter(fk_question=id, fk_player2=player_id)
            if not (query_question_player1 or query_question_player2):
                query = Question.objects.filter(id=id)
                question_content = list(query.values_list('question_content', flat=True))
                player1 = get_object_or_404(Player, id=player_id[0])
                question = get_object_or_404(Question, id=id)
                player2_id = list(Player.objects.all().order_by('?')[:1].values_list('id', flat=True))
                player2 = get_object_or_404(Player, id=player2_id[0])
                TowQuestionPlayer.objects.create(fk_player1=player1, fk_player2=player2, fk_question=question, is_playing=True)

                result = {'id': "{}".format(int(id)), 'question_content': "{}".format(question_content[0])}
                return JsonResponse(result)


    # send_question(request)
    return JsonResponse({'id': -1, 'question_content': "error"})


@csrf_exempt
def wiki_test(request, word1, word2):
    page = requests.get("https://en.wikipedia.org/wiki/" + word1)
    soup = BeautifulSoup(page.content, features="html.parser")

    word_tokenized1 = []
    size = len(soup.find_all('p'))
    content = soup.find_all('p')
    for i in range(size):
        word_tokenized1.append(word_tokenize(content[i].get_text()))

    filtered_words1 = []
    for list in word_tokenized1:
        for word in list:
            if word not in stopwords.words('english'):
                if word.isalpha():
                    filtered_words1.append(word)

    most_common_words1 = (collections.Counter(filtered_words1).most_common(100))

#---------------------------------------------------------
    page = requests.get("https://en.wikipedia.org/wiki/" + word2)
    soup = BeautifulSoup(page.content, features="html.parser")

    word_tokenized2 = []
    size = len(soup.find_all('p'))
    content = soup.find_all('p')
    for i in range(size):
        word_tokenized2.append(word_tokenize(content[i].get_text()))

    filtered_words2 = []
    for list in word_tokenized2:
        for word in list:
            if word not in stopwords.words('english'):
                if word.isalpha():
                    filtered_words2.append(word)

    most_common_words2 = (collections.Counter(filtered_words2).most_common(100))

    len2 = 0
    i = 0
    x = 0
    for w, c in most_common_words2:
        len2 += c
        if w == word1:
            x = i
    i += 1
    return JsonResponse({'s': (most_common_words2[x][1] / len2) * 100})






