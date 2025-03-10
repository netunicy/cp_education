from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class accept_t_c(models.Model):
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    accept_terms = models.BooleanField(default='True')
class UserActivation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=40)
    activated = models.BooleanField(default=False)

