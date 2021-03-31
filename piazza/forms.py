from django.conf import settings
from django import forms
from .models import post

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
#MAX_TWEET_LENGTH = 240 # instead of declaring this every time we have it in django settings and used every where as above

class TweetForm(forms.ModelForm):
    #can also declare individuals fields like below
    #message = forms.TextFeld()
    class Meta:
        model = post
        fields = ['message']

    #message will be cleaned and is not over a certain length
    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return message

