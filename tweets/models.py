from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
import re
from django.db.models.signals import post_save
from hashtags.signals import parsed_hashtags

def validate_content(value):
    content = value
    if content == "":
        raise ValidationError("Content Cannot be blank")
    return value

class TweetManager(models.Manager):
    def retweet(self, user, parent_obj):
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj
        # Make sure I cannot retweet more than once
        qs = Tweet.objects.filter(user=user, parent=og_parent).filter(reply=False)
        if qs.exists():
            return None
        obj = self.model(
            parent = og_parent,
            user = user,
            content = parent_obj.content,
        )
        obj.save()
        return obj

    def like_toggle(self, user, tweet_obj):
        if user in tweet_obj.liked.all():
            is_liked = False
            tweet_obj.liked.remove(user)
        else:
            is_liked = True
            tweet_obj.liked.add(user)
        return is_liked



class Tweet(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    # Tweets must be associated to a user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=140, validators=[validate_content])
    reply = models.BooleanField(verbose_name="Is a reply", default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')


    objects = TweetManager()

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse("tweet:detailre", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-timestamp']

    # def clean(self, *args, **kwargs):
    #     content = self.content
    #     if content == "abc":
    #         raise ValidationError("Content Cannot be ABC")
    #     return super(Tweet, self).clean(*args,**kwargs)

    # PENTRU REPLY

    def get_parent(self):
        the_parent = self
        if self.parent:
            the_parent = self.parent
        return the_parent

    def get_children(self):
        parent = self.get_parent()
        qs = Tweet.objects.filter(parent=parent)
        qs_parent = Tweet.objects.filter(pk = parent.pk)
        return (qs | qs_parent)

def tweet_save_receiver(sender, instance, created, *args, **kwargs):
    if created and not instance.parent:
        # notify a user
        user_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(user_regex, instance.content)

        # send notification to user here TODO

        # Save multiple hashtags
        hash_tag = r'#(?P<hashtag>[\w\d-]+)'
        hashtags = re.findall(hash_tag, instance.content)
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)
        # send hashtag signal

post_save.connect(tweet_save_receiver, sender=Tweet)
