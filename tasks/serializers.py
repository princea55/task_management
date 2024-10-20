# tasks/serializers.py

from rest_framework import serializers

from .models import Task, User, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'assigned_to', 'created_by',
                  'comments']

    def validate(self, data):
        assigned_to = data.get('assigned_to')
        if assigned_to and assigned_to.role == 'admin':
            raise serializers.ValidationError("Tasks cannot be assigned to Admin users.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user

        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'tasks']
