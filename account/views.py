from django.shortcuts import render,redirect, get_object_or_404
from .models import Category, Product, Cart, CartItem
from .forms import Register,Login
from django.contrib import messages
from .models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'account/home.html', {'categories': categories, 'products': products})

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    products = category.products.all()
    return render(request, 'account/category_detail.html', {'category': category, 'products': products})


def register(request):
    form = Register()
    if request.method == 'POST':
        form=Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if confirm_password == password:
                User.objects.create(username=username, email=email, phone_number=phone_number,password=make_password(password))
                return redirect('login')
        else:
            print("invalid",form.errors)
    return render(request, 'user/register.html',{'form':form})


def login_fun(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username_email = form.cleaned_data['username']
            print("username",username_email)
            password = form.cleaned_data['password']
            user = User.objects.get(Q(username=username_email)| Q(email=username_email))
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials, please try again.')
    else:
        form = Login()

    return render(request, 'user/login.html', {'form': form})


def logout_fun(request):
    logout(request)
    return redirect('home')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()
    total_price = cart.get_total_price()

    return render(request, 'account/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('view_cart')