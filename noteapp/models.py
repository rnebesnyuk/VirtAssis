from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint



class Tag(models.Model):
    objects = None
    name = models.CharField(max_length=25, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
        
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'user'],
                name='unique_tag_per_user'
            )
        ]
        ordering = ['name']


class Note(models.Model):
    IMPORTANCE_CHOICES = (
        ('', 'None'),
        ('1 - low', 'Low'),
        ('2 - medium', 'Medium'),
        ('3 - high', 'High'),
    )

    objects = None
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=False, null=False)
    importance = models.CharField(max_length=15, choices=IMPORTANCE_CHOICES, default='')
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class NoteToTag(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
