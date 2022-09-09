from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cities')

    def __str__(self) -> str:
        return self.name
