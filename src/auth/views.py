from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model   

User = get_user_model()

# Create your views here.
def login_view(request):
    print(request.method, request.POST or None)
    if request.method == "POST":
        username = request.POST.get("username") or None
        password = request.POST.get("password") or None
        user = authenticate(request, username=username, password=password)
        if all([username, password]):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                print("User authenticated and logged in.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
                print("Authentication failed.")
        else:
            messages.warning(request, "Please provide both username and password.")
    return render(request, "auth/login.html", {})

def register_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username") or None
        email = request.POST.get("email") or None
        password = request.POST.get("password") or None
        # user_exists = User.objects.filter(username__iexact=username).exists()
        # email_exists = User.objects.filter(email__iexact=email).exists()
        try:
            User.objects.create_user(username, email=email, password=password)
        except :
            pass
    template_name = "auth/register.html"  # Default template
    return render(request, template_name, {})