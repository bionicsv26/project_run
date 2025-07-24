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
