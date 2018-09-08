from django.shortcuts import render, redirect
from .forms import UserForm, RegisterForm
from account.models import User, Product, Photo
from cart.cart import Cart
import json
from django.http import HttpResponse

# Create your views here.


def login(request):
    if request.session.get('is_login', None):
        return redirect('/home')

    if request.method == 'POST':
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']  # 从表单获取数据
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)      # 从数据库查找用户信息
                if user.password == password:
                    request.session['is_login'] = True      # 创建session
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
    request.session.flush()                          # 清空session
    return redirect('/home/')


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)  # 提交RegisterForm中的内容
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']  # 提取username的内容
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)  # 查找数据库
                if same_name_user:
                    message = '用户名已经存在！'
                    return render(request, 'register.html', locals())
                new_user = User.objects.create()  # 创建数据
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


def add_to_cart(request):
    if request.session.get('is_login', None):
        product_name = request.POST['product_name']                   # 获取目标商品
        product = Product.objects.get(product_name=product_name)
        quantity = 1                                                 # 每次添加数量为1
        cart = Cart(request)
        cart.add(product, product.price, quantity)
        resp = {'errCode': 0, "data": '', "msg": '加入购物车成功'}      # 消息返回前端
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        resp = {'errCode': 0, "data": '', "msg": '请先登录'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


def remove_from_cart(request):
    product_name = request.POST['product_name']
    product = Product.objects.get(product_name=product_name)
    cart = Cart(request)
    cart.remove(product)
    resp = {'errCode': 0, "data": '', "msg": '删除物品成功'}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def cart(request):
    if request.session.get('is_login', None):
        all = Product.objects.all()
        cart = Cart(request)
        return render(request, 'mycar.html', locals())


def allen(request):
    return render(request, 'allen.html', locals())


def introduce(request):
    return render(request, 'introduce.html', locals())


def skill(request):
    return render(request, 'skill.html', locals())

