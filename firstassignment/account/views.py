from django.shortcuts import render

def signup(request):

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        print("New User:", name, email, password)

    return render(request, "account/signup.html")
