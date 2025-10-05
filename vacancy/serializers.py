from rest_framework import serializers
from .models import VacancyApplication

class VacancyApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyApplication
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
