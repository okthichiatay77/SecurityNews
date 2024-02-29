from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from .models import CVE


class CVEForm(forms.ModelForm):
	class Meta:
		model = CVE
		fields = '__all__'

		widgets = {
			'description': RichTextField(config_name='default')
		}
