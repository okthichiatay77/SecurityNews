from django.contrib import admin
from .models import UserProfile, NotificationUser


admin.site.register(UserProfile)
admin.site.register(NotificationUser)
