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
    address_line1=models.CharField(max_length=255,)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"Shipping Address for {self.user.username}"
    



from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'

    class OrderStatusChoices(models.TextChoices):
        PROCESSING = 'processing', 'Processing'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'

    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Designs, on_delete=models.CASCADE)
    designer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='designer_orders',default=2)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address_id = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, default=1)
    razorpay_order_id = models.CharField(max_length=255, null=True)
    payment_id = models.CharField(max_length=255, null=True)
    order_status = models.CharField(max_length=20, choices=OrderStatusChoices.choices, default=OrderStatusChoices.PROCESSING)
    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)

    # Add this method to activate the order
    def activate_order(self):
        self.payment_status = Order.PaymentStatusChoices.SUCCESSFUL
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
    id=models.AutoField(primary_key=True,default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # ForeignKey to the User model
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE,default=1)  # Razorpay Order ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount in INR
    currency = models.CharField(max_length=3, default='INR')  # Currency code
    payment_status = models.BooleanField(max_length=20, default=False)  # Payment status (e.g., 'success', 'pending', 'failed')
    payment_date = models.DateTimeField(auto_now_add=True)  # Date and time of payment
    # Add more fields as needed, such as product, etc.

    def __str__(self):
        return f"Payment ID: {self.id}, Order ID: {self.order_id}"


    
    
# billing
class BillingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # If you want to associate the billing details with a user
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    apartment_suite_unit = models.CharField(max_length=255, blank=True, null=True)  # Optional field
    town_city = models.CharField(max_length=255)
    postcode_zip = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Billing Details"
    
    
    
    
