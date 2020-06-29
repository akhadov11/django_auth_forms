import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from .models import User, Department
from .forms import PhoneForm, Reg1Form, Reg2Form, StaffForm, NotStaffForm

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_phone(request):
    """
    function for processing phone number and selecting right case of authentication
    :param request: http request object
    :return: HttpRedirect
    """
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            otp = get_random_string(4, allowed_chars='0123456789')
            logger.info(f'{otp}')
            print(otp)
            request.session['otp'] = otp
            if not User.objects.filter(phone=form.cleaned_data["phone"]) and User.objects.all():
                return redirect('auth', case=1, phone=form.cleaned_data["phone"])
            elif not User.objects.filter(phone=form.cleaned_data["phone"]) and not User.objects.all():
                return redirect('auth', case=2, phone=form.cleaned_data["phone"])
            elif User.objects.get(phone=form.cleaned_data["phone"]).is_staff:
                return redirect('auth', case=3, phone=form.cleaned_data["phone"])
            elif not User.objects.get(phone=form.cleaned_data["phone"]).is_staff:
                return redirect('auth', case=4, phone=form.cleaned_data["phone"])
    else:
        form = PhoneForm()

    return render(request, 'core/index.html', {'form': form})


def authenticate(request, case, phone):
    """
    function for authorization and reqgistration of users
    :param request: http request object
    :param case: case of auth
    :param phone: phone umber from previous form
    :return: HttpResponse
    """
    if request.method == 'POST':
        if case == 1:
            form = Reg1Form(request.POST)
            if form.is_valid() and form.cleaned_data["otp"] == request.session.get("otp"):
                full_name = f'{form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}'
                user = User.objects.create(full_name=full_name, phone=phone, is_staff=False)
                return HttpResponse(f"{user}")
        elif case == 2:
            form = Reg2Form(request.POST)
            dep = Department.objects.get(id=1)
            if form.is_valid() and form.cleaned_data["otp"] == request.session.get("otp"):
                full_name = f'{form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}'
                user = User.objects.create(full_name=full_name, phone=phone, password=form.cleaned_data["password"],
                                           department=dep, is_staff=True)
                return HttpResponse(f"{user}")
        elif case == 3:
            form = StaffForm(request.POST)
            user = User.objects.get(phone=phone)
            if form.is_valid():
                if form.cleaned_data["otp"] == request.session.get("otp") and form.cleaned_data["password"] ==\
                        User.objects.get(phone=phone).password:
                    return HttpResponse(f"Добрый день, {user.full_name}. Ваш отдел {user.department.name}.")
                else:
                    return HttpResponse("Вы указали неверный пароль.")
        elif case == 4:
            form = NotStaffForm(request.POST)
            user = User.objects.get(phone=phone)
            if form.is_valid() and form.cleaned_data["otp"] == request.session.get("otp"):
                return HttpResponse(f"Добрый день, {user.full_name}.")

    else:
        if case == 1:
            form = Reg1Form()
        elif case == 2:
            form = Reg2Form()
        elif case == 3:
            form = StaffForm()
        elif case == 4:
            form = NotStaffForm()
    return render(request, 'core/register.html', {'form': form})
