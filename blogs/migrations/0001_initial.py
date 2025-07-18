# Generated by Django 5.1.5 on 2025-03-10 00:23

import django.db.models.deletion
import tinymce.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Τίτλος')),
                ('content', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Περιεχόμενο')),
                ('image', models.URLField(blank=True, max_length=1000, null=True, verbose_name='Εικόνα (URL)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ημερομηνία Δημιουργίας')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Τελευταία Ενημέρωση')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Συγγραφέας')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
