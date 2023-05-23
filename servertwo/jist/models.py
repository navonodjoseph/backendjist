from django.db import models

# Create your models here.
class Audio(models.Model):
    audio_file = models.FileField(upload_to='audio/%Y/%m/%d/')
    filename = models.CharField(max_length=255, blank=True)
    transcribe = models.TextField(blank=True)

    def __str__(self):
        return self.audio_file.name
    
# Add second model here for transcription 