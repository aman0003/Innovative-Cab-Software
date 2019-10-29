from rest_framework import serializers
from . models import fare_prediction

class fare_predictionSerializers(serializers.ModelSerializer):
    
    model = fare_prediction
    fields = '__all__'