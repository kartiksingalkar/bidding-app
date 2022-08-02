from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ImageField
from django.template.defaultfilters import slugify


class User(AbstractUser):
    pass

class Categories(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return f"{self.name}"

class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ownerOfAuction")
    title = models.CharField(max_length=128)
    datePosted = models.DateField(auto_now_add=True)
    body = models.CharField(max_length=400)
    tags = models.ManyToManyField(Categories, related_name="Tags")
    price = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id} {self.title}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ownerOfWatchlist")
    posts = models.ManyToManyField(AuctionListing, null=True)

    def __str__(self):
        return f"{self.user} is watching {self.posts}"


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)

class Images(models.Model):
    post = models.ForeignKey(AuctionListing,on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=get_image_filename,verbose_name='Image')
    def __str__(self):
        return f"{self.id} Image for {self.post}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ownerOfBid")
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user}"

class Comments(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ownerOfComment")
    content = models.TextField()
    post = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id} {self.user} {self.post}"
    
class AuctionBid(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bids  = models.ManyToManyField(Bid)

    def __str__(self):
        return f"{self.auction.title} has {self.bids.count()} bids"