from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('sign-up/', views.sign_up_view, name='sign_up'),
	path('change-password/<int:pk>/', views.change_password_view, name='change_password'),
	path('profile/', views.profile_detail_view, name='profile'),
	path('list-affect/', views.list_affect_view, name='list_affect'),
	path('notification/', views.notification_user_view, name='notification'),
]
