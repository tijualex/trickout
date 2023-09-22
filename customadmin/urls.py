from django.urls import path
from . import views

urlpatterns = [
    path('admin_index/', views.admin_index, name='admin_index'),
    
    # fabric
    path('add_fabric/', views.add_fabric, name='add_fabric'),
    path('fabric_grid/', views.fabric_grid, name='fabric_grid'),
    path('soft-delete-fabric/<int:fabric_id>/', views.soft_delete_fabric, name='soft_delete_fabric'),
    path('get-fabric-details/<int:fabric_id>/', views.get_fabric_details, name='get_fabric_details'),
    path('update-fabric/<int:fabric_id>/', views.update_fabric, name='update_fabric'),
    
    #top pattern
    path('add_top_pattern/', views.add_top_pattern, name='add_top_pattern'),
    path('list_top_pattern/', views.list_top_pattern, name='list_top_pattern'),
    path('get-top-pattern-details/<int:pattern_id>/', views.get_top_pattern_details, name='get_top_pattern_details'),
    path('update-top-pattern/<int:pattern_id>/', views.update_top_pattern, name='update-top-pattern'),
    
    #bottom pattern
    path('add_bottom_pattern/', views.add_bottom_pattern, name='add_bottom_pattern'),
    path('list_bottom_pattern/', views.list_bottom_pattern, name='list_bottom_pattern'),
    path('get-bottom-pattern-details/<int:pattern_id>/', views.get_bottom_pattern_details, name='get_bottom_pattern_details'),
    path('update-bottom-pattern/<int:pattern_id>/', views.update_bottom_pattern, name='update-bottom-pattern'),



    
    #dress type
    path('add_dress_type/', views.add_dress_type, name='add_dress_type'),
    path('list_dress_type/', views.list_dress_type, name='list_dress_type'),
    
    #neck pattern
    path('add_neck_pattern/', views.add_neck_pattern, name='add_neck_pattern'),
    path('list_neck_pattern/', views.list_neck_pattern, name='list_neck_pattern'),
    path('get-neck-pattern-details/<int:pattern_id>/', views.get_neck_pattern_details, name='get_neck_pattern_details'),
    path('update-neck-pattern/<int:pattern_id>/', views.update_neck_pattern, name='update-neck-pattern'),

    
    #sleeves pattern
    path('add_sleeves_pattern/', views.add_sleeves_pattern, name='add_sleeves_pattern'),
    path('list_sleeves_pattern/', views.list_sleeves_pattern, name='list_sleeves_pattern'),
    path('get-sleeves-pattern-details/<int:pattern_id>/', views.get_sleeves_pattern_details, name='get_sleeves_pattern_details'),
    path('update-sleeves-pattern/<int:pattern_id>/', views.update_sleeves_pattern, name='update-sleeves-pattern'),

    
    
    # designs view
    path('users_design/', views.users_design, name='users_design'),
    path('measurement_display/<int:measurement_id>/', views.measurement_display, name='measurement_display'),
    path('show_user_designs/<int:user_id>/', views.show_user_designs, name='show_user_designs'),
    
    
    
    
    
        # users details
    path('list-users/', views.list_users, name='list_users'),
    # path('show-user-designs/<int:user_id>/', views.show_user_designs, name='show_user_designs'),
]
