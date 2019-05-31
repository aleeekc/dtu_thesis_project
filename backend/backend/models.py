from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser


class Key(models.Model):
    key = models.CharField(max_length=1000)
    owner = models.CharField(max_length=1000)
    meant_for = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name_plural = "Keys"


class Folder(models.Model):
    uid = models.CharField(max_length=1000, default=uuid4().__str__().replace("-", ""))
    owner = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.uid

    class Meta:
        verbose_name_plural = "Folders"


class File(models.Model):
    uid = models.CharField(max_length=1000, default=uuid4().__str__().replace("-", ""))
    owner = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.uid

    class Meta:
        verbose_name_plural = "Files"


class Link(models.Model):
    uid = models.CharField(max_length=1000, default=uuid4().__str__().replace("-", ""))
    owner = models.CharField(max_length=1000)
    # name = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return self.uid

    class Meta:
        verbose_name_plural = "Links"


class UserDetails(models.Model):
    uid = models.CharField(max_length=150)
    userAlias = models.EmailField(blank=True)
    friends = models.EmailField(blank=True)

    def __str__(self):
        return self.uid

    class Meta:
        verbose_name_plural = "User Details"


