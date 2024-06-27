from django.db import models

class Video(models.model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    uplooad_at = models.DateTimeField(auto_now_add=True)
