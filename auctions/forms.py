from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Comment'}), max_length=300)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

class BidForm(forms.Form):
    amount = forms.DecimalField(label="",widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Bid', }), max_digits=10, decimal_places=2)