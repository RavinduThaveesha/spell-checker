from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='checker-home'),
    path('pusher', views.pusher, name='pusher'),
    path('api/check/', views.check, name='checker'),
    path('api/dictionary/', views.dictionary, name='dictionary')
]
