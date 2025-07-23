from django.contrib.auth.models import User

from rest_framework import serializers

from app_run.models import Run


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name')


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserNestedSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished']

    @staticmethod
    def get_type(obj):
        return 'coach' if obj.is_staff else 'athlete'

    @staticmethod
    def get_runs_finished(obj):
        if hasattr(obj, 'finished_runs_count'):
            return obj.finished_runs_count
        return obj.run_set.filter(status='finished').count()

