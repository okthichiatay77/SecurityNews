from django.db import models
from django.contrib.auth.models import User, AbstractUser


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
	# avatar_profile = models.ImageField(upload_to='avatar_profile', blank=True)
	dob = models.CharField(blank=True, max_length=50)
	phone_number = models.CharField(max_length=20, blank=True)
	full_name = models.CharField(max_length=40, blank=True)
	email_profile = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return str(self.user.username)


class NotificationUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_notification')
	status = models.CharField(max_length=200, blank=True)
	email_address = models.EmailField(blank=True)
	token_bot = models.CharField(max_length=50, blank=True)
	chat_id = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return str(self.user.username)
