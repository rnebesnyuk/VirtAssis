from django.db import models
from django.contrib.auth.models import User



class Tag(models.Model):
    objects = None
    name = models.CharField(max_length=25, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Note(models.Model):
    IMPORTANCE_CHOICES = (
        ('', 'None'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    objects = None
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=False, null=False)
    importance = models.CharField(max_length=6, choices=IMPORTANCE_CHOICES, default='')
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class NoteToTag(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
