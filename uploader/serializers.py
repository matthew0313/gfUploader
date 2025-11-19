from rest_framework import serializers
from .models import SaveFile
class SaveFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveFile
        fields = ['username', 'gameID', 'fileName', 'saveData']