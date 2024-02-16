from django.shortcuts import render


def index_view(request):
    context = {
        'list_news': ['1', '2', '3']
    }
    return render(request, 'home.html', context=context)
