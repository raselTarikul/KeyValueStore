from django.db import models

# Create your models here.


class Storage(models.Model):
    """
    Data class
    """
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(null=True)
    ttl = models.IntegerField(default=15)
    expiration_time = models.DateTimeField(null=True)
