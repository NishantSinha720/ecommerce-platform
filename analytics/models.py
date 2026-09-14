from django.db import models

class AnalyticsSnapshot(models.Model):
    metric_name = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=18, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
