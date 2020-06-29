from django import forms


class PhoneForm(forms.Form):
    """
        form for getting the phone number of the user
    """
    phone = forms.CharField(label="Phone number ", max_length=12)


class Reg1Form(forms.Form):
    """
        form for new not staff users registration
    """
    last_name = forms.CharField(label="Last name", max_length=126)
    first_name = forms.CharField(label="First name", max_length=128)
    otp = forms.CharField(label="OTP", max_length=4)


class Reg2Form(forms.Form):
    """
        form for new staff users registration
    """
    last_name = forms.CharField(label="Last name", max_length=126)
    first_name = forms.CharField(label="First name", max_length=128)
    password = forms.CharField()
    confirm_password = forms.CharField()
    otp = forms.CharField(label="OTP", max_length=4)

    def clean(self):
        cleaned_data = super(Reg2Form, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "passwords do not match"
            )


class StaffForm(forms.Form):
    """
        form for authorization of staff users
    """
    password = forms.CharField()
    otp = forms.CharField(label="OTP", max_length=4)


class NotStaffForm(forms.Form):
    """
        form for authorization of not staff users
    """
    otp = forms.CharField(label="OTP", max_length=4)
