from django import forms

from .models import Member, Comment


class SignUpForm(forms.ModelForm):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = Member
        exclude = ("joined_date", "slug")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ("password", "joined_date", "slug")


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(
        label="Old password", widget=forms.PasswordInput, min_length=8
    )

    class Meta:
        model = Member
        fields = ("password",)

    new_password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)


class LoginForm(forms.Form):
    email = forms.EmailField(label="Your Email")
    password = forms.CharField(
        label="Your Password", widget=forms.PasswordInput, min_length=8
    )


class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(label="Your Comment", widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ("comment_text",)
