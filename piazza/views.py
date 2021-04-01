import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import TweetForm
from rest_framework import viewsets
from .models import post, person, interaction
from .serializers import (
    postSerializer, 
    personSerializer, 
    interactionSerializer, 
    #responseSerializer,
    #some extra serializer
    TweetSerializer,
    TweetActionSerializer,
    TweetCreateSerializer
)
from django.views.generic import TemplateView
import requests
import json
import datetime

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

#these are class based view 
class postViewSet(viewsets.ModelViewSet):
    queryset = post.objects.all()
    serializer_class = postSerializer

class personViewSet(viewsets.ModelViewSet):
    queryset = person.objects.all()
    serializer_class = personSerializer


class interactionViewSet(viewsets.ModelViewSet):
    queryset = interaction.objects.all()
    serializer_class = interactionSerializer

#class responseViewSet(viewsets.ModelViewSet):
    #queryset = response.objects.all()
    #serializer_class = responseSerializer

#--------------
#here I am trying to do some front end using function based view
def home_view(request, *args, **kwargs):
    #print(request.user or None) #associate a user in this view
    #print(args, kwargs) no need any more
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)

@api_view(['POST']) #http method the client == POST
#@authentication_classes([SessionAuthentication]) done default
@permission_classes([IsAuthenticated])#REST API Course
def tweet_create_view(request, *args, **kwargs):
    #date = request.POST or None
    serializer = TweetCreateSerializer(data=request.POST)
    #serializer = TweetSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True):
       serializer.save(user=request.user)
       return Response(serializer.data, status=201)
    return Response({}, status=400)
       #print(obj)
       #return JsonResponse(serializer.data, status=201)#now use serializer.data instead of obj
        #serializer.save(commit=False) #no need to initialze obj here
        #obj.user = request.user
        #obj.save()

@api_view(['GET'])  
def tweet_detail_view(request, tweet_id,  *args, **kwargs):
    qs = post.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST']) 
@permission_classes([IsAuthenticated]) 
def tweet_delete_view(request, tweet_id,  *args, **kwargs):
    qs = post.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)#makesure the user is authenticated grab the permission classes
    if not qs.exists():#unauthorised
        return Response({"message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    #serializer = TweetSerializer(obj)
    return Response({"message": "Tweet removed"}, status=200)

@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: likes, disike, comments
    '''
    #print(request.POST, request.data)
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        message = data.get("message")
        qs = post.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "likes":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "dislikes":#unlike
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "comments":#retweet
            new_tweet = post.objects.create(
                    user=request.user, 
                    parent=obj,
                    message=message,
                    )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)

'''def tweet_like_toggle_view(request, tweet_id,  *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    if request.user in obj.likes.all():
        obj.likes.remove(request.user)
    else:
        obj.likes.add(request.user)
    return Response({"message": "Tweet removed"}, status=200)'''

@api_view(['GET'])  
def tweet_list_view(request, *args, **kwargs):
    qs = post.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)
    

def tweet_create_view_pure_django(request, *args, **kwargs):
    '''
    REST API Create View->DRF(Django rest framework)
    '''
    user = request.user
    if not request.user.is_authenticated:#if the user pass this block which applies that they are authenticated which the applies one can use obj.user
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    #server define
    #print(abc)
    #print("ajax", request.is_ajax())
    form = TweetForm(request.POST or None)
    #print('post data is', request.POST)
    next_url = request.POST.get("next") or None
    #print("next_url", next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        #do other form related logic
        obj.user = user #user or None # None Annon User then it will default to none
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items, no need of print ajax statement as we have this

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view_pure_django(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/ioS/Android
    return json data
    """

    qs = post.objects.all()#looping through all of the objects in the database
    #tweets_list = [{"id": x.id, "message": x.message, "likes": random.randint(0, 122)} for x in qs]#turning python obj into dictionary
    tweets_list = [x.serialize() for x in qs]#just do serialise instead of returning dict
    data = {
        "isUser": False,
       "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/ioS/Android
    return json data
    """

    data = {
        "id": tweet_id,
        #"message": obj.message,
        #"image_path": obj.image.url
    }
    status = 200
    try:
    #print(args, kwargs) used for testing 
        obj = post.objects.get(id=tweet_id)
        data['message'] = obj.message #if there is an object then add in the object
    except:
        data['message'] = "Not found"
        status = 404
        #raise Http404
    return JsonResponse(data, status=status) #json.dumps content_type='application/json'
    #return HttpResponse(f"<h1>Hello {tweet_id} - {obj.message}</h1>")
