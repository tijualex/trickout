from django.contrib import admin
from user.models import UserProfile, PersonMeasurement,Order,ShippingAddress, Payment

admin.site.register(PersonMeasurement)
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Payment)