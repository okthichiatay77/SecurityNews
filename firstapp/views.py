from django.shortcuts import render


def index_view(request):
    context = {
        'list_news': ['1', '2', '3']
    }
    return render(request, 'home.html', context=context)


def list_cves_view(request):

    context = {
        'list_cve': [1, 2, 3, 4]
    }
    return render(request, 'firstapp/list_cves.html', context=context)