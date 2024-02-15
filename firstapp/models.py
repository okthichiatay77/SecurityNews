from django.db import models
from ckeditor.fields import RichTextField


class CVE(models.Model):
    data_type = models.CharField(max_length=200)
    data_version = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar_cve')
    publish_date = models.DateTimeField(blank=True)

