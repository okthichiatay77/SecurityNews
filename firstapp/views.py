from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import CVE, Affected, References, Metric, FollowAffected
from accounts.models import NotificationUser
from .forms import AffectedForm

from _common.alert_email import send_email
from _common.alert_telegram import send_message_telegram
from _common.common import reformat_form_telegram
from _common.bot_chat import ask_openai


def index_view(request):
	list_cve = CVE.objects.all()[:3]
	try:
		check_user_notifi = NotificationUser.objects.get(user=request.user)
		if not check_user_notifi.status:
			status = False
		else:
			status = True
	except:
		status = False
	# chatbot
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)
		return JsonResponse({'message': message, 'response': response})
	# tìm kiếm cve
	elif request.method == 'POST' and 'id_cve' in request.POST:
		id_cve = request.POST['id_cve']
		# trả về trang list cve
		return HttpResponseRedirect(reverse('app:list_cves', kwargs={'page': "id_cve: {}".format(id_cve)}))

	context = {
		'list_test': [1, 2, 3],
		'list_cves': list_cve,
		'status': status,
	}
	return render(request, 'home.html', context=context)


def list_cves_view(request, page):
	# lấy status để check xem user đăng ký thông báo chưa
	try:
		check_user_notifi = NotificationUser.objects.get(user=request.user)
		if not check_user_notifi.status:
			status = False
		else:
			status = True
	except:
		status = False

	# check arg từ tìm kiếm của trang home
	if page.startswith("id_cve"):
		list_cve = CVE.objects.filter(cve_id__contains=page.replace("id_cve: ", ""))
	else:
		list_cve = CVE.objects.all()

	# lấy danh sách các năm của cve để show ra tìm kiếm
	list_years = []
	for it in list_cve:
		if it.year in list_years:
			continue
		list_years.append(it.year)
	list_years.sort()
	# chatbot
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	# tìm kiếm theo cve_id
	elif request.method == 'POST' and 'search_focus' in request.POST:
		id_cve = request.POST['search_focus']
		list_cve = CVE.objects.filter(cve_id__contains=id_cve)
	# sắp xếp theo ngày mới nhất
	elif request.method == 'POST' and 'newest' in request.POST:
		list_cve = CVE.objects.all().order_by('-date_publish')
	# sắp xếp theo ngày cũ nhất
	elif request.method == 'POST' and 'oldest' in request.POST:
		list_cve = CVE.objects.all().order_by('date_publish')
	# lọc theo năm cve
	elif request.method == 'POST' and 'filter_year' in request.POST:
		list_cve = CVE.objects.filter(year=request.POST['filter_year'])
	paginator = Paginator(list_cve, 15)
	page_obj = paginator.get_page(page)
	data = page_obj.object_list
	context = {
		"page": {
			'prev': page_obj.number - 1 if page_obj.number - 1 > 0 else 1,
			'current': page_obj.number,
			'next': page_obj.number + 1 if page_obj.number + 1 < paginator.num_pages else paginator.num_pages,
		},
		'len_page': paginator.num_pages,
		'list_cve': data,
		'list_years': list_years,
		'status': status,
	}
	return render(request, 'firstapp/list_cves.html', context=context)


def detail_cves_view(request, pk):
	# hàm status để kiểm tra xem người dùng đã bật thông báo tele hoặc gmail chưa
	try:
		check_user_notifi = NotificationUser.objects.get(user=request.user)
		if not check_user_notifi.status:
			status = False
		else:
			status = True
	except:
		status = False
	detail_cve = CVE.objects.get(pk=pk)
	try:
		# check xem cve hiện tại đã có affected chưa
		affected = Affected.objects.filter(cve_id=detail_cve.id)
	except:
		# nếu chưa
		affected = None

	try:
		reference = References.objects.get(cve=detail_cve)
	except:
		reference = None

	try:
		metric = Metric.objects.get(cve=detail_cve)
	except:
		metric = None

	# bot chat
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	# follow affected của cve
	elif request.method == 'POST' and 'follow_affect' in request.POST:
		affect_id = request.POST['follow_affect']
		if affect_id == "null":
			msg = "CVE not have affected! Please create affected for this CVE"
		else:
			# hàm này kiểm tra xem user đã follow
			followed = True
			# lấy tất cả affect của cve
			for aff in affected:
				try:
					# kiểm tra xem user đã follow affect chưa
					check = FollowAffected.objects.get(user=request.user, affected_id=aff.id)
				except:
					# chưa follow
					check = None
				# nếu chưa follow thì tạo bảng follow afected
				if not check:
					follow_aff = FollowAffected.objects.create(user=request.user, affected_id=aff.id)
					follow_aff.save()
					followed = False

			if followed is True:
				# nếu đã follow hết affect của cve
				msg = 'You had follow this Affeted'
			else:
				# nếu chưa gửi thông báo
				msg = "You have been tracked successfully!"
	else:
		msg = ""
	context = {
		'detail_cve': detail_cve,
		'affected': affected,
		'reference': reference,
		'metric': metric,
		'msg': msg,
		'status': status,
	}
	return render(request, 'firstapp/detail_cve.html', context=context)


def create_affrected_view(request):
	try:
		check_user_notifi = NotificationUser.objects.get(user=request.user)
		if not check_user_notifi.status:
			status = False
		else:
			status = True
	except:
		status = False
	form = AffectedForm()
	# bot chat
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	elif request.method == 'POST':
		form = AffectedForm(request.POST)
		if form.is_valid():
			# lưu affected
			_data = form.save(commit=True)
			title_cve = _data.cve.cve_id
			pk_cve = _data.cve.pk
			# Từ affected trên đã lưu lấy tất cả thông tin user đã follow affected theo pro, ven
			for it in FollowAffected.objects.filter(
					affected__product_id=_data.product.id, affected__vendor_id=_data.vendor.id).all():
				# lấy thông tin token của tele hoặc gmail
				info = NotificationUser.objects.get(user_id=it.user_id)
				message = reformat_form_telegram(title_cve, pk_cve)
				# kiểm tra đã trạng thái user muốn thông báo gì
				if info.status == 'telegram':
					# print("---- Telegram")
					send_message_telegram(message, info.token_bot, info.chat_id)
				elif info.status == 'gmail':
					# print("---- Gmail")
					send_email(message, info.email_address)
				else:
					# print("------- all")
					send_email(message, info.email_address)
					send_message_telegram(message, info.token_bot, info.chat_id)

			return HttpResponseRedirect(reverse('app:home'))

	context = {
		'form': form,
		'status': status
	}
	return render(request, 'firstapp/create_affected.html', context=context)


# view của hướng đẫn lấy token telegram
def tele_notifi_view(request):
	try:
		check_user_notifi = NotificationUser.objects.get(user=request.user)
		if not check_user_notifi.status:
			status = False
		else:
			status = True
	except:
		status = False
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	return render(request, 'telegram_notifi.html', {'status': status})


def gmail_notifi_view(request):
	try:
		check_user_notifi = NotificationUser.objects.get(user=request.user)
		if not check_user_notifi.status:
			status = False
		else:
			status = True
	except:
		status = False
	data_noti = NotificationUser.objects.get(user_id=request.user.id)
	msg = ""
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	elif request.method == 'POST':
		status = 'gmail'
		email_address = request.POST['email_notification']

		data_noti.status = status
		data_noti.email_address = email_address

		data_noti.save()
		msg = "You have successfully set up Gmail notifications"

	context = {
		'msg': msg,
		'status': status,
	}
	return render(request, 'gmail_notifi.html', context=context)

