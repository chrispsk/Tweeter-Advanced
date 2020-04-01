from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#from .views import tweet_detail_view, tweet_list_view, TweetDetailView, TweetListView, tweet_create_view, tweet_update_view, delete_view
from django.views.generic import RedirectView
from .views import TweetListAPIView, TweetCreateAPIView, RetweetAPIView, LikeToggleAPIView, TweetDetailAPIView

urlpatterns = [
    # path('', RedirectView.as_view(url="/")),
    path('', TweetListAPIView.as_view(), name='listapi'), # /api/tweet/
    path('create/', TweetCreateAPIView.as_view(), name='create'),
    path('<int:pk>/retweet/', RetweetAPIView.as_view(), name='retweet'),
    path('<int:pk>/like/', LikeToggleAPIView.as_view(), name='like'),
    path('<int:pk>/', TweetDetailAPIView.as_view(), name='detail'),
    # path('<int:pk>', tweet_detail_view, name='detail'),
    # path('create/', tweet_create_view, name='create'),
    # path('<int:pk>/edit/', tweet_update_view, name='update'),
    # path('<int:pk>/delete/', delete_view, name='delete'),
    # CLASS BASED VIEWS
    # path('<int:pk>', TweetDetailView.as_view(), name='detail'),
    # path('', TweetListView.as_view(), name='list'),
]
