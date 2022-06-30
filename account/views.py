from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm, EditProfileForm

# Create your views here.
from .models import UserBase
from .token import account_activation_token


@login_required
def dashboard(request):
    """ Dashboard"""

    if request.method == 'POST':
        # Edit user profile
        user_form = EditProfileForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()

    else:
        user_form = EditProfileForm(instance=request.user)
    return render(request, 'account/user/dashboard.html', {'user_form': user_form})


@login_required
def delete_user(request):
    """
    Delete account
    """
    user = UserBase.objects.get(email=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirm')


def account_register(request):
    if request.user.is_authenticated:
        # check if user is logged in
        return redirect('account:dashboard')
        # redirect to dashboard

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        # get data from the form
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']

            user.set_password(registerForm.cleaned_data['password'])

            # cleaned data -> make sure data is in correct format(email pattern and prevent password injection)
            user.is_active = False
            user.save()

            # setup email
            current_site = get_current_site(request)
            # get site url
            subject = 'Activate',
            message = render_to_string('account/registration/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/activation_sent.html')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
