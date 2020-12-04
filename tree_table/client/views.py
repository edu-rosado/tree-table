from django.shortcuts import render


def react_view(request):
    return render(request, "index.html")
