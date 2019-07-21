from django.contrib.auth.models import User
from django.db import models
class Problem(models.Model):
    text = models.TextField()
    room = models.PositiveIntegerField()
    status = models.TextField(default='Не выполнено')
    author = models.ForeignKey(User, on_delete='models.CASCAD')
    likes = models.ManyToManyField(User, related_name='like')