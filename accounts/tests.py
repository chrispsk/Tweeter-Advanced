from django.test import TestCase
from .models import UserProfile
from django.contrib.auth import get_user_model

###################### TESTING SIGNALS ##################
# Make sure UserProfile is created

User = get_user_model()

class UserProfileTest(TestCase):
    def setUp(self):
        self.username = "some_user"
        new_user = User.objects.create(username=self.username)

    def test_profile_created(self):
        username = self.username
        self.assertTrue(UserProfile.objects.filter(user__username=self.username).exists())
        self.assertTrue(UserProfile.objects.filter(user__username=self.username).count()==1)

# create a existent user
    def test_new_user(self):
        new_user = User.objects.create(username=self.username + "abc")
