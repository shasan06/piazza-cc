from rest_framework import serializers
from .models import post, person, interaction, response
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime


        
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
    class Meta:
        model = interaction
        fields =('interactionID', 'postID', 'personID', 'response_type', 'comments', 'interacTimestamp')
        read_only_fields = ('interactionID', 'interacTimestamp')

#logic 3 how to disable the response type when the current timestamp exceeds the expiration time?


class responseSerializer(serializers.ModelSerializer):
    #logic 4 ---- #to post the number of likes, dislikes, comments for a particular post
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







   



        



    
        



    

    


    
   






