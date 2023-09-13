from django.contrib import admin
from user.models import UserProfile, User, PersonMeasurement

admin.site.register(User)
admin.site.register(PersonMeasurement)
admin.site.register(UserProfile)