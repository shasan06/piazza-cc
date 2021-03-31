from django.conf import settings
from rest_framework import serializers
from .models import post, person, interaction, response
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Count


# some values initialised in the settings of the api
MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS


class postSerializer(serializers.ModelSerializer):
    def validate(self, exptime):#logic1 for expiration time delay for 7 hours so the post can stay up to 7 hours
        expireDateTime = datetime.strftime(
            timezone.now() + timedelta(hours=7), '%Y-%m-%d %H:%M:%S')
        exptime['expireDateTime'] = expireDateTime
        return exptime

    def status_validate(self, s):#logic2 for status that will expire after the expiration time (7 hours)
        if self.timestamp > self.expireDateTime:#if the current time greater than the expiration time then the status should change from default(live) to expired
            status = 'Expired'
        s['status'] = status
        return s
    
    class Meta:
        model = post
        fields =('postID', 'title', 'politics', 'health', 'sports', 'tech', 'message', 'image', 'timestamp', 'expireDateTime',
        'status', 'personID')
        read_only_fields = ('postID', 'timestamp', 'expireDateTime', 'status')



class personSerializer(serializers.ModelSerializer):
    class Meta:
        model = person
        fields =('personID', 'personName')
        #read_only_fields = ('personID') why this not working
        


class interactionSerializer(serializers.ModelSerializer):
    #use agrregate function 'count' for total count
    '''@property
    def total_count(self):
        return interaction.published.annotate(
            total_comments = Count('comments')
        )'''
    class Meta:
        model = interaction
        fields =('interactionID', 'postID', 'personID', 'response_type', 'comments', 'interacTimestamp')
        read_only_fields = ('interactionID', 'interacTimestamp')

#logic 3 how to disable the response type when the current timestamp exceeds the expiration time?


class responseSerializer(serializers.ModelSerializer):
    #logic 4 ---- #to post the number of likes, dislikes, comments for a particular post, i tried aggregate function above
    

    '''def validate1(self, response):
        actionresponse = response['postInteractionID'].actions
        if actionresponse == 'Like':
            response['no_of_like'] +=1
        if actionresponse == 'Dislike':
            response['no_of_dislike'] +=1   
        if actionresponse == 'comment':
            response['no_of_dislike'] +=1  
        return  response'''

    class Meta:
        model = response
        fields = ('no_of_like', 'no_of_dislike',
                  'no_of_comment', 'postID', 'interactionID')
        read_only_fields = ('no_of_like', 'no_of_dislike',
                  'no_of_comment', 'postID', 'interactionID')

#------------------
#some of the extra serializers for the function based view
#basically i am trying to build a part of the post model in the front end
#another serializer for tweet actions
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    message = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()# "Like"->"like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value


class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = post
        fields = ['postID', 'title', 'politics', 'health', 'sports', 'tech', 'message', 'image', 'timestamp', 'expireDateTime',
        'status', 'personID']
    #the thing which is not the same is the clean and validate. the actual value that is being passed into that field
    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_content(self, value):# message to value and forms to serializers are changed
        if len(value) > MAX_TWEET_LENGTH: #max_.. is imported  now from settings django.conf
            raise serializers.ValidationError("This tweet is too long")
        return value
    

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    #message = serializers.SerializerMethodField(read_only=True)
    #is_comment = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = post
        fields = ['postID', 'title', 'politics', 'health', 'sports', 'tech', 'message', 'image', 'timestamp', 'expireDateTime',
        'status', 'personID']
    #the thing which is not the same is the clean and validate. the actual value that is being passed into that field
    def get_likes(self, obj):
        return obj.likes.count()
    
    '''def get_message(self, obj):
        message = obj.message#by default we will use the message from the object itself
        if obj.is_comment:
            message = obj.parent.message
        return message'''
    





   



        



    
        



    

    


    
   






