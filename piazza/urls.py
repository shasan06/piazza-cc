from django.urls import path

from .views import (
    home_view,
    tweet_delete_view,
    tweet_action_view,
    tweet_detail_view,
    tweet_list_view,
    tweet_create_view,
)

'''
CLIENT
Base ENDPOINT /api/piazza/
'''

urlpatterns = [
    path('', tweet_list_view),#need to list them out
    path('action/', tweet_action_view),
    path('create/', tweet_create_view),#need create way
    path('<int:tweet_id>/', tweet_detail_view),#need actual id
    path('<int:tweet_id>/delete/', tweet_delete_view),
]

#all tweets message are in a url format 



