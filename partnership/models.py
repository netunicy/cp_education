import os
from django.db import models
from django.contrib.auth.models import User
from pathlib import Path
from tinymce.models import HTMLField
BASE_DIR = Path(__file__).resolve().parent.parent

class T_C_Partnership(models.Model):
    title=models.CharField(max_length=1000,default='T_C')
    content=HTMLField(null=True,blank=True)
    
    class Meta:
        verbose_name_plural = 'Terms and Conditions'
        
    def __str__(self):
        t_c='Terms and Conditions'
        return t_c

from django.db import models

class PartnerProfile(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Όνομα", blank=False, null=False)
    last_name = models.CharField(max_length=50, verbose_name="Επώνυμο", blank=False, null=False)
    address = models.TextField(verbose_name="Διεύθυνση Διαμονής", blank=False, null=False)
    country = models.CharField(max_length=50, verbose_name="Χώρα", blank=False, null=False)
    postal_code = models.CharField(max_length=10, verbose_name="Ταχυδρομικός Κώδικας", blank=False, null=False)
    email = models.EmailField(verbose_name="Email", blank=False, null=False)
    phone = models.CharField(max_length=15, verbose_name="Τηλέφωνο", blank=False, null=False)
    degree_title = models.CharField(max_length=100, verbose_name="Τίτλος Σπουδών", blank=False, null=False)
    iban = models.CharField(max_length=34, verbose_name="IBAN", blank=False, null=False)

    def __str__(self):
        return self.first_name,self.last_name
