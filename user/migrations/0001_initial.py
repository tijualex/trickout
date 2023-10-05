# Generated by Django 4.2.4 on 2023-09-29 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customadmin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_status', models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=20)),
                ('payment_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('recipient_name', models.CharField(max_length=255)),
                ('address_line1', models.CharField(max_length=255)),
                ('street_address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonMeasurement',
            fields=[
                ('measurement_id', models.AutoField(primary_key=True, serialize=False)),
                ('waist', models.DecimalField(decimal_places=2, max_digits=5)),
                ('shoulder', models.DecimalField(decimal_places=2, max_digits=5)),
                ('chest', models.DecimalField(decimal_places=2, max_digits=5)),
                ('hips', models.DecimalField(decimal_places=2, max_digits=5)),
                ('inseam_length', models.DecimalField(decimal_places=2, default=19.0, max_digits=5)),
                ('design', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customadmin.designs')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(default=1, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='INR', max_length=3)),
                ('payment_status', models.BooleanField(default=False, max_length=20)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('order_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.order')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.shippingaddress'),
        ),
        migrations.AddField(
            model_name='order',
            name='design',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.designs'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BillingDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('street_address', models.CharField(max_length=255)),
                ('apartment_suite_unit', models.CharField(blank=True, max_length=255, null=True)),
                ('town_city', models.CharField(max_length=255)),
                ('postcode_zip', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
