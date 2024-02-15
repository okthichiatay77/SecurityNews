from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sign-up/', views.sign_up_view, name='sign_up'),
    path('change-password/<int:pk>/', views.change_password_view, name='change_password'),
    path('profile/', views.profile_detail_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
]