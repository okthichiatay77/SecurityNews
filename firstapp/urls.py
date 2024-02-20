from django.urls import path
from .views import index_view, list_cves_view, detail_cves_view


app_name = 'app'


urlpatterns = [
    path('', index_view, name='home'),
    path('list-cve/', list_cves_view, name='list_cves'),
    path('detail-cve/<int:pk>/', detail_cves_view, name='detail_cves')
]
