from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('road/', views.road, name='road'),
    path('tickets/', views.tickets, name='tickets'),
    path('statistics/', views.statistics, name='statistics'),
    path('settings/', views.settings, name='settings'),
    path('route/<int:pk>/', views.RouteDetailView.as_view(), name='route_detail'),
    path('contact/', views.contact, name='contact'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
] 