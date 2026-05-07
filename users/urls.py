from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('signup/', views.register, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user-profile'),
    path('users/<str:username>/', views.user_profile, name='user-profile-alt'),
    path('author/<str:username>/', views.user_profile, name='author-posts'),
    path('follow/<str:username>/', views.follow_user, name='follow-user'),
    path('notifications/', views.notifications, name='notifications'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-posts/', views.dashboard, name='my-posts'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
