from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import UserProfile, Account
from store.models import Cart, CartItem
from store.views import _cart_id
from orders.models import Order
import requests

# Email verification

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    if request.method == 'POST':
     form = RegistrationForm(request.POST)
     if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        phone_no = form.cleaned_data['phone_no']
        password = form.cleaned_data['password']
        username = email.split("@")[0]

        user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.phone_no = phone_no
        user.save()
        messages.success(request, 'Registration Successful!')

        # User profile creation
        profile = UserProfile()
        profile.user_id = user.id
        profile.profile_picture = 'default/default-user.png'
        profile.save()

        # Activate user account
        # current_site = get_current_site(request)
        # mail_subject = "Please activate your account."
        # message = render_to_string('useraccounts/verification_email.html', {
        #     'user': user,
        #     'domain': current_site,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': default_token_generator.make_token(user),
        # })
        # to_email = email

        # send_email = EmailMessage(mail_subject, message, to=[to_email])
        # send_email.send()
        
        return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'useraccounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Get product variations by cart ID
                    product_variations = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variations.append(list(variation))

                    # Get the cart items from user to get product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variations:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.cart_quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'Successfully logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)    
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')

    return render(request, 'useraccounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('login')

# def activate(request, uidb64, token):
#     return HttpResponse('Ok')

@login_required(login_url = 'login')
def dashboard(request):
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    order_count = orders.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'orders_count': order_count,
        'userprofile': userprofile,
    }
    return render(request, 'useraccounts/dashboard.html', context)

@login_required(login_url = 'login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'useraccounts/my_orders.html', context)

@login_required(login_url = 'login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile' : userprofile,
    }
    return render(request, 'useraccounts/edit_profile.html', context)

@login_required(login_url = 'login')
def update_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                auth.logout(request)
                messages.success(request, 'Password updated successfully!')
                return redirect('update_password')
            else:
                messages.error(request, 'Please enter valid current password.')
                return redirect('update_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('update_password')
    return render(request, 'useraccounts/update_password.html')

@login_required(login_url = 'login')
def order_detail(request, order_id):
    return render(request, 'useraccounts/order_detail.html')