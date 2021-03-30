from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime



# Create your models here.
#this is a post table, the post table will depend on owner table(with ownerID as a Foreign Key)
class post(models.Model):
    postID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True)
    #Topic--politics, health, sports and tech
    politics = models.BooleanField()
    health = models.BooleanField()
    sports = models.BooleanField()
    tech = models.BooleanField()
    message = models.CharField(max_length=240)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    expireDateTime = models.DateTimeField(null=True)
    #status_list = [('Live', 'Live'), ('Expired', 'Expired')]
    #status = models.CharField(max_length=100, choices=status_list, default='Live')
    status_option = [('Live','Live'), ('Expired','Expired')]
    status = models.CharField(max_length=100, choices=status_option, default='Live')
    personID = models.ForeignKey(User, on_delete=models.CASCADE)
    

#the personId is unique and it should be in the post table as a FK(foreign key)
class person(models.Model):
    personID = models.AutoField(primary_key=True)
    personName = models.CharField(max_length=100)


#response table to the post table
#this table(interacton/response) depends on both the above table that is post and owner table
class interaction(models.Model):
    interactionID = models.AutoField(primary_key=True)
    postID = models.ForeignKey("post", on_delete=models.CASCADE)
    personID = models.ForeignKey("person", on_delete=models.CASCADE)
    response_list = [('Like', 'Like'), ('Dislike', 'Dislike'),('Comments', 'Comments')]
    response_type = models.CharField(max_length=100, choices=response_list)
    comments = models.CharField(max_length=600)
    interacTimestamp = models.DateTimeField(default=timezone.now)
    

class response(models.Model):
    #responseID = models.AutoField(primary_key=True)
    no_of_like = models.IntegerField(null=True)#no. of like counts by a user
    no_of_dislike = models.IntegerField(null=True)#no. of dislike counts by a user
    no_of_comment = models.IntegerField(null=True)#no. of commentCount by a user
    postID = models.ForeignKey("post", on_delete=models.CASCADE)
    interactionID = models.ForeignKey("interaction", on_delete=models.CASCADE)


    
    

                  
