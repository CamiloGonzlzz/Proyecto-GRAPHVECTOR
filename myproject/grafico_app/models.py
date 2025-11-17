# models.py
from django.db import models
from django.contrib.auth.models import User

class Function3D(models.Model):
    name = models.CharField(max_length=100)
    equation = models.TextField()  # ej: "z = x**2 + y**2"
    parameters = models.JSONField(default=dict)  # parámetros ajustables
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
