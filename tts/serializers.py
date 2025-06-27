from rest_framework import serializers
from .models import TTS


class TTSSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()

    class Meta:
        model = TTS
        fields = ['id', 'status', 'text', 'language', 'speed', 'duration', 'file_size', 'audio_url', 'created_at', 'updated_at', 'error']
        read_only_fields = ['id', 'status', 'duration', 'file_size', 'audio_url', 'created_at', 'updated_at', 'error']

    def get_audio_url(self, obj):
        if obj.audio_file:
            return obj.audio_file.url
        return None