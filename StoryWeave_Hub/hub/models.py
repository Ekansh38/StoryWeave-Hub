from django.contrib.auth.models import User
from django.db import models


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    text_data = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.text_data[:20]}..."


class MainStory(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"Main Story: {str(self.branch)}"


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote For: {str(self.branch)} By {str(self.user)}"
