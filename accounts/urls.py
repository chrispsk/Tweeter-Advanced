from django.urls import path, include
#from .views import UserDetailView
from .views import userdetail, userfollow #UserFollowView

urlpatterns = [
    # path('<int:pk>', UserDetailView.as_view(), name='detail'),
    path('<username>/', userdetail, name='detail'),
    path('<username>/follow/', userfollow, name='follow'),
]
