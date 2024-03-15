from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import User


# from _common.common import build_url_news


class CVE(models.Model):
	cve_id = models.CharField(max_length=200, blank=True, default="")
	data_type = models.CharField(max_length=200, default="")
	data_version = models.CharField(max_length=100, default="")
	description = RichTextField(blank=True, null=True)
	solution = models.CharField(max_length=200, default="")
	year = models.IntegerField(blank=True, default=None)
	date_reserved = models.DateTimeField(blank=True, default=None)
	date_publish = models.DateTimeField(blank=True, default=None)
	date_update = models.DateTimeField(blank=True, default=None)
	state = models.CharField(max_length=100, default="")

	def __str__(self):
		return str(self.cve_id)


class Version(models.Model):
	version = models.CharField(max_length=3005, blank=True)
	status = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return str(self.version)


class Product(models.Model):
	name = models.CharField(max_length=3005, blank=True, null=True)

	def __str__(self):
		return str(self.name)


class Vendor(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return str(self.name)


class ProductsVersions(models.Model):
	version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='productsversion_version')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productsversion_product')

	def __str__(self):
		return str(self.version)


class Affected(models.Model):
	cve = models.ForeignKey(CVE, on_delete=models.CASCADE, related_name='affected_cve', blank=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='affected_product', blank=True)
	vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='affected_vendor', blank=True)

	def __str__(self):
		return "{} -> {} -> {}".format(self.cve, self.product, self.vendor)


class FollowAffected(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follow_affected')
	affected = models.ForeignKey(Affected, on_delete=models.CASCADE, related_name='affected_follow')

	def __str__(self):
		return "{} -> {} -> {}".format(self.user.username, self.affected.product, self.affected.vendor)

# =====================================================================


class References(models.Model):
	cve = models.ForeignKey(CVE, on_delete=models.CASCADE, related_name='references_cve', blank=True)
	url = models.CharField(max_length=1000, blank=True, default=None, null=True)

	def __str__(self):
		return str(self.url)


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
	cve = models.ForeignKey(CVE, on_delete=models.CASCADE, related_name='metric_cve', blank=True)
	cvssv20 = models.ForeignKey(CvssV20, on_delete=models.CASCADE, related_name='metric_cvss_v20', default=None,
								blank=True, null=True)
	cvssv30 = models.ForeignKey(CvssV30, on_delete=models.CASCADE, related_name='metric_cvss_v30', default=None,
								blank=True, null=True)
	cvssv31 = models.ForeignKey(CvssV31, on_delete=models.CASCADE, related_name='metric_cvss_v31', default=None,
								blank=True, null=True)

	def __str__(self):
		return str(self.cve)


# =====================================================================


class Favorite(models.Model):
	pass
