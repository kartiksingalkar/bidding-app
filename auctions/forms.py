from django import forms

from auctions.models import AuctionListing, Bid, Images, Comments


class AuctionForm(forms.ModelForm):
    title = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Tilte', 'class': 'form-control'}))
    body = forms.CharField(max_length=245, widget=forms.TextInput(attrs={'placeholder': 'Item Description.', 'class': 'form-control'}))
    price = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Price', 'size': '50%', 'class': 'form-control', 'aria-label':"Bid"}))

    class Meta:
        model = AuctionListing
        fields = ('title', 'body', 'price')
 
 
class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='')   
    image.widget.attrs.update({'class': 'custom-file-input inputGroupFile01', 'id': 'inputGroupFile01','onblur': 'check()'}) 
    class Meta:
        model = Images
        fields = ('image', )

class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Comment', 'size': '50%', 'class': 'form-control', 'aria-label':"Add Comment:"}))

    class Meta:
        model = Comments
        fields = ("content",)

class BidForm(forms.ModelForm):
    amount = forms.IntegerField (widget=forms.NumberInput(attrs={'placeholder': 'Bid', 'size': '50%', 'class': 'form-control', 'aria-label':"Bid"}))

    class Meta:
        model = Bid
        fields = ("amount",)
