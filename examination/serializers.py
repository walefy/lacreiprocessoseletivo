from rest_framework import serializers
from .models import Examination
from professional.serializers import ProfessionalSerializer


class ExaminationSerializer(serializers.ModelSerializer):
    professional = ProfessionalSerializer()

    class Meta:
        model = Examination
        fields = '__all__'


class ExaminationCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = '__all__'

