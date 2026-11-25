from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import UserProfile


class StyledFormMixin:
    """Applies consistent CSS classes to form widgets."""

    def _apply_widget_classes(self) -> None:
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            if 'form-input' not in existing:
                field.widget.attrs['class'] = f'{existing} form-input'.strip()


class UserRegisterForm(StyledFormMixin, UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label='First Name')
    last_name = forms.CharField(max_length=150, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email Address')
    phone = forms.CharField(max_length=20, required=False, label='Phone Number')
    occupation = forms.CharField(max_length=100, required=False, label='Role / Occupation')
    address = forms.CharField(max_length=255, required=False, label='Address')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'occupation',
            'address',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_widget_classes()
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['email'].widget.attrs['placeholder'] = 'you@example.com'
        self.fields['phone'].widget.attrs['placeholder'] = 'Optional phone number'
        self.fields['occupation'].widget.attrs['placeholder'] = 'e.g. Student, Developer'
        self.fields['address'].widget.attrs['placeholder'] = 'Optional city / address'

    @transaction.atomic
    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name'].strip()
        user.last_name = self.cleaned_data['last_name'].strip()
        user.email = self.cleaned_data['email'].strip()
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data.get('phone', '').strip(),
                    'occupation': self.cleaned_data.get('occupation', '').strip(),
                    'address': self.cleaned_data.get('address', '').strip(),
                },
            )
        return user


class UserLoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_widget_classes()
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter password'


class UserUpdateForm(StyledFormMixin, forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label='First Name')
    last_name = forms.CharField(max_length=150, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email Address')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_widget_classes()


class ProfileUpdateForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'occupation', 'address', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Short bio or technical background'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_widget_classes()


class StyledPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_widget_classes()
