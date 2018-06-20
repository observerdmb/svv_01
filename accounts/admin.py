from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import UserAdmin
from .models import Profile #Subscriptions

# admin.site.register(Subscriptions)
admin.site.register(Profile, UserAdmin)
admin.site.unregister(Group)