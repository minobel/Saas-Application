from django.http import HttpResponse
import pathlib
from django.shortcuts import render

from visits.models import Visit

this_dir = pathlib.Path(__file__).resolve().parent

def home_page_view(request, *args, **kwargs):
    queryset = Visit.objects.all()
    my_title = "Hello World!"
    html_template = "home.html"
    my_context = {
        "page_title": my_title,
        "page_visit_count": queryset.count(),
    }
    Visit.objects.create()
    return render(request, html_template, my_context)