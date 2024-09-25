from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div

# class DonationForm(forms.ModelForm):
#     class Meta:
#         model = Donation
#         fields = ['cause', 'donor_name', 'amount', 'is_anonymous', 'is_recurring']

#         widgets = {
#             'cause': forms.Select(attrs={'class': 'form-select'}),
#             'donor_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Name'}),
#             'amount': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Amount'}),
#             'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
#             'is_recurring': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
#         }


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['cause', 'donor_name', 'amount', 'is_anonymous', 'is_recurring']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Field('cause', wrapper_class='mb-4'),
                Field('donor_name', wrapper_class='mb-4', id="donor_name_field"),
                Field('amount', wrapper_class='mb-4'),
                Div(
                    Field('is_anonymous', wrapper_class='inline-flex items-center', id="is_anonymous_field"),
                    css_class='mb-4'
                ),
                Div(
                    Field('is_recurring', wrapper_class='inline-flex items-center'),
                    css_class='mb-4'
                ),
                css_class='space-y-4'
            ),
            Submit('submit', 'Donate', css_class='w-full px-4 py-2 text-white bg-gray-700 rounded-md hover:bg-gray-600 focus:outline-none focus:bg-blue-600')
        )

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500'
            if field in ['is_anonymous', 'is_recurring']:
                self.fields[field].widget.attrs['class'] = 'form-checkbox h-5 w-5 text-blue-600 mr-2'


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            # 'content': forms.Textarea(attrs={'rows': 5}),
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'class': 'w-full p-2 border border-gray-300 rounded-md',
            'placeholder': 'Enter your comment here...'
        }