# Generated by Django 4.2.9 on 2024-02-15 02:59

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CVE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_type', models.CharField(max_length=200)),
                ('data_version', models.CharField(max_length=100)),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('avatar', models.ImageField(upload_to='avatar_cve')),
                ('publish_date', models.DateTimeField(blank=True)),
            ],
        ),
    ]