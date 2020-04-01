from rest_framework import generics
from .serializers import TweetModelSerializer
from tweets.models import Tweet
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .pagination import StandardResultsPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin

class LikeToggleAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        if request.user.is_authenticated:
            is_liked = Tweet.objects.like_toggle(request.user, tweet_qs.first())
            return Response({'liked': is_liked})

        return Response({"message":"Cannot retweet again."}, status=400)



class RetweetAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        if tweet_qs.exists() and tweet_qs.count() == 1:
            if request.user.is_authenticated:
                new_tweet = Tweet.objects.retweet(request.user, tweet_qs.first())
                if new_tweet is not None:
                    data = TweetModelSerializer(new_tweet).data
                    return Response(data)

        return Response({"message":"Cannot retweet again."}, status=400)


class SearchTweetAPIView(generics.ListAPIView):
    queryset = Tweet.objects.all().order_by("-timestamp")
    serializer_class = TweetModelSerializer
    # PAGINATION
    pagination_class = StandardResultsPagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(SearchTweetAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        qs = self.queryset
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs


class TweetListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TweetModelSerializer
    # PAGINATION
    pagination_class = StandardResultsPagination


    def get_queryset(self, *args, **kwargs):
        ###### PENTRU TWEETURILE USERULUI LISTARE ############
        requested_user = self.kwargs.get("username")
        if requested_user:
            #they_follow = self.request.user.profile.get_following()
            #qs1 = Tweet.objects.filter(user__in=im_following) # tweets I'm follow
            qs = Tweet.objects.filter(user__username=requested_user).order_by("-timestamp") # my own tweets
            # combining querysets
            query = self.request.GET.get("q", None)
            if query is not None:
                qs = qs.filter(
                    Q(content__icontains=query) |
                    Q(user__username__icontains=query)
                )
            return qs
        else:
        ########################################################
            im_following = self.request.user.profile.get_following()
            # print(im_following)
            # qs = Tweet.objects.all().order_by("-timestamp")
            qs1 = Tweet.objects.filter(user__in=im_following) # tweets I'm follow
            qs2 = Tweet.objects.filter(user=self.request.user) # my own tweets
            # combining querysets
            qs = (qs1 | qs2).distinct().order_by("-timestamp")
            #print(self.request.GET)
            query = self.request.GET.get("q", None)
            if query is not None:
                qs = qs.filter(
                    Q(content__icontains=query) |
                    Q(user__username__icontains=query)
                )
            return qs


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    # don't allow anonymous user
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Create a new tweet"""
        print(serializer.validated_data.get('content'))
        serializer.save(user=self.request.user, content=escape(serializer.validated_data.get('content')))


class TweetDetailAPIView(generics.ListAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination
    # don't allow anonymous user
    #permission_classes = (permissions.AllowAny,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        tweet_id = self.kwargs.get("pk")
        qs = Tweet.objects.filter(pk=tweet_id)
        if qs.exists() and qs.count()==1:
            parent_obj = qs.first()
            qs1 = parent_obj.get_children()
            qs = (qs | qs1).distinct().extra(select={"parent_id_null":"parent_id IS NULL"})
        return qs.order_by("-parent_id_null", "-timestamp")
