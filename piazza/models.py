from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime



# Create your models here.
#this is a post table, the post table will depend on person table(with personID as a Foreign Key)
class post(models.Model):
    postID = models.AutoField(primary_key=True)#Please note that by default django creates a primary key even if not declared in the model. But I declared it
    title = models.CharField(max_length=100, null=True)
    #Topic--politics, health, sports and tech
    politics = models.BooleanField()
    health = models.BooleanField()
    sports = models.BooleanField()
    tech = models.BooleanField()
    message = models.CharField(max_length=240, blank=True)#an empty message will be acceptable by the system blank = True
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    expireDateTime = models.DateTimeField(null=True)
    #i could have used person instead of user in the below argument but person model is the second schema so it threw an error 'of using person before assignment' so i used User instead as it is an inbuilt django user
    personID = models.ForeignKey(User, on_delete=models.CASCADE)
    #status_list = [('Live', 'Live'), ('Expired', 'Expired')]
    #status = models.CharField(max_length=100, choices=status_list, default='Live')
    #status_option = [('Live','Live'), ('Expired','Expired')]
    #status = models.CharField(max_length=100, choices=status_option, default='Live')
    #personID = models.ForeignKey(User, on_delete=models.CASCADE)
    #personID = models.ForeignKey(User, on_delete=models.CASCADE)
    #Please note i do not need to declare status field as above bcoz the data is not persistent so a function 
    # of status will do the task of checking the status by annotating with @property means that it will be a 
    # field of this post model but has no persistent data as status will depend on expired time
    #this status function will check if the current time exceeds the expired time then status is 'Expired' otherwise 'Live'
    @property
    def status(self):
        #expiredate = self.expireDateTime
        #if timezone.now()>self.expireDateTime:
        #if timezone.now()>datetime.strptime(expiredate):
        if timezone.now()>self.expireDateTime:
            return 'Expired'
        else:
            return 'Live'
    #this total_likes, total_dislikes and total_comments function uses an attribute of 'relate_name that is interactions' used in the interaction model below. 
    # This is done to relate a particular post likes, dislikes or comments if any to the below interaction model
    @property
    def total_likes(self):
        return self.interactions.filter(response_type='Like').count()#tell django u want the result of that join. Here count an aggregate func is used to count and filter total interactions of like 
    @property
    def total_dislikes(self):
        return self.interactions.filter(response_type='Dislike').count()# Here count an aggregate func is used to count and filter total interactions of dislike
    '''@property
    def total_comments(self):
        return self.interactions.filter(response_type='Comments').count()'''
    @property
    def total_comments(self):#exclude--opposite of filter--> if not empty string means comments. It list the total comments using count
        return self.interactions.exclude(comments='').count()
#the personId is unique and it should be in the post table as a FK(foreign key). It depends on post table as it carries a person info who made the post
class person(models.Model):
    personID = models.AutoField(primary_key=True)
    personName = models.CharField(max_length=100)


#interaction model is the response  to the post model
#this table(interacton/response) depends on both the above table that is post and person table. As it carries responses(likes, dislikes, comments) from other users to a post
class interaction(models.Model):
    interactionID = models.AutoField(primary_key=True)
    postID = models.ForeignKey("post", on_delete=models.CASCADE, related_name='interactions')#relate_name used to connect the post model on interaction model
    personID = models.ForeignKey("person", on_delete=models.CASCADE)
    response_list = [('Like', 'Like'), ('Dislike', 'Dislike'),('Comments', 'Comments')]
    response_type = models.CharField(max_length=100, choices=response_list)
    comments = models.CharField(max_length=255, blank=True)#note i used blank is true so that if any user wants to just like or dislike without giving any comments will be able to do. So the blank field of comments will be acceptable.
    interacTimestamp = models.DateTimeField(default=timezone.now)
    

#this response table is not needed as the total responses for a particular post will be computed by using a function
#class response(models.Model):
    #responseID = models.AutoField(primary_key=True)
    #no_of_like = models.IntegerField(null=True)#no. of like counts by a user
    #no_of_dislike = models.IntegerField(null=True)#no. of dislike counts by a user
    #no_of_comment = models.IntegerField(null=True)#no. of commentCount by a user
    #postID = models.ForeignKey("post", on_delete=models.CASCADE)
    #interactionID = models.ForeignKey("interaction", on_delete=models.CASCADE)


    
    

                  
