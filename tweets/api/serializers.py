from rest_framework import serializers
from tweets.models import Tweet
from accounts.api.serializers import UserDisplaySerializer
from django.utils.timesince import timesince


class ParentTweetModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True) # this brings all data from user not only id
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'id',
            'likes',
        ]

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y | at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

    def get_likes(self, obj):
        return obj.liked.all().count()

class TweetModelSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(write_only=True, required=False) # pt reply
    user = UserDisplaySerializer(read_only=True) # this brings all data from user not only id
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    parent = ParentTweetModelSerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Tweet
        fields = [
            'parent_id',

            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'id',
            'parent',
            'likes',

            'reply',
        ]
        #read_only_fields = ['reply'] # hide is_reply 

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y | at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

    def get_likes(self, obj):
        return obj.liked.all().count()
