from django import forms
from django.contrib.auth import get_user_model
from .models import Donation, Volunteer, EventRegistration, Campaign

User = get_user_model()


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    subject = forms.CharField(max_length=255, required=False)
    message = forms.CharField(widget=forms.Textarea)


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor', 'amount', 'method', 'campaign']
        widgets = {
            'method': forms.Select(),
            'campaign': forms.Select(),
        }


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['skills', 'availability']
        widgets = {
            'skills': forms.Textarea(),
        }


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['name', 'email', 'extra_info']
        widgets = {
            'extra_info': forms.Textarea(attrs={'rows': 3}),
        }