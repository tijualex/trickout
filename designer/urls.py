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
    path('measurement_details/<int:design_id>/', views.measurement_details, name='measurement_details'),
    
    
    # fabric
    path('add_fabric/', views.add_fabric, name='add_fabric'),
    path('fabric_list/', views.fabric_list, name='fabric_list'),
    path('soft-delete-fabric/<int:fabric_id>/', views.soft_delete_fabric, name='soft_delete_fabric'),
    path('get-fabric-details/<int:fabric_id>/', views.get_fabric_details, name='get_fabric_details'),
    path('update-fabric/<int:fabric_id>/', views.update_fabric, name='update_fabric'),
    
    #top pattern
    path('add_top_pattern/', views.add_top_pattern, name='add_top_pattern'),
    path('list_toppattern/', views.list_toppattern, name='list_toppattern'),
    path('get-top-pattern-details/<int:pattern_id>/', views.get_top_pattern_details, name='get_top_pattern_details'),
    path('update-top-pattern/<int:pattern_id>/', views.update_top_pattern, name='update-top-pattern'),
    
    #bottom pattern
    path('add_bottom_pattern/', views.add_bottom_pattern, name='add_bottom_pattern'),
    path('list_bottompattern/', views.list_bottompattern, name='list_bottompattern'),
    path('get-bottom-pattern-details/<int:pattern_id>/', views.get_bottom_pattern_details, name='get_bottom_pattern_details'),
    path('update-bottom-pattern/<int:pattern_id>/', views.update_bottom_pattern, name='update-bottom-pattern'),



    
    #dress type
    path('add_dress_type/', views.add_dress_type, name='add_dress_type'),
    path('list_dress/', views.list_dress, name='list_dress'),
    
    #neck pattern
    path('add_neck_pattern/', views.add_neck_pattern, name='add_neck_pattern'),
    path('listneck_pattern/', views.list_neckpattern, name='list_neckpattern'),
    path('get-neck-pattern-details/<int:pattern_id>/', views.get_neck_pattern_details, name='get_neck_pattern_details'),
    path('update-neck-pattern/<int:pattern_id>/', views.update_neck_pattern, name='update-neck-pattern'),

    
    #sleeves pattern
    path('add_sleeves_pattern/', views.add_sleeves_pattern, name='add_sleeves_pattern'),
    path('list_sleevespattern/', views.list_sleevespattern, name='list_sleevespattern'),
    path('get-sleeves-pattern-details/<int:pattern_id>/', views.get_sleeves_pattern_details, name='get_sleeves_pattern_details'),
    path('update-sleeves-pattern/<int:pattern_id>/', views.update_sleeves_pattern, name='update-sleeves-pattern'),


]