from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from . import forms
from . import models


def login_view(request):
	form = AuthenticationForm()
	msg = ""
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')

			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('app:home'))
			else:
				msg = "Tên tài khoản hoặc mật khẩu của bạn đăng nhập không chính xác!"
		else:
			msg = "Tên tài khoản hoặc mật khẩu của bạn đăng nhập không chính xác!"
	context = {
		'form': form,
		'msg': msg
	}
	return render(request, 'accounts/login.html', context=context)


def sign_up_view(request):
	form = forms.CreateNewUser()
	if request.method == 'POST':
		form = forms.CreateNewUser(request.POST)
		if form.is_valid():
			user = form.save()
			create_profile = models.UserProfile.objects.create(user=user)
			create_profile.save()
			return HttpResponseRedirect(reverse('accounts:login'))

	return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('app:home'))


@login_required
def profile_detail_view(request):
	form = forms.EditProfile()
	profile = models.UserProfile.objects.get(user=request.user)
	if request.method == 'POST':
		form = forms.EditProfile(request.POST or None, request.FILES, instance=profile)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(reverse('accounts:profile'))

	context = {
		'profile': profile,
		'form': form,
	}
	return render(request, 'accounts/profile.html', context=context)


@login_required
def edit_profile_view(request):
	form = forms.EditProfile()
	profile = models.UserProfile.objects.get(user=request.user)
	if request.method == 'POST':
		form = forms.EditProfile(request.POST or None, request.FILES, instance=profile)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(reverse('accounts:profile'))

	context = {
		'form': form
	}
	return render(request, 'accounts/edit_profile.html', context=context)


@login_required
def change_password_view(request, pk):
	mess = ""
	if request.method == 'POST' and 'your_news_password1' in request.POST:
		cur_user = models.User.objects.get(pk=pk)
		old_pass = request.POST['old_password']
		new_password = request.POST['your_news_password1']
		new_password_conf = request.POST['your_news_password2']
		print("--check", cur_user.check_password(old_pass))
		if not cur_user.check_password(old_pass):
			mess = 'Bạn nhập mật khẩu cũ không đúng, vui lòng nhập lại!'
		elif new_password != new_password_conf:
			mess = "Mật khẩu mới bạn nhập không trùng nhau, vui lòng thử lại!!"
		else:
			cur_user.set_password(new_password)
			cur_user.save()
			mess = "Bạn đã thay đổi mật khẩu thành công!"
			return HttpResponseRedirect(reverse('app:home'))
	context = {
		'mess': mess
	}
	return render(request, 'accounts/change_password.html', context=context)
