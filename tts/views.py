import os
import time
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import TTS
from .serializers import TTSSerializer
from gtts import gTTS


class TTSConvertAPIView(APIView):
    def post(self, request):
        serializer = TTSSerializer(data=request.data)
        if serializer.is_valid():
            tts_job = serializer.save(status='queued')

            try:
                tts_job.status = 'processing'
                tts_job.save(update_fields=['status'])

                slow = True if tts_job.speed < 1.0 else False
                tts = gTTS(text=tts_job.text, lang=tts_job.language, slow=slow)

                filename = f"tts_{tts_job.id}.mp3"
                path = os.path.join('media', 'tts_audio', filename)
                os.makedirs(os.path.dirname(path), exist_ok=True)

                start_time = time.time()
                tts.save(path)
                end_time = time.time()

                tts_job.audio_file.name = os.path.join('tts_audio', filename)
                tts_job.duration = round(end_time - start_time, 2)
                tts_job.file_size = os.path.getsize(path)
                tts_job.status = 'completed'
                tts_job.save()

            except Exception as e:
                tts_job.status = 'failed'
                tts_job.error = str(e)
                tts_job.save()

            return Response(TTSSerializer(tts_job, context={'request': request}).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TTSDetailAPIView(generics.RetrieveAPIView):
    queryset = TTS.objects.all()
    serializer_class = TTSSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class TTSAudioAPIView(APIView):
    def get(self, request, id):
        tts_job = get_object_or_404(TTS, id=id)

        if not tts_job.audio_file:
            raise Http404("Audio file not found.")

        return FileResponse(tts_job.audio_file.open(), content_type='audio/mpeg')

class TTSHistoryAPIView(generics.ListAPIView):
    queryset = TTS.objects.all().order_by('-created_at')
    serializer_class = TTSSerializer
    permission_classes = [IsAuthenticated]

