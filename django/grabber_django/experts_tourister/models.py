from django.db import models

# Create your models here.
#http://experts.tourister.ru/germany/busines
STATUSES = (
        (0, 'New'),
        (1, 'Complete'),
        (2, 'Reject'),
    )

class Profile(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255,blank=True)
    email = models.EmailField(max_length=255,blank=True)
    url_profile = models.URLField(blank=True, unique=True)
    status = models.IntegerField(choices=STATUSES, default=0)
    