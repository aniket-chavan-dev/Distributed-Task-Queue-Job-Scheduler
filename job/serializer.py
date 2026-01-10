from rest_framework import serializers
from .models import Job, JobResult


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id',
            'job_type',
            'payload',
            'status',
            'attempts',
            'max_attempts',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'status',
            'attempts',
            'created_at',
            'updated_at',
        ]

    def validate_payload(self, value):
        #checks only that the payload must be valid json
        if value is not None and not isinstance(value, dict):
            raise serializers.ValidationError(
                "Payload must be a valid JSON object"
            )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
    

class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResult
        fields = [
            'id',
            'job',
            'output',
            'error',
            'execution_time_ms',
            'completed_at',
        ]
        read_only_fields = [
            'id',
            'completed_at',
        ]


class JobWithResultsSerializer(JobSerializer):
    results = JobResultSerializer(many=True, read_only=True)

    class Meta(JobSerializer.Meta):
        fields = JobSerializer.Meta.fields + ['results']
