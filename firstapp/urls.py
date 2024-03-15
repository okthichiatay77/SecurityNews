from django.urls import path
from .views import index_view, list_cves_view, detail_cves_view, create_affrected_view, \
	tele_notifi_view, gmail_notifi_view

app_name = 'app'

urlpatterns = [
	path('', index_view, name='home'),
	path('list-cve/<int:page>/', list_cves_view, name='list_cves'),
	path('detail-cve/<int:pk>/', detail_cves_view, name='detail_cves'),
	path('create-affected/', create_affrected_view, name='create_effected'),
	path('telegram-notification/', tele_notifi_view, name='tele_noti'),
	path('gmail-notification/', gmail_notifi_view, name='gmail_noti'),
]
