from django.db import models

from trickout import settings

class DressType(models.Model):
    dress_type = models.CharField(max_length=255, primary_key=True)  # Custom primary key
    image = models.ImageField(upload_to='dresses/')
    details = models.TextField(max_length=300, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.dress_type

class NeckPattern(models.Model):
    custom_id = models.AutoField(primary_key=True)  # Custom primary key
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='neck_patterns/')
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
    custom_id = models.AutoField(primary_key=True)  # Custom primary key
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sleeves_patterns/')
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
    custom_id = models.AutoField(primary_key=True)  # Custom primary key
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='bottom_patterns/')
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
    custom_id = models.AutoField(primary_key=True)  # Custom primary key
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='top_patterns/')
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
    custom_id = models.AutoField(primary_key=True)  # Custom primary key
    name = models.CharField(max_length=255)
    fabric_image = models.ImageField(upload_to='media/fabrics/')
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
    neck_pattern = models.ForeignKey(NeckPattern, on_delete=models.CASCADE, default=1, related_name='neck_pattern')
    sleeves_pattern = models.ForeignKey(SleevesPattern, on_delete=models.CASCADE, default=1, related_name='sleeves_pattern')
    bottom_pattern = models.ForeignKey(BottomPattern, on_delete=models.CASCADE, default=1, related_name='bottom_pattern')
    top_pattern = models.ForeignKey(TopPattern, on_delete=models.CASCADE, related_name='top_pattern')
    fabric1 = models.ForeignKey(Fabric, on_delete=models.CASCADE, null=True, blank=True, related_name='fabric1')
    is_active = models.BooleanField(default=True)
    
    def __int__(self) :
        return self.design_id