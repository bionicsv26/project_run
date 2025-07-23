from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from app_run.filters import RunFilter
from app_run.models import Run
from app_run.serializers import RunSerializer, UserSerializer


@api_view(['GET'])
def company_details(request):
        return Response({
            'company_name': settings.COMPANY_NAME,
            'slogan': settings.SLOGAN,
            'contacts': settings.CONTACTS,
        })

class ConditionalPagination(PageNumberPagination):
    page_size = 10  # Значение по умолчанию
    page_size_query_param = 'size'
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view=None):
        # Включаем пагинацию только если указан параметр size
        if 'size' in request.query_params:
            return super().paginate_queryset(queryset, request, view)
        return None


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete')
    serializer_class = RunSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at']
    pagination_class = ConditionalPagination
    filterset_class = RunFilter


class RunStartAPIView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, pk=run_id)

        if run.status != 'init':
            return Response(
                {'error': 'Забег уже начат или завершен.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        run.status = 'in_progress'
        run.save()

        return Response(
            {'status': 'Забег начат.', 'run_id': run.id, 'current_status': run.status},
            status=status.HTTP_200_OK
        )


class RunStopAPIView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, pk=run_id)

        if run.status != 'in_progress':
            return Response(
                {'error': 'Забег еще не начат или уже завершен.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        run.status = 'finished'
        run.save()

        return Response(
            {'status': 'Забег завершен.', 'run_id': run.id, 'current_status': run.status},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']
    pagination_class = ConditionalPagination

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
