from django.shortcuts import render , redirect 
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from barcode_app.models import Barcode
from .forms import SignupForm , ProfileForm
from django.contrib.auth import authenticate , login ,logout
from django.db.models import Sum
from django.contrib.auth.models import User  # علشان نجيب عدد المستخدمين
from django.db.models import Count
import qrcode
from io import BytesIO
import base64
#Create your views here.

def signup(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            #------------ البروفايل اتعمل بالـ signal
            profile = user.profile
            profile.phone_namber = profile_form.cleaned_data['phone_namber']
            profile.addres = profile_form.cleaned_data['addres']
            profile.save()

            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')  

    else:
        user_form = SignupForm()
        profile_form = ProfileForm()

    return render(
        request,
        'registration/signup.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )

@never_cache
@login_required
def dashboard(request):
    barcodes = Barcode.objects.filter(user=request.user)
    all_barcode = barcodes.count()
    total_users = None
    if request.user.is_superuser:
        total_users = User.objects.count()
    
    
    # -----لو سوبر يوزر، نجيب عدد الباركودات لكل مستخدم
    users_with_barcodes = User.objects.annotate(
        barcode_count=Count('barcode')
    )


    # -------مجموع كل المسحات
    total_scans = barcodes.aggregate(total=Sum('scans'))['total'] or 0

    return render(request, "registration/dashboard.html", {
        "barcodes": barcodes,
        "all_barcode": all_barcode,
        "total_scans": total_scans,
        "total_users":total_users,
        'users_with_barcodes':users_with_barcodes
    })


def logout_view(request):
    logout(request)
    return redirect('login')