from django.urls import path
from .views import TTSConvertAPIView, TTSDetailAPIView, TTSAudioAPIView, TTSHistoryAPIView


urlpatterns = [
    path('convert/', TTSConvertAPIView.as_view(), name='tts-convert'),
    path('<uuid:id>/', TTSDetailAPIView.as_view(), name='tts-detail'),
    path('<uuid:id>/audio/', TTSAudioAPIView.as_view(), name='download-audio'),
    path('history/', TTSHistoryAPIView.as_view(), name='tts-history'),
]