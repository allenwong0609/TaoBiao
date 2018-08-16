from django.shortcuts import render, redirect
from .forms import UserForm, RegisterForm
from account.models import User, Product, Photo


# Create your views here.


def login(request):
    if request.session.get('is_login', None):
        return redirect('/home')

    if request.method == 'POST':
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/home/')
                else:
                    message = '密码错误!'
            except:
                message = '用户不存在'
        return render(request, 'login.html', locals())
    else:
        login_form = UserForm()
        return render(request, 'login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/home/')


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在！'
                    return render(request, 'register.html', locals())
                new_user = User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.save()
                return redirect('/login/')
    else:
        register_form = RegisterForm()
        return render(request, 'register.html', locals())


def home(request):
    products = Product.objects.all()
    photos = Photo.objects.all()
    return render(request, 'home.html', locals())