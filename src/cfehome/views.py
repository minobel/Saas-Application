from django.http import HttpResponse
import pathlib
from django.shortcuts import render

from visits.models import Visit

this_dir = pathlib.Path(__file__).resolve().parent
def home_view(request, *args, **kwargs):
    template_name = "home.html"  # Default template
    return render(request, template_name, *args, **kwargs)

def about_view(request, *args, **kwargs):
    qs = Visit.objects.all()
    page_qs = Visit.objects.filter(path=request.path)
    try:
        percent = (page_qs.count() * 100.0)/ qs.count(), 
    except:
        percent = 0.0
    my_title = "Hello World!"
    html_template = "home.html"
    my_context = {
        "page_title": my_title,
        "page_visit_count": qs.count(),
        "percent": percent,
        "total_visit_count": qs.count(),
    }
    Visit.objects.create()
    return render(request, html_template, my_context)