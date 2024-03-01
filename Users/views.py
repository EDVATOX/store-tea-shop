from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User
import time
from Products.models import *


def signup(request):
    if request.user.is_authenticated:
        return redirect('store')
    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, 'این نام کاربری قبلا ثبت شده است', extra_tags='form-control')
            return render(request, 'signup.html')
        user = User(username=request.POST.get('username'))
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 == pass2 and pass2 is not None:
            if len(pass1) >= 8:
                user.set_password(pass1)
                user.save()
                username = user.username
                time.sleep(3)
                return redirect('login')
            else:
                messages.error(request, 'رمز عبور باید حداقل 8 کاراکتر باشد', extra_tags='form-control')
        else:
            messages.error(request, 'تکرار رمز عبور مظابقت ندارد', extra_tags='form-control')

    return render(request, 'signup.html',)


def login(request):
    if request.user.is_authenticated:
        return redirect('store')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        if username:
            if User.objects.filter(username=username).exists():
                user = authenticate(request, username=username, password=password)
                if user:
                    auth.login(request, user)
                    return redirect('store')
                messages.error(request, 'کاربری یافت نشد')
                return render(request, 'login.html')
            messages.error(request, 'حسابی با این نام کاربری وجود ندارد')
    return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('store')


@login_required(login_url='login')
def profile(request):
    shoppingcart_cart, temp = ShoppingCart.objects.get_or_create(user=request.user)
    items = shoppingcart_cart.shoppingcartitem_set.all()
    context = {
        'shoppingcart': shoppingcart_cart,
        'shoppingcart_items': items,
        'shoppingcart_count': items.count()
    }
    return render(request, 'cart.html', context=context)


@login_required(login_url='login')
def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get("now_password")
                new_password = form.cleaned_data.get("new_password")
                if len(new_password) < 8:
                    messages.error(request, "رمز عبور جدید حداقل باید 8 کارکتر داشته باشد")
                    return render(request, 'change_password.html', {'form': form})
                check = request.user.check_password(password)
                if check:
                    request.user.set_password(new_password)
                    request.user.save()
                    messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت')
                    return render(request, 'change_password.html', {'form': form})
                messages.error(request, "رمز عبور فعلی شما نادرست است")
                return render(request, 'change_password.html', {'form': form})
            else:
                messages.error(request,'اطلاعات مورد تایید نیست')
                return render(request, 'change_password.html',{'form':form})
        if request.method == "GET":
            form = ChangePasswordForm()
            return render(request, 'change_password.html',context={'form':form})
