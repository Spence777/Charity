from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['cause', 'donor_name', 'amount', 'is_anonymous', 'is_recurring']

        widgets = {
            'cause': forms.Select(attrs={'class': 'form-select'}),
            'donor_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Name'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Amount'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
