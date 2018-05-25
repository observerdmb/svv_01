from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import UserAdmin
from .models import Profile


admin.site.register(Profile, UserAdmin)
admin.site.unregister(Group)