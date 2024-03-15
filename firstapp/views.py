import openai
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

from _common.alert_email import send_email
from _common.alert_telegram import send_message_telegram
from _common.common import reformat_form_telegram
from accounts.models import NotificationUser
from .forms import CVEForm
from .models import CVE, FollowAffected

openai_api_key = ''
openai.api_key = openai_api_key


def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )

    answer = response.choices[0].message.content.strip()
    return answer


def index_view(request):
    list_cve = CVE.objects.all()[:3]
    if request.method == 'POST' and 'message' in request.POST:
        message = request.POST['message']
        print("Question:", message)
        response = ask_openai(message)
        print("Bot Chat: ", response)
        return JsonResponse({'message': message, 'response': response})
    elif request.method == 'POST' and 'id_cve' in request.POST:
        id_cve = request.POST['id_cve']
        list_cve = CVE.objects.filter(title__contains=id_cve)

    context = {
        'list_test': [1, 2, 3],
        'list_cves': list_cve,
    }
    return render(request, 'home.html', context=context)


def list_cves_view(request):
    list_cve = CVE.objects.all()
    if request.method == 'POST' and 'search_focus' in request.POST:
        id_cve = request.POST['search_focus']
        list_cve = CVE.objects.filter(title__contains=id_cve)
    elif request.method == 'POST' and 'newest' in request.POST:
        list_cve = CVE.objects.all().order_by('-publish_date')
    elif request.method == 'POST' and 'oldest' in request.POST:
        list_cve = CVE.objects.all().order_by('publish_date')
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
            data = form.save(commit=True)
            title = request.POST['title']
            pk = data.pk
            for it in FollowAffected.objects.filter(affected_id=request.POST['affected']).all():
                info = NotificationUser.objects.get(user_id=it.user_id)
                message = reformat_form_telegram(title, pk)
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

            return HttpResponseRedirect(reverse('app:list_cves'))

    return render(request, 'firstapp/create_cves.html', {'form': form})
