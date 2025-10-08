from rest_framework import serializers
from .models import Vacancy, VacancyApplication

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'
        read_only_fields = ['posted_at', 'updated_at']

class VacancyApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyApplication
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
