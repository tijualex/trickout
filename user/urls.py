# user/urls.py
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # general
    path('accounts/', include('allauth.urls')),
    path('login_view/', views.login_view, name='login_view'),   # URL for login
    path('signup', views.signup, name='signup'),  # URL for signup
    path('', views.index, name='index'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('design/', views.design, name='design'),
    
    
    path('check-username-exists/', views.check_username_exists, name='check-username-exists'),
    
    #forgot password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #profile
    path('profile', views.profile, name='profile'),
  
    #google
    path('accounts/', include('allauth.urls')),
    
    
    
    # design
    
    path('dress_detail/<str:dress_type>/', views.dress_detail, name='dress_detail'),
    path('confirm_design', views.confirm_design, name='confirm_design'),
    path('display_selected_patterns/<str:selected_patterns>/<str:selected_pattern_id>/<str:total_price>/', views.display_selected_patterns, name='display_selected_patterns'),
    path('create_design', views.create_design, name='create_design'),
    
    # mesurement
    path('measurement/<int:design_id>/', views.measurement_view, name='measurement_view'),
    
    
    #order
    path('order_confirmation_view/<int:design_id>', views.order_confirmation_view, name='order_confirmation_view'),










]
