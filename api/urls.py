"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path #url()
from rest_framework.routers import DefaultRouter
from piazza.views import (
    postViewSet, 
    personViewSet, 
    interactionViewSet, 
    #responseViewSet,
    home_view,
    tweet_delete_view,
    tweet_action_view,
    tweet_detail_view,
    tweet_list_view,
    tweet_create_view,
)


router = DefaultRouter()
router.register('post', postViewSet)
router.register('person', personViewSet)
router.register('interaction', interactionViewSet)
#router.register('response', responseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('authentication/', include('users.urls')),
    path('v1/', include(router.urls)),
    #front-end view url i.e end points given below
    path('', home_view),
    path('create-tweet', tweet_create_view),
    path('piazza', tweet_list_view),
    path('piazza/<int:tweet_id>', tweet_detail_view),
    path('api/piazza/', include('piazza.urls')),

]







