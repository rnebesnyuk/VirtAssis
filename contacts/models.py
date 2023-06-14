import random
import uuid

from django.db import models
from django.urls import reverse
from django.db.models import (
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    SlugField,
    TextField,
    EmailField, 
    ImageField,
)
from django.utils.text import slugify


class Contact(Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    birthdate = DateTimeField(max_length=20, blank=True, null=True,)
    gender = CharField(max_length=6, choices=GENDER_CHOICES)
    address = TextField(blank=True, null=True, verbose_name="Address")
    photo = ImageField(upload_to="photos/%Y/%m/%d/",blank=True, null=True,)
    slug = SlugField(max_length=55, unique=True, db_index=True, verbose_name="URL")
    time_create = DateTimeField(auto_now_add=True, verbose_name="Created")
    time_update = DateTimeField(auto_now=True, verbose_name="Updated")

    def save(self, *args, **kwargs):
        full_name = f"{self.first_name} {self.last_name}"
        self.slug = slugify(full_name)
        if Contact.objects.filter(slug=self.slug):
            self.slug = f"{self.slug}_{str(uuid.uuid4().hex)}"
        super().save(*args, **kwargs)

    def update(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("contact", kwargs={"contact_slug": self.slug})

    def __str__(self):
        return self.last_name

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["id"]


class PhoneNumber(Model):
    contact = ForeignKey(Contact, on_delete=models.CASCADE, related_name='phones')
    phone = CharField(max_length=20)
    field_type = ForeignKey("DataType", on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name="Type")


    def __str__(self):
        return self.phone

    class Meta:
        ordering = ["phone"]


class Email(Model):
    contact = ForeignKey(Contact, on_delete=models.CASCADE, related_name='emails')
    email = EmailField(max_length=30)
    field_type = ForeignKey("DataType", on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name="Type")

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["email"]


class DataType(Model):
    data_type = CharField(max_length=10, db_index=True, blank=True, null=True, verbose_name='Type')

    def __str__(self):
        return self.data_type
    

class Application(Model):
    app = CharField(max_length=20, db_index=True, verbose_name='Application')
    slug = SlugField(max_length=15, unique=True, db_index=True, verbose_name='URL')


    def get_absolute_url(self):
        return reverse("application", kwargs={"app_slug": self.slug})

    def __str__(self):
        return self.app
    
    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications' 

