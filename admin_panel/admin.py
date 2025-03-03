from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Route, Ticket

# Настройка админ-сайта
admin.site.site_header = "BusBook Administration"
admin.site.site_title = "BusBook Admin Portal"
admin.site.index_title = "Welcome to BusBook Admin Portal"

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('from_city', 'to_city', 'departure_time', 'arrival_time', 'price', 'available_seats')
    list_filter = ('from_city', 'to_city', 'departure_time')
    search_fields = ('from_city', 'to_city')
    ordering = ('departure_time',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('route', 'seat_number', 'is_purchased', 'purchase_date')
    list_filter = ('is_purchased', 'route', 'purchase_date')
    search_fields = ('route__from_city', 'route__to_city')
    ordering = ('-purchase_date',)
