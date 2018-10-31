from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name='profile')
    user_name = models.CharField(max_length=50, null=True)
    profile_photo = models.ImageField(
        upload_to='images/', blank=True, default='dwf_profile.jpg')
    phone = models.IntegerField(null=True)
    email = models.CharField(max_length=50, null=True)

    # @classmethod
    # def new_user(cls):
    #     return cls.objects.last()

    @classmethod
    def create_profile(cls, user):
        cls.objects.create(user=user, user_name=user.username)

    def save_profile(self, current_user):
        self.user = current_user
        self.save()

    def __str__(self):
        return self.user_name
