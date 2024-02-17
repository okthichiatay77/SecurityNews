from django.db import models
from ckeditor.fields import RichTextField

from _common.common import build_url_news


class Product(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True, default="")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.url = build_url_news(self.name)
        super(Product, self).save(*args, **kwargs)


class Vendor(models.Model):
    name = models.CharField(max_length=200)


class Solution(models.Model):
    value = models.CharField(max_length=200)


class Reference(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True, default="")


class CVE(models.Model):
    data_type = models.CharField(max_length=200)
    data_version = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar_cve')
    publish_date = models.DateTimeField(blank=True)

    references = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name='cve_reference')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='cve_solution')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cve_product')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='cve_vendor')
