from django.contrib.auth.models import User
from django.db import models

from app_run.validators import validate_coordinate


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


class AthleteInfo(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='athlete_info'
    )
    goals = models.TextField(blank=True, default='')
    weight = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Athletes Info'

    def __str__(self):
        return f"Athlete info for {self.user.username}"


class Challenge(models.Model):
    full_name = models.CharField(max_length=250)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['full_name', 'athlete']


class Position(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    latitude = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        validators=[validate_coordinate],
        help_text="Широта: от -90.0000 до 90.0000"
    )
    longitude = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        validators=[validate_coordinate],
        help_text="Долгота: от -90.0000 до 90.0000"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"
