from django.shortcuts import render

def home(request):

    return render(request,'main/customer/customer_home.html',{
        'water_bills': request.user.customer_profile.water_bills.all()
    })
