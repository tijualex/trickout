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
    
    path('dress_type_selection/', views.dress_type_selection, name='dress_type_selection'),
    path('fabric_selection/', views.fabric_selection, name='fabric_selection'),
    
    
    # top pattern
    path('top-pattern-selection/', views.top_pattern_selection, name='top_pattern_selection_all'),
    path('dress-type/<str:dress_type_id>/top-pattern-selection/', views.top_pattern_for_dress_type, name='top_pattern_for_dress_type'),

    
    # neck pattern
    path('neck-pattern-selection/', views.neck_pattern_selection, name='neck_pattern_selection_all'),
    path('dress-type/<str:dress_type_id>/neck-pattern-selection/', views.neck_pattern_for_dress_type, name='neck_pattern_selection'),
    
    
    #sleeves pattern
    path('sleeves-pattern-selection/', views.sleeves_pattern_selection, name='sleeves_pattern_selection_all'),
    path('dress-type/<str:dress_type_id>/sleeves-pattern-selection/', views.sleeves_pattern_for_dress_type, name='sleeves_pattern_selection'),


    #top pattern
    path('bottom-pattern-selection/', views.bottom_pattern_selection, name='bottom_pattern_selection_all'),
    path('dress-type/<str:dress_type_id>/bottom-pattern-selection/', views.bottom_pattern_for_dress_type, name='bottom_pattern_selection'),
    
    
    #dress detail view
    path('dress/detail/<int:pk>/', views.DressDetailView.as_view(), name='dress_detail')
]
