from django.shortcuts import render

from .models import CVE

def index_view(request):
    context = {
        'list_news': ['1', '2', '3']
    }
    return render(request, 'home.html', context=context)


def list_cves_view(request):

    if request.method == 'POST':


        id_cve = request.POST['search_focus']
        list_cve = CVE.objects.filter(content__contains=id_cve)
    else:
        list_cve = CVE.objects.all()
    context = {
        'list_cve': [1, 2, 3, 4],
        # 'list_cve': list_cve
    }
    return render(request, 'firstapp/list_cves.html', context=context)