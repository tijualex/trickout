from django.urls import  path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
   #designer
    path('index_designer/',views.index_designer, name='index_designer'),
    path('view_patterns/',views.view_patterns, name='view_patterns'),
    path('orders/',views.order_list, name='orders'),
    path('shipping_address_details/<int:order_id>/', views.shipping_address_details, name='shipping_address_details'),
        path('design/<int:design_id>/', views.design_details, name='design_details'),

    # URL pattern for displaying measurement details
    path('measurement/<int:measurement_id>/', views.measurement_details, name='measurement_details'),
    

    

]
