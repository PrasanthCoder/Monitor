# serializers.py

from rest_framework import serializers
from .models import UserStock


class UserStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStock
        fields = ['stock']
