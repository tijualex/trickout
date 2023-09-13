from django.contrib import admin
from .models import  Fabric, TopPattern, SleevesPattern, NeckPattern,BottomPattern, DressType


admin.site.register(Fabric)
admin.site.register(TopPattern)
admin.site.register(SleevesPattern)
admin.site.register(NeckPattern)
admin.site.register(BottomPattern)
admin.site.register(DressType)