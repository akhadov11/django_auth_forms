from django.urls import path

from core import views

urlpatterns = [
    path('phone/', views.get_phone, name='phone'),
    path('auth/<int:case>/<str:phone>/', views.authenticate, name='auth'),
]
