from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CVE)
admin.site.register(models.Metric)
admin.site.register(models.CvssV31)
admin.site.register(models.CvssV30)
admin.site.register(models.CvssV20)
admin.site.register(models.References)
admin.site.register(models.Affected)
admin.site.register(models.Vendor)
admin.site.register(models.Version)
admin.site.register(models.Product)
admin.site.register(models.ProductsVersions)
admin.site.register(models.FollowAffected)
