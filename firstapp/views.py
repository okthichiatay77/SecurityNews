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
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	elif request.method == 'POST' and 'id_cve' in request.POST:
		id_cve = request.POST['id_cve']
		list_cve = CVE.objects.filter(cve_id__contains=id_cve)

	context = {
		'list_test': [1, 2, 3],
		'list_cves': list_cve,
		'status': status,
	}
	return render(request, 'home.html', context=context)


def list_cves_view(request, page):
	try:
		check_user_notifi = NotificationUser.objects.get(user=request.user)
		if not check_user_notifi.status:
			status = False
		else:
			status = True
	except:
		status = False

	list_cve = CVE.objects.all()
	list_years = []
	for it in list_cve:
		if it.year in list_years:
			continue
		list_years.append(it.year)

	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	elif request.method == 'POST' and 'search_focus' in request.POST:
		id_cve = request.POST['search_focus']
		list_cve = CVE.objects.filter(cve_id__contains=id_cve)
	elif request.method == 'POST' and 'newest' in request.POST:
		list_cve = CVE.objects.all().order_by('-date_publish')
	elif request.method == 'POST' and 'oldest' in request.POST:
		list_cve = CVE.objects.all().order_by('date_publish')
	elif request.method == 'POST' and 'filter_year' in request.POST:
		list_cve = CVE.objects.filter(year=request.POST['filter_year'])

	per_page = request.GET.get("per_page", 15)
	paginator = Paginator(list_cve, per_page)
	page_obj = paginator.get_page(page)

	data = page_obj.object_list

	context = {
		"page": {
			'current': page_obj.number,
			'has_next': page_obj.has_next(),
			'has_previous': page_obj.has_previous(),
		},
		'paginator': paginator,
		'list_cve': data,
		'list_years': list_years,
		'status': status,
	}
	return render(request, 'firstapp/list_cves.html', context=context)


def detail_cves_view(request, pk):
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
		affected = Affected.objects.filter(cve_id=detail_cve.id)
		print("xxx", affected)
		for it in affected:
			print("OBJECT->", it)
	except:
		affected = None

	try:
		reference = References.objects.get(cve=detail_cve)
	except:
		reference = None

	try:
		metric = Metric.objects.get(cve=detail_cve)
	except:
		metric = None

	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	elif request.method == 'POST' and 'follow_affect' in request.POST:
		affect_id = request.POST['follow_affect']
		if affect_id == "null":
			msg = "CVE not have affected! Please create affected for this CVE"
		else:
			followed = True
			for aff in affected:
				try:
					check = FollowAffected.objects.get(user=request.user, affected_id=aff.id)
				except:
					check = None

				if not check:
					follow_aff = FollowAffected.objects.create(user=request.user, affected_id=aff.id)
					follow_aff.save()
					followed = False
			if followed is True:
				msg = 'You had follow this Affeted'
			else:
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
	if request.method == 'POST' and 'message' in request.POST:
		message = request.POST['message']
		response = ask_openai(message)

		return JsonResponse({'message': message, 'response': response})
	elif request.method == 'POST':
		form = AffectedForm(request.POST)
		if form.is_valid():
			_data = form.save(commit=True)
			title_cve = _data.cve.cve_id
			pk_cve = _data.cve.pk
			for it in FollowAffected.objects.filter(
					affected__product_id=_data.product.id, affected__vendor_id=_data.vendor.id).all():
				info = NotificationUser.objects.get(user_id=it.user_id)
				message = reformat_form_telegram(title_cve, pk_cve)
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

