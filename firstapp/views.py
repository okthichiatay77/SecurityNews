from django.shortcuts import render

from .models import CVE, Affected, References, Metric

def index_view(request):
    context = {
        'list_news': ['1', '2', '3']
    }
    return render(request, 'home.html', context=context)


def list_cves_view(request):

    if request.method == 'POST':
        id_cve = request.POST['search_focus']
        list_cve = CVE.objects.filter(title__contains=id_cve)
        print(list_cve)
    else:
        list_cve = CVE.objects.all()
    context = {
        # 'list_cve': [1, 2, 3, 4],
        'list_cve': list_cve
    }
    return render(request, 'firstapp/list_cves.html', context=context)

def detail_cves_view(request, pk):
    detail_cve = CVE.objects.get(pk=pk)
    context = {
        'detail_cve': detail_cve
    }
    return render(request, 'firstapp/detail_cve.html', context=context)
