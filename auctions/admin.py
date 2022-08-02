from django.contrib import admin

from .models import AuctionBid, Categories, User, AuctionListing, Bid, Comments, Images, WatchList
# Register your models here.

admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(Images)
admin.site.register(Categories)
admin.site.register(WatchList)
admin.site.register(AuctionBid)