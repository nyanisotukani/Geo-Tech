from django.db import models

# Create your models here.
from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class FloodAlert(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    alert_level = models.CharField(max_length=50)
    alert_message = models.TextField()
    date_issued = models.DateTimeField(auto_now_add=True)


class WeatherEvent(models.Model):
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    precipitation = models.FloatField()
    event_type = models.CharField(max_length=50)
    risk_level = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.location} - {self.event_type} ({self.date})"