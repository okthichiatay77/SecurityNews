from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator

from . import forms
from . import models
from firstapp.models import FollowAffected
from _common.bot_chat import ask_openai

status_noti = [
	('telegram', 'Telegram'),
	('gmail', 'Gmail'),
	('all', 'All')
]


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
			create_notifi = models.NotificationUser.objects.create(user=user)
			create_profile.save()
			create_notifi.save()
			return HttpResponseRedirect(reverse('accounts:login'))

	return render(request, 'accounts/sign_up.html', {'form': form})


def notification_user_view(request):
	try:
		check_user_notifi = models.NotificationUser.objects.get(user=request.user)
		if not check_user_notifi.status:
			status = False
		else:
			status = True
	except:
		status = False
	form = forms.CreateNotification()
	data_noti = models.NotificationUser.objects.get(user_id=request.user.id)
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	elif request.method == 'POST':
		status = request.POST['status']
		email_address = request.POST['email_address']
		token_bot = request.POST['token_bot']
		chat_id = request.POST['chat_id']

		data_noti.status = status
		data_noti.email_address = email_address
		data_noti.token_bot = token_bot
		data_noti.chat_id = chat_id
		data_noti.save()

		return HttpResponseRedirect(reverse('accounts:profile'))

	context = {
		'user': request.user,
		'form': form,
		'data_noti': data_noti,
		'status_noti': status_noti,
		'status': status,
	}
	return render(request, 'accounts/notification_user.html', context=context)


@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('app:home'))


@login_required
def profile_detail_view(request):
	try:
		check_user_notifi = models.NotificationUser.objects.get(user=request.user)
		if not check_user_notifi.status:
			status = False
		else:
			status = True
	except:
		status = False
	form = forms.EditProfile()
	profile = models.UserProfile.objects.get(user=request.user)
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	elif request.method == 'POST':
		form = forms.EditProfile(request.POST or None, request.FILES, instance=profile)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(reverse('accounts:profile'))

	context = {
		'profile': profile,
		'form': form,
		'status': status,
	}
	return render(request, 'accounts/profile.html', context=context)

def list_affect_view(request, page):
	list_followed = FollowAffected.objects.filter(user=request.user)

	list_products = []
	unique_id = []
	for it in list_followed:
		if it.affected.product_id not in unique_id:
			unique_id.append(it.affected.product_id)
			list_products.append(it.affected.product)

	list_venders = []
	unique_id = []
	for it in list_followed:
		if it.affected.vendor_id not in unique_id:
			unique_id.append(it.affected.vendor_id)
			list_venders.append(it.affected.vendor)

	if request.method == 'POST' and 'vender_filter' in request.POST:
		vender = request.POST['vender_filter']
		print(vender)
		list_followed = list_followed.filter(affected__vendor__name__contains=vender)
	elif request.method == 'POST' and 'product_filter' in request.POST:
		product_filter = request.POST['product_filter']
		list_followed = list_followed.filter(affected__product__name__contains=product_filter)

	paginator = Paginator(list_followed, 15)
	page_obj = paginator.get_page(page)
	data = page_obj.object_list

	context = {
		"page": {
			'prev': page_obj.number - 1 if page_obj.number - 1 > 0 else 1,
			'current': page_obj.number,
			'next': page_obj.number + 1 if page_obj.number + 1 < paginator.num_pages else paginator.num_pages,
		},
		'list_fllowed': data,
		'list_venders': list_venders,
		'list_products': list_products,
		'len_page': paginator.num_pages,
	}
	return render(request, 'accounts/list_affect.html', context=context)


@login_required
def change_password_view(request, pk):
	try:
		check_user_notifi = models.NotificationUser.objects.get(user=request.user)
		if not check_user_notifi.status:
			status = False
		else:
			status = True
	except:
		status = False
	mess = ""
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	elif request.method == 'POST' and 'your_news_password1' in request.POST:
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
		'mess': mess,
		'status': status,
	}
	return render(request, 'accounts/change_password.html', context=context)
