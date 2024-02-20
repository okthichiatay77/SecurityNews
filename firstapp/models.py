from django.db import models
from ckeditor.fields import RichTextField


# from _common.common import build_url_news


class ProductsVersions(models.Model):
    version = models.CharField(max_length=200)
    status = models.CharField(max_length=100)

    def __str__(self):
        return str(self.version)


class Product(models.Model):
    name = models.CharField(max_length=100)
    version = models.ForeignKey(ProductsVersions, on_delete=models.CASCADE, related_name='product_version')

    def __str__(self):
        return str(self.name)

class Vendor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Affected(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='affected_product', blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='affected_vendor', blank=True)

    def __str__(self):
        return str(self.product)

# =====================================================================

class ReferencesTags(models.Model):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.tag_name)

class References(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    tag = models.ForeignKey(ReferencesTags, on_delete=models.CASCADE, related_name='references_tag')

    def __str__(self):
        return str(self.name)

# =====================================================================

class CvssV20(models.Model):
    version = models.CharField(max_length=200, blank=True)
    vector = models.CharField(max_length=200, blank=True)
    base_score = models.FloatField(blank=True)

    def __str__(self):
        return str(self.version)

class CvssV30(models.Model):
    version = models.CharField(max_length=200, blank=True)
    vector = models.CharField(max_length=200, blank=True)
    base_score = models.FloatField(blank=True)
    base_severity = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.version)


class CvssV31(models.Model):
    version = models.CharField(max_length=200, blank=True)
    vector = models.CharField(max_length=200, blank=True)
    base_score = models.FloatField(blank=True)
    base_severity = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.version)

class Metric(models.Model):
    format = models.CharField(max_length=200)
    cvssv20 = models.ForeignKey(CvssV20, on_delete=models.CASCADE, related_name='metric_cvss_v20')
    cvssv30 = models.ForeignKey(CvssV20, on_delete=models.CASCADE, related_name='metric_cvss_v30')
    cvssv31 = models.ForeignKey(CvssV20, on_delete=models.CASCADE, related_name='metric_cvss_v31')

    def __str__(self):
        return str(self.format)

# =====================================================================


class CVE(models.Model):
    title = models.CharField(max_length=200, blank=True)
    data_type = models.CharField(max_length=200)
    data_version = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatar_cve')
    publish_date = models.DateTimeField(blank=True)
    description = RichTextField(blank=True, null=True)
    solution = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200)
    date_reserved = models.DateTimeField(blank=True)
    date_publish = models.DateTimeField(blank=True)
    date_update = models.DateTimeField(blank=True)
    state = models.CharField(max_length=100)
    affected = models.ForeignKey(Affected, on_delete=models.CASCADE, related_name='cve_affected', blank=True)
    references = models.ForeignKey(References, on_delete=models.CASCADE, related_name='cve_reference', blank=True)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='cve_metric', blank=True)

    def __str__(self):
        return str(self.short_name)


class Favorite(models.Model):
    pass
