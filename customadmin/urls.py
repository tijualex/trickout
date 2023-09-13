from django.urls import path
from . import views

urlpatterns = [
    path('admin_index/', views.admin_index, name='admin_index'),
    
    # fabric
    path('add_fabric/', views.add_fabric, name='add_fabric'),
    path('fabric_grid/', views.fabric_grid, name='fabric_grid'),
    path('soft-delete-fabric/<int:fabric_id>/', views.soft_delete_fabric, name='soft_delete_fabric'),
    
    #top pattern
    path('add_top_pattern/', views.add_top_pattern, name='add_top_pattern'),
    path('list_top_pattern/', views.list_top_pattern, name='list_top_pattern'),
    
    #bottom pattern
    path('add_bottom_pattern/', views.add_bottom_pattern, name='add_bottom_pattern'),
    path('list_bottom_pattern/', views.list_bottom_pattern, name='list_bottom_pattern'),
    path('update_bottom_pattern/<int:bottom_pattern_id>/', views.update_bottom_pattern, name='update_bottom_pattern'),

    
    #dress type
    path('add_dress_type/', views.add_dress_type, name='add_dress_type'),
    path('list_dress_type/', views.list_dress_type, name='list_dress_type'),
    
    #neck pattern
    path('add_neck_pattern/', views.add_neck_pattern, name='add_neck_pattern'),
    path('list_neck_pattern/', views.list_neck_pattern, name='list_neck_pattern'),
    
    #sleeves pattern
    path('add_sleeves_pattern/', views.add_sleeves_pattern, name='add_sleeves_pattern'),
    path('list_sleeves_pattern/', views.list_sleeves_pattern, name='list_sleeves_pattern'),
    
    
    path('list_product/', views.list_product, name='list_product'),
    
    
]
