from datetime import timezone
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from customadmin.models import Designs

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    
    
    
    
    
# users actions

class PersonMeasurement(models.Model):
    measurement_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waist = models.DecimalField(max_digits=5, decimal_places=2)
    shoulder = models.DecimalField(max_digits=5, decimal_places=2)
    chest = models.DecimalField(max_digits=5, decimal_places=2)
    hips = models.DecimalField(max_digits=5, decimal_places=2)
    inseam_length = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
    design = models.ForeignKey(Designs, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.design.design_id}'s Measurements"
    
class ShippingAddress(models.Model):
    address_id= models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"Shipping Address for {self.user.username}"
    



class Order(models.Model):
    order_id= models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Designs, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ORDER_STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='processing')
    payment_status = models.BooleanField(default=False)  # Payment status field

    # Add this method to activate the order
    def activate_order(self):
        self.payment_status = True
        self.save()

    def __str__(self):
        return f"Order #{self.order_id} by {self.user.username}"
    
    
    
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=Order.ORDER_STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"Payment for Order #{self.order.order_id} by {self.user.username}"

@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, **kwargs):
    # Update the order's status when a payment is saved
    instance.order.order_status = instance.order_status
    instance.order.save()