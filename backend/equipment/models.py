from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=50)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)


class UploadHistory(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_equipment = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()

    def __str__(self):
        return f"Upload on {self.uploaded_at}"

    def __str__(self):
        return self.name
class UploadSummary(models.Model):
    total_equipment = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary at {self.uploaded_at}"

