from django.urls import path
from . import views

urlpatterns = [
    path('admin_index/', views.admin_index, name='admin_index'),
    
    # fabric
    path('fabric_grid/', views.fabric_grid, name='fabric_grid'),
    #top pattern
    path('list_top_pattern/', views.list_top_pattern, name='list_top_pattern'),

    
    #bottom pattern
    path('list_bottom_pattern/', views.list_bottom_pattern, name='list_bottom_pattern'),



    
    #dress type
    path('list_dress_type/', views.list_dress_type, name='list_dress_type'),
    
    #neck pattern
    path('list_neck_pattern/', views.list_neck_pattern, name='list_neck_pattern'),

    
    #sleeves pattern
    path('list_sleeves_pattern/', views.list_sleeves_pattern, name='list_sleeves_pattern'),

    
    
    # designs view
    path('users_design/', views.users_design, name='users_design'),
    path('measurement_display/<int:design_id>/', views.measurement_display, name='measurement_display'),
    path('show_user_designs/<int:user_id>/', views.show_user_designs, name='show_user_designs'),
    
    
    
    # orders
    path('order_list/', views.order_list, name='order_list'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    
    
    
    # users details
    path('list-users/', views.list_users, name='list_users'),
    
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    # path('show-user-designs/<int:user_id>/', views.show_user_designs, name='show_user_designs'),
    
    
    # designer details
    path('create_designer/', views.create_designer, name='create_designer'),
    path('designers/', views.list_designers, name='list_designers'),
    path('activate_designer/<int:user_id>/', views.activate_designer, name='activate_designer'),
    path('deactivate_designer/<int:user_id>/', views.deactivate_designer, name='deactivate_designer'),
    
    
    
    # charts
    path('get_orders_last_7_days/', views.get_orders_last_7_days, name='get_orders_last_7_days'),
    path('get_order_status_counts/', views.get_order_status_counts, name='get_order_status_counts'),
    
]
