from django.db import models
from django.utils import timezone


class File(models.Model):
    objects = None
    CATEGORIES = (
        ('images', 'Images'),
        ('documents', 'Documents'),
        ('videos', 'Videos'),
        ('others', 'Others'),
    )

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    category = models.CharField(max_length=20, choices=CATEGORIES)
    upload_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
