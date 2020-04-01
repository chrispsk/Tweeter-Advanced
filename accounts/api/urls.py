from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#from .views import tweet_detail_view, tweet_list_view, TweetDetailView, TweetListView, tweet_create_view, tweet_update_view, delete_view
from django.views.generic import RedirectView
from tweets.api.views import TweetListAPIView

urlpatterns = [
    path('<username>/tweet/', TweetListAPIView.as_view(), name='list'), # /api/tweet/
]
