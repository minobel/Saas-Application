from django.http import HttpResponse
import pathlib
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.conf import settings
from visits.models import Visit

LOGIN_URL = settings.LOGIN_URL
this_dir = pathlib.Path(__file__).resolve().parent

def home_view(request, *args, **kwargs):
    # Ekhane check kore nite hobe user login kora kina
    if request.user.is_authenticated:
        print(f"Logged in: {request.user.is_authenticated}, Name: {request.user.first_name}")
    else:
        print(f"Logged in: {request.user.is_authenticated}, User: Anonymous")
    
    template_name = "home.html"
    
    # Context pass korle template-e data dekhano shohoj hoy
    context = {
        "username": request.user.first_name if request.user.is_authenticated else "Guest"
    }
    return render(request, template_name, context)

def about_view(request, *args, **kwargs):
    qs = Visit.objects.all()
    page_qs = Visit.objects.filter(path=request.path)
    
    # Percent calculation thik kora hoyeche (tuple error bad deya hoyeche)
    try:
        total_count = qs.count()
        if total_count > 0:
            percent = (page_qs.count() * 100.0) / total_count
        else:
            percent = 0.0
    except:
        percent = 0.0
        
    my_title = "About Us"
    html_template = "home.html"
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(),
        "percent": percent,
        "total_visit_count": qs.count(),
    }
    
    # Path soho visit record create kora bhalo practice
    Visit.objects.create(path=request.path) 
    return render(request, html_template, my_context)

VALID_CODE = "abc123"
def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0
    #print( request.session.get('protected_page_allowed'), type(request.session.get('protected_page_allowed')))
    if request.method == "POST":
        user_pw_sent = request.POST.get("code") or None
        if user_pw_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed
            
    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, "protected/entry.html", {})


@login_required
def user_only_view(request, *args, **kwargs):
    return render(request, "protected/user-only.html", {})

@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
    return render(request, "protected/user-only.html", {})