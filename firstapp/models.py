from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import User


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


class FollowAffected(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follow_affected')
	affected = models.ForeignKey(Affected, on_delete=models.CASCADE, related_name='affected_follow')

	def __str__(self):
		return str(self.user.username) + '->' + str(self.affected.product)

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
	cvssv20 = models.ForeignKey(CvssV20, on_delete=models.CASCADE, related_name='metric_cvss_v20', default=None,
								blank=True, null=True)
	cvssv30 = models.ForeignKey(CvssV20, on_delete=models.CASCADE, related_name='metric_cvss_v30', default=None,
								blank=True, null=True)
	cvssv31 = models.ForeignKey(CvssV20, on_delete=models.CASCADE, related_name='metric_cvss_v31', default=None,
								blank=True, null=True)

	def __str__(self):
		return str(self.format)


# =====================================================================


class CVE(models.Model):
	title = models.CharField(max_length=200, blank=True)
	data_type = models.CharField(max_length=200, default="")
	data_version = models.CharField(max_length=100, default="")
	avatar = models.ImageField(upload_to='avatar_cve')
	publish_date = models.DateTimeField(blank=True, default=None)
	description = RichTextField(blank=True, null=True)
	solution = models.CharField(max_length=200, default="")
	short_name = models.CharField(max_length=200, default="")
	date_reserved = models.DateTimeField(blank=True, default=None)
	date_publish = models.DateTimeField(blank=True, default=None)
	date_update = models.DateTimeField(blank=True, default=None)
	state = models.CharField(max_length=100, default="")
	affected = models.ForeignKey(Affected, on_delete=models.CASCADE, related_name='cve_affected', blank=True,
								 default=None)
	references = models.ForeignKey(References, on_delete=models.CASCADE, related_name='cve_reference', blank=True,
								   default=None)
	metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='cve_metric', blank=True, default=None)

	def __str__(self):
		return str(self.short_name)


class Favorite(models.Model):
	pass
