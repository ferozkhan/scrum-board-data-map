
from __future__ import unicode_literals
from rest_framework.reverse import reverse
from rest_framework import serializers
from .models import Sprint, Task

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField('get_full_name', read_only=True)
    links = serializers.SerializerMethodField('get_links')

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', )

    def get_links(self, obj):
        request = self.context['request']

        return {
            'self': reverse('user-detail', kwargs={'pk': obj.pk}, request=request),
        }


class SprintSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField('get_links')

    class Meta:
        model = Sprint
        fields = ('id', 'name', 'description', 'end', )

    def get_links(self, obj):
        request = self.context['request']

        return {
            'self': reverse('sprint-detail', kwargs={'pk': obj.pk}, request=request),
        }


class TaskSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField('get_links')
    status_display = serializers.SerializerMethodField('get_status_display')
    assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, required=False)

    class Meta:
        model = Task
        field = ('id', 'name', 'description', 'sprint', 'status', 'order', 'assigned', 'started', 'due', 'completed')

    def get_status_display(self, obj):
        return obj.get_status_display() if obj else None

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse('task-detail', kwargs={'pk': obj.pk}, request=request),
            'sprint': None,
            'assigned': None
        }
        if obj.sprint_id:
            links['sprint'] = reverse('sprint-detail', kwargs={'pk': obj.sprint_id}, request=request)
        if obj.assigned_id:
            links['assigned'] = reverse('user-detail', kwargs={'pk': obj.assigned_id}, request=request)
        return links
