from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from .models import CVE, Affected, References, Metric, FollowAffected
from accounts.models import NotificationUser
from .forms import CVEForm

from _common.alert_email import send_email
from _common.alert_telegram import send_message_telegram

def index_view(request):
	list_cve = CVE.objects.all()[:3]
	if request.method == 'POST':
		id_cve = request.POST['id_cve']
		list_cve = CVE.objects.filter(title__contains=id_cve)

	context = {
		'list_test': [1, 2, 3],
		'list_news': list_cve,
	}
	return render(request, 'home.html', context=context)


def list_cves_view(request):
	if request.method == 'POST':
		id_cve = request.POST['search_focus']
		list_cve = CVE.objects.filter(title__contains=id_cve)
	else:
		list_cve = CVE.objects.all()
	context = {
		# 'list_cve': [1, 2, 3, 4],
		'list_cve': list_cve
	}
	return render(request, 'firstapp/list_cves.html', context=context)


def detail_cves_view(request, pk):
	detail_cve = CVE.objects.get(pk=pk)
	if request.method == 'POST':
		try:
			check = FollowAffected.objects.get(user=request.user, affected_id=request.POST['follow_affect'])
		except:
			check = None
		if check:
			msg = 'You had follow this Affeted'
		else:
			follow_aff = FollowAffected.objects.create(user=request.user, affected_id=request.POST['follow_affect'])
			follow_aff.save()
			msg = "You have been tracked successfully!"
	else:
		msg = ""

	context = {
		'detail_cve': detail_cve,
		'msg': msg,
	}
	return render(request, 'firstapp/detail_cve.html', context=context)


def create_cves_view(request):
	form = CVEForm()
	if request.method == 'POST':
		form = CVEForm(request.POST or None, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			title = request.POST['title']
			for it in FollowAffected.objects.filter(affected_id=request.POST['affected']).all():
				info = NotificationUser.objects.get(user_id=it.user_id)
				# send_email(info.email_address, title)
				send_message_telegram(title, info.token_bot, info.chat_id)

			return HttpResponseRedirect(reverse('app:list_cves'))

	return render(request, 'firstapp/create_cves.html', {'form': form})

