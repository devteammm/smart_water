from django.shortcuts import render,redirect

from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout

from django.http import HttpResponse

def login(request):

	next = "/"
	if 'next' in request.GET:
		next = request.GET['next']

	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username = username,password=password)
		if user:
			auth_login(request,user)
			return redirect(next)
		else:
			return HttpResponse("Đăng nhập thất bại")
	else:
		return render(request,"sysauth/login.html",{})


def logout(request):
	next = "/"

	if 'next' in request.GET:
		next = request.GET['next']

	auth_logout(request)

	return redirect(next)
