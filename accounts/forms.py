from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from registration.forms import RegistrationForm


class LoginForm(forms.Form):
    email = forms.EmailField(label='Your E-Mail:')
    password = forms.CharField(widget=forms.PasswordInput, label='Password:')


class AccountRegistrationForm(RegistrationForm):
    def clean(self):
        try:
            if Profile.objects.get(email=self.cleaned_data['email']):
                raise forms.ValidationError('This username already in a use. Choose another please.')
        except Profile.DoesNotExist:
            pass
            try:
                if Profile.objects.get(nick_name=self.cleaned_data['nick_name']):
                    raise forms.ValidationError('This nickname already in a use. Choose another please.')
            except Profile.DoesNotExist:
                pass
            return self.cleaned_data

    class Meta:
        model = Profile
        fields = ('email', 'nick_name', 'password1', 'password2')


class AccountEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=('%d.%m.%Y', '%Y-%m-%d'), required=False)
    class Meta:
        model = Profile
        exclude = ['email', 'is_active', 'is_admin', 'last_login', 'password']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': ''},),
            'nick_name': forms.TextInput(attrs={'placeholder': ''}),
            'date_of_birth': forms.TextInput(attrs={'placeholder': ''}),
            'about_me': forms.Textarea(attrs={'placeholder': ''}),
            'country': forms.TextInput(attrs={'placeholder': ''}),
            'city': forms.TextInput(attrs={'placeholder': ''}),
        }


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('email', 'full_name', 'nick_name', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Profile
        fields = ('email', 'password', 'full_name', 'nick_name', 'date_of_birth', 'about_me', 'photo', 'is_active', 'is_admin', 'subscription')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'nick_name', 'full_name', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'nick_name', 'full_name', 'about_me', 'photo', 'subscription')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()