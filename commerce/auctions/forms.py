from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", max_length=300)

class BidForm(forms.Form):
    amount = forms.DecimalField(label="Bid_amount", max_digits=10, decimal_places=2)