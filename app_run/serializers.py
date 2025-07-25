from django.contrib.auth.models import User

from rest_framework import serializers

from app_run.models import Run, AthleteInfo, Challenge, Position
from app_run.validators import validate_coordinate


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


class AthleteInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = AthleteInfo
        fields = ['user_id', 'goals', 'weight']

    @staticmethod
    def validate_weight(value):
        if value is not None:
            if value <= 0 or value >= 900:
                raise serializers.ValidationError(
                    "Weight must be greater than 0 and less than 900"
                )
        return value


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['full_name', 'athlete']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'run', 'latitude', 'longitude']

    @staticmethod
    def validate_run(value):
        if value.status != 'in_progress':
            raise serializers.ValidationError("Run must be in 'in_progress' status")
        return value

    @staticmethod
    def validate_latitude(value):
        return validate_coordinate(value)

    @staticmethod
    def validate_longitude(value):
        return validate_coordinate(value)
