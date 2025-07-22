from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from app_run.models import Run
from app_run.serializers import RunSerializer, UserSerializer


@api_view(['GET'])
def company_details(request):
        return Response({
            'company_name': settings.COMPANY_NAME,
            'slogan': settings.SLOGAN,
            'contacts': settings.CONTACTS,
        })


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete')
    serializer_class = RunSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        type_user = self.request.query_params.get('type', '').strip().lower()
        match type_user:
            case 'coach':
                return qs.filter(is_staff=True)
            case 'athlete':
                return qs.filter(is_staff=False)
            case _:
                return qs
