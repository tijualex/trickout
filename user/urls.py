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
    
    #mesurement
    path('measurement/', views.measurement, name='measurement'),
    path('measurement_sub/', views.measurement_sub, name='measurement_sub'),
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
    
    path('dress/<int:dress_type_id>/', views.dress_detail, name='dress_detail'),
]
