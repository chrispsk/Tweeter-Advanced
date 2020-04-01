from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

class UserProfileManager(models.Manager):
    """ Override all() in order to fix the problem: I am followed by Myself"""
    def all(self):
        qs = self.get_queryset().all()
        # print(dir(self))
        # print(self.instance) # user
        try:
            if self.instance:
                qs = qs.exclude(user = self.instance)
        except:
            pass
        return qs


# ================== FOLLOW ============================
    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False

    def recommended(self, user, limit_to=10):
        print(user)
        profile = user.profile
        #following = profile.following.all()
        following = profile.get_following()
        # any user who I don't follow, I will recommend ordered in random manner
        qs = self.get_queryset().exclude(user__in=following).exclude(id=profile.id).order_by("?")[:limit_to]
        return qs

class UserProfile(models.Model):
    # user.profile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE) # This is Me
    # we can follow a lot of users and a lot of users can follow Me
    # user.profile.following - users I follow
    # user.followed_by - users that follow Me -- reverse relationship
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_by') # This is who I follow

    objects = UserProfileManager() # UserProfile.objects.all()
    # abc = UserProfileManager() # UserProfile.abc.all()

    def __str__(self):
        return str(self.following.all().count()) # user.profile

    def get_following(self):
        """Who I'm following exclude Myself"""
        # User.objects.all().exclude(username=self.user.username)
        return self.following.all().exclude(username=self.user.username)

# ADD SIGNAL create UserProfile after created a new user
def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    # print(instance)
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)
        # celery + redis

post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)
