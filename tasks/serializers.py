from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Task, BugReport, Note


class BaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    validators = [
            UniqueTogetherValidator(
                queryset=Task.objects.all(),
                fields=['owner', 'title'],
                message="You already have a task with this title."
            )
        ]

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Task title must be at least 3 characters long.")
        return value

class TaskSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = Task
        fields = BaseItemSerializer.Meta.fields + ['status', 'priority', 'assigned_to', 'owner']
        read_only_fields = BaseItemSerializer.Meta.read_only_fields + ['owner']



class BugReportSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = BugReport
        fields = BaseItemSerializer.Meta.fields + ['severity', 'status', 'owner', 'expected_result']
        read_only_fields = BaseItemSerializer.Meta.read_only_fields + ['owner']

class NoteSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = Note
        fields = BaseItemSerializer.Meta.fields + ['note_type', 'is_pinned', 'tags', 'owner']
        read_only_fields = BaseItemSerializer.Meta.read_only_fields + ['owner']
