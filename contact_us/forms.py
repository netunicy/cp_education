from django import forms
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, required=True, label="Name")
    surname = forms.CharField(max_length=200, required=True, label="Surname")
    email = forms.EmailField(required=True, label="Email Address")
    phone = forms.CharField(max_length=50, required=True, label="Phone Number")
    subject = forms.CharField(max_length=100, required=True, label="Subject")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message")
    captcha = CaptchaField(label="Type the latters")