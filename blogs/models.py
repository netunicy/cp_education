from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Τίτλος")
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, verbose_name="Συγγραφέας")
    content = HTMLField(null=True,blank=True,verbose_name="Περιεχόμενο")
    image = models.URLField(max_length=1000, null=True, blank=True, verbose_name="Εικόνα (URL)")  # URL Εικόνας
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ημερομηνία Δημιουργίας")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Τελευταία Ενημέρωση")

    class Meta:
        ordering = ['-created_at']  # Πρόσφατα άρθρα πρώτα
    
    def __str__(self):
        return self.title + '|' + str(self.author).title()
