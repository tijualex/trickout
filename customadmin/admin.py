from django.contrib import admin
from .models import  Fabric, TopPattern, SleevesPattern, NeckPattern,BottomPattern, DressType,Designs, UserRole


admin.site.register(Fabric)
admin.site.register(TopPattern)
admin.site.register(SleevesPattern)
admin.site.register(NeckPattern)
admin.site.register(BottomPattern)
admin.site.register(DressType)
admin.site.register(Designs)
admin.site.register(UserRole)