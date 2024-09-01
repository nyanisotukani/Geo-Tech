from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('map_dashboard/', views.map_dashboard, name='map_dashboard'),
    path('reports/', views.reports, name='reports'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('alerts/', views.alerts, name='alerts'),
    path('chat/', views.chat_view, name='chat_view'),
     path('monitor/<str:location>/', views.monitor_location, name='monitor_location'),
]
 