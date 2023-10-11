from django.db import models

from trickout import settings

class DressType(models.Model):
    dress_type = models.CharField(max_length=255, primary_key=True)  # Custom primary key
    image = models.ImageField(upload_to='media/')
    details = models.TextField(max_length=300, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.dress_type

class NeckPattern(models.Model):
    neck_id = models.AutoField(primary_key=True)  # Custom primary key
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/')
    details = models.TextField(max_length=300, null=True)
    dress_type = models.ForeignKey(DressType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    def soft_delete(self):
        self.is_active = False
        self.save()
    
    def __str__(self) :
        return self.name

class SleevesPattern(models.Model):
    sleeve_id = models.AutoField(primary_key=True)  # Custom primary key
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/')
    details = models.TextField(max_length=300, null=True)
    dress_type = models.ForeignKey(DressType, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    def soft_delete(self):
        self.is_active = False
        self.save()
    
    def __str__(self) :
        return self.name

class BottomPattern(models.Model):
    bottom_id = models.AutoField(primary_key=True)  # Custom primary key
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/')
    details = models.TextField(max_length=300, null=True)
    dress_type = models.ForeignKey(DressType, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    def soft_delete(self):
        self.is_active = False
        self.save()
    
    def __str__(self) :
        return self.name

class TopPattern(models.Model):
    top_id = models.AutoField(primary_key=True)  # Custom primary key
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/')
    details = models.TextField(max_length=300, null=True)
    dress_type = models.ForeignKey(DressType, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    def soft_delete(self):
        self.is_active = False
        self.save()
    
    def __str__(self) :
        return self.name
    

class Fabric(models.Model):
    fabric_id = models.AutoField(primary_key=True)  # Custom primary key
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/')
    details = models.TextField(max_length=300, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    def soft_delete(self):
        self.is_active = False
        self.save()
    
    def __str__(self) :
        return self.name

class Designs(models.Model):
    design_id = models.AutoField(primary_key=True)  # Custom primary key
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dress_type = models.ForeignKey(DressType, on_delete=models.CASCADE, default=1)
    neck_id = models.ForeignKey(NeckPattern, on_delete=models.CASCADE, default=1, related_name='neck_pattern')
    sleeve_id = models.ForeignKey(SleevesPattern, on_delete=models.CASCADE, default=1, related_name='sleeves_pattern')
    bottom_id = models.ForeignKey(BottomPattern, on_delete=models.CASCADE, default=1, related_name='bottom_pattern')
    top_id = models.ForeignKey(TopPattern, on_delete=models.CASCADE, default=1, related_name='top_pattern')
    fabric_id = models.ForeignKey(Fabric, on_delete=models.CASCADE, null=True, blank=True, related_name='fabric1')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Design {self.design_id} by {self.user.username}"
    
    
    
from django.contrib.auth.models import User
from django.db import models

class UserRole(models.Model):
    USER_ROLES = [
        ('designer', 'Designer'),
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=USER_ROLES, default='user')
    is_allocated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username