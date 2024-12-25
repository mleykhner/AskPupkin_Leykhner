from django import forms
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'nickname']

class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    nickname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['nickname'].initial = user.profile.nickname

    def save(self, commit=True):
        instance = super().save(commit=False)
        user = instance.user

        user.email = self.cleaned_data.get('email')
        user.save()

        if commit:
            instance.save()
        return instance

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=True, help_text="Comma separated list of tags")

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def clean_tags(self):
        tags_data = self.cleaned_data.get('tags')
        tags = [tag.strip() for tag in tags_data.split(',') if tag.strip()]
        return tags

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']