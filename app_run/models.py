from django.contrib.auth.models import User
from django.db import models


class Run(models.Model):

    STATUS_CHOICES = [
        ('init', 'Инициализирован'),
        ('in_progress', 'В процессе'),
        ('finished', 'Завершен'),
    ]

    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='init')
