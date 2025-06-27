from django.db import models
import uuid


class TTS(models.Model):

    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    text = models.TextField()
    language = models.CharField(max_length=10, default='en')
    speed = models.FloatField(default=1.0)
    duration = models.FloatField(null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)
    audio_file = models.FileField(upload_to='tts_audio/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"TTSJob {self.id} - {self.status}"
