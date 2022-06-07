from rest_framework import serializers, exceptions
from .models import Category
import datetime


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields =('id', 'code', 'title', 'parent', 'description', 'status', 'created_at', 'updated_at', 'deleted_at')

    def validate_code(self, data):
        '''validate code length'''
        if len(data) < 2 or len(data) > 10:
            msg = ('The code must be between 2 and 10 characters.')
            raise exceptions.ValidationError(msg)
        return data

    def validate_title(self, data):
        '''validate title length'''
        if len(data) < 2 or len(data) > 10:
            msg = ('The title must be between 2 and 10 characters.')
            raise exceptions.ValidationError(msg)
        return data

    def validate_description(self, data):
        '''validate description length'''
        if len(data) < 10 or len(data) > 500:
            msg = ('The description must be between 10 and 500 characters.')
            raise exceptions.ValidationError(msg)
        return data

    def validate_parent_branches(self, parent, instance=None):
        '''check if a category already has 3 branches'''
        error = False

        if instance:
            if Category.objects.filter(parent=parent).exclude(id=instance.id).count() >= 3:
                error = True
        else:
            if Category.objects.filter(parent=parent).count() >= 3:
                error = True

        if error:
            msg = ('The parent category already has 3 branches.')
            raise exceptions.ValidationError(msg)

    def create(self, validated_data):
        if validated_data.get('parent'):
            self.validate_parent_branches(validated_data.get('parent'))
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):

        '''check status '''
        if validated_data.get('status'):
            if validated_data.get('status') == 'inactive':
                instance.deleted_at = datetime.datetime.now().date()

        if validated_data.get('parent'):
            self.validate_parent_branches(validated_data.get('parent'), instance)

        instance.status = validated_data.get('status', instance.status)
        instance.code = validated_data.get('code', instance.code)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.parent = validated_data.get('parent', instance.parent)
        instance.save()
        return instance
