from django.contrib.auth.models import User
from django.db import models


class Run(models.Model):
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
