from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """topic user is learning about"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """return a string representation of a model"""
        return self.text
    
class Entry(models.Model):
    """something specific learned"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    # new tags field
    tags = models.CharField(max_length=200, blank=True, help_text="Separate tags with commas")

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """return a simple string representing the entry"""
        return f"{self.text[:50]}..."
