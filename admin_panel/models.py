from django.db import models
from django.utils import timezone

# Create your models here.

class Route(models.Model):
    from_city = models.CharField(max_length=100, verbose_name="Город отправления")
    to_city = models.CharField(max_length=100, verbose_name="Город прибытия")
    departure_time = models.DateTimeField(verbose_name="Время отправления")
    arrival_time = models.DateTimeField(verbose_name="Время прибытия")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    total_seats = models.IntegerField(verbose_name="Всего мест")
    available_seats = models.IntegerField(verbose_name="Свободных мест")

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.from_city} → {self.to_city} ({self.departure_time.strftime('%d.%m.%Y %H:%M')})"

class Ticket(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='tickets', verbose_name="Маршрут")
    seat_number = models.IntegerField(verbose_name="Номер места")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")
    is_purchased = models.BooleanField(default=False, verbose_name="Куплен")

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
        ordering = ['route', 'seat_number']

    def __str__(self):
        return f"Билет {self.seat_number} на {self.route}"
