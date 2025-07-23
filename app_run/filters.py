from django.contrib.auth import get_user_model

import django_filters

from app_run.models import Run

User = get_user_model()

class RunFilter(django_filters.FilterSet):
    athlete = django_filters.ModelChoiceFilter(
        field_name='athlete',
        queryset=User.objects.filter(is_superuser=False),
        label='Athlete'
    )
    status = django_filters.ChoiceFilter(
        choices=Run.STATUS_CHOICES,
        label='Status'
    )

    class Meta:
        model = Run
        fields = ['athlete', 'status']