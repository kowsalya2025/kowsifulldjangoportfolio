from django import forms

class ContactForm(forms.Form):
    from_name = forms.CharField(max_length=100)
    reply_to = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
