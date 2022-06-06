from rest_framework import serializers
from .models import Category
import datetime


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields =('id', 'code', 'title', 'parent', 'description', 'status', 'created_at', 'updated_at', 'deleted_at')

    def update(self, instance, validated_data):
        if validated_data.get('status'):
            if validated_data.get('status') == 'inactive':
                instance.deleted_at = datetime.datetime.now().date()

        instance.status = validated_data.get('status', instance.status)
        instance.code = validated_data.get('code', instance.code)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
