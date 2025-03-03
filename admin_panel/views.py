from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Route, Ticket
from datetime import datetime
from django.utils import timezone
from django.db.models import Count, Sum
import pytz

# Create your views here.

class DashboardView(LoginRequiredMixin, ListView):
    model = Route
    template_name = 'dashboard.html'
    context_object_name = 'routes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.now().strftime("%d.%m.%Y %H:%M")
        return context

class RouteDetailView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = 'route_detail.html'
    context_object_name = 'route'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.filter(route=self.object)
        return context

@login_required
def dashboard(request):
    # Устанавливаем часовой пояс Алматы
    almaty_tz = pytz.timezone('Asia/Almaty')
    current_date = timezone.localtime(timezone.now(), almaty_tz)
    
    # Получаем статистику
    total_routes = Route.objects.count()
    active_routes = Route.objects.filter(departure_time__gte=current_date).count()
    sold_tickets = Ticket.objects.filter(is_purchased=True).count()
    
    # Считаем общую выручку
    total_revenue = 0
    purchased_tickets = Ticket.objects.filter(is_purchased=True).select_related('route')
    for ticket in purchased_tickets:
        total_revenue += ticket.route.price
    
    # Получаем последние маршруты
    recent_routes = Route.objects.filter(departure_time__gte=current_date).order_by('departure_time')[:5]
    
    context = {
        'current_date': current_date,
        'total_routes': total_routes,
        'active_routes': active_routes,
        'sold_tickets': sold_tickets,
        'total_revenue': total_revenue,
        'recent_routes': recent_routes
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def road(request):
    current_date = timezone.now()
    routes = Route.objects.all().order_by('departure_time')
    return render(request, 'road.html', {
        'current_date': current_date,
        'routes': routes
    })

@login_required
def tickets(request):
    current_date = timezone.now()
    return render(request, 'tickets.html', {'current_date': current_date})

@login_required
def statistics(request):
    current_date = timezone.now()
    return render(request, 'statistics.html', {'current_date': current_date})

@login_required
def settings(request):
    current_date = timezone.now()
    return render(request, 'settings.html', {'current_date': current_date})

def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
