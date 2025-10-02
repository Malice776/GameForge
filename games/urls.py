from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Pages principales
    path('', views.HomeView.as_view(), name='home'),
    path('games/', views.GameListView.as_view(), name='game_list'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    
    # Authentification
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard et profil
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Gestion des jeux
    path('create/', views.create_game_view, name='create_game'),
    path('games/<int:pk>/edit/', views.edit_game_view, name='edit_game'),
    path('games/<int:pk>/delete/', views.delete_game_view, name='delete_game'),
    
    # Favoris
    path('favorites/', views.favorites_view, name='favorites'),
    path('games/<int:pk>/toggle-favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    
    
    # Réinitialisation de mot de passe
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
