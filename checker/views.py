from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from checker.spellchecker import SpellChecker
import json


def home(request):
    return render(request, 'checker/home.html')


@api_view(['POST'])
def check(request):
    text = request.POST.get("text", "")
    s = SpellChecker()
    result = s.check(text)
    return JsonResponse(result, safe=False)


@api_view(['GET'])
def dictionary(request):
    text = request.GET.get("query", "")
    with open('checker/dictionary.json', 'r') as f:
        data = json.load(f)
        dictionary = data['unigram']

    return JsonResponse(dictionary, safe=False)


def pusher(request):
    return render(request, 'checker/pusher.html')
