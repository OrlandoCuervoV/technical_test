from rest_framework import viewsets, status, filters
from categories.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('id')