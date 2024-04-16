from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Entry(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField("date created")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)
