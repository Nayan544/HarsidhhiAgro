from django.shortcuts import render,redirect, get_object_or_404
from .models import Category, Product, Cart, CartItem ,Order, OrderItem
from .forms import Register,Login,VendorForm,ProductReviewForm
from django.contrib import messages
from .models import User,Vendor,Slider
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    sliders = Slider.objects.all()
    products = Product.objects.all().order_by('id')[:5]
    return render(request, 'account/home.html', {'sliders': sliders, 'products': products})


def product(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'account/product.html', {'categories': categories, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    
    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductReviewForm()

    return render(request, "account/product_detail.html", {
        'product': product,
        'reviews': reviews,
        'form': form
    })


def product_list(request, category_id=None):
    categories = Category.objects.all()
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    return render(request, 'account/product.html', {
        'categories': categories,
        'products': products,
        'selected_category': category_id
    })

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
    print ('remove from cart',cart_item)
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


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderItem

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or not cart.cart_items.exists():
        return redirect("cart")  # Redirect to cart if empty

    if request.method == "POST":
        # Process the order (your existing order creation logic)
        order = Order.objects.create(
            user=request.user, 
            total_price=cart.get_total_price(), 
            is_completed=True
        )

        # Move cart items to order
        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.get_total_price(),
            )

        # Clear cart
        cart.cart_items.all().delete()

        return redirect("thank_you")  # Redirect to thank you page

    # Pass cart items and total price to the template
    cart_items = cart.cart_items.all()
    total_price = cart.get_total_price()

    return render(request, "account/checkout.html", {"cart_items": cart_items, "total_price": total_price})


def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor/vendor_list.html', {'vendors': vendors})

def add_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save()
            
            
            subject = "New Vendor Added"
            message = vendor.message
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ["nayandabhi544@gmail.com"]  
            
            send_mail(subject, message, from_email, recipient_list)
            
            return redirect('vendor_list')
    else:
        form = VendorForm()

    return render(request, 'vendor/add_vendor.html', {'form': form})



def profile(request):
    return render(request, 'user/profile.html')


def thank_you(request):
    return render(request, "account/thank_you.html")



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "account/order_history.html", {"orders": orders})