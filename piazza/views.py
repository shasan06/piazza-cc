from django.shortcuts import render
from rest_framework import viewsets
from .models import post, person, interaction, response
from .serializers import postSerializer, personSerializer, interactionSerializer, responseSerializer
from django.views.generic import TemplateView
import requests
import json
import datetime


class postViewSet(viewsets.ModelViewSet):
    queryset = post.objects.all()
    serializer_class = postSerializer

class personViewSet(viewsets.ModelViewSet):
    queryset = person.objects.all()
    serializer_class = personSerializer


class interactionViewSet(viewsets.ModelViewSet):
    queryset = interaction.objects.all()
    serializer_class = interactionSerializer

class responseViewSet(viewsets.ModelViewSet):
    queryset = response.objects.all()
    serializer_class = responseSerializer