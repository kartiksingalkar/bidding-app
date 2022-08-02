from django.db.models import Max
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from auctions.forms import AuctionForm, BidForm, ImageForm, CommentForm
from commerce.settings import MEDIA_URL

from .models import AuctionBid, AuctionListing, Categories, Comments, Images, User, WatchList


def get_object(self, request):
    try:
        return WatchList.objects.get(user = request.user)
    except:
        return 0

def get_number(self, wposts):
    try:
        return wposts.count()
    except:
        return 0

def get_wposts(self, watchlist):
    try:
        return watchlist.posts.all()
    except:
        return 0

def index(request):
    if request.user.is_authenticated:
        
        watchlist = get_object(WatchList ,request)
        
        wposts = get_wposts(WatchList,watchlist)

        number = get_number(WatchList, wposts)
        

        
        
        posts = AuctionListing.objects.all()
        maxbids = []
        imagelist = []  

        for post in posts:
            image =Images.objects.filter(post=post).first()
            imagelist.append(image)
            

            try:
                bids = AuctionBid.objects.get(auction=post)
                maxbid = bids.bids.order_by('-amount')[0].amount
                bids.price = bids.bids.order_by('-amount')[0].amount
                bids.save
                maxbids.append(maxbid)
            except:
                maxbid = AuctionListing.objects.get(title =post.title).price
                maxbids.append(maxbid)


        mylist = zip(posts, imagelist, maxbids)
        context = {
                'mylist': mylist,
                'MEDIA_ROOT' :  MEDIA_URL,
                'amount': number,
            }

        return render(request, "auctions/index.html", context)
    else:
        posts = AuctionListing.objects.all()
        imagelist = []
        maxbids = []
        for post in posts:
            image =Images.objects.filter(post=post).first()
            imagelist.append(image)
            maxbid = post.price
            maxbids.append(maxbid)
            

        mylist = zip(posts, imagelist, maxbids)
        context = {
                'mylist': mylist,
                'MEDIA_ROOT' :  MEDIA_URL,
            }
        return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return  redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "auctions/register.html")

def listing_view(request, auction):
    

    if request.user.is_authenticated:
        watchlist = get_object(WatchList ,request)
        
        wposts = get_wposts(WatchList,watchlist)

        number = get_number(WatchList, wposts)
        commentForm = CommentForm(request.POST)
        auctionlisting = AuctionListing.objects.get(title=auction)
        images = Images.objects.filter(post = auctionlisting)
        comments = Comments.objects.filter(post = auctionlisting)
        auctionOwner = auctionlisting.user
        tags = auctionlisting.tags
        added = False
        bidform = BidForm(request.POST)
        bids = AuctionBid.objects.get_or_create(auction = auctionlisting)
        bids = AuctionBid.objects.get(auction = auctionlisting)
        bidmessage = ''

        if WatchList.objects.filter(user=request.user, posts__title=auction).exists():
                added = True
        
        context = {
            'auction': auctionlisting,
            'comments': comments,
            'images' : images,
            'MEDIA_ROOT' :  MEDIA_URL,
            'commentForm': commentForm,
            'bidForm': bidform,
            'bids' : reversed(bids.bids.all()),
            'user' : request.user,
            'owner' : auctionOwner,
            'tags' : tags,
            'amount' : number,
            "added" : added,
            'bidMessage' : bidmessage,
        }
        if request.method == 'GET':

            if request.user.id is None:
                return redirect('login')
            try:
                auctionlisting.price = bids.bids.order_by('-amount')[0].amount
                maxbid = bids.bids.order_by('-amount')[0].amount
                maxbidder = bids.bids.order_by('-amount')[0].user
                auctionlisting.save()
                context = {
                        'auction': auctionlisting,
                        'comments': comments,
                        'images' : images,
                        'MEDIA_ROOT' :  MEDIA_URL,
                        'commentForm': commentForm,
                        'bidForm': bidform,
                        'bids' : reversed(bids.bids.all()),
                        'user' : request.user,
                        'owner' : auctionOwner,
                        'tags' : tags,
                        'amount' : number,
                        "added" : added,
                        'bidMessage' : bidmessage,
                        'price' : maxbid,
                        'winner' : maxbidder
                    }
            except:
                maxbid = auctionlisting.price
                maxbidder = auctionlisting.user
                context = {
                        'auction': auctionlisting,
                        'comments': comments,
                        'images' : images,
                        'MEDIA_ROOT' :  MEDIA_URL,
                        'commentForm': commentForm,
                        'bidForm': bidform,
                        'bids' : reversed(bids.bids.all()),
                        'user' : request.user,
                        'owner' : auctionOwner,
                        'tags' : tags,
                        'amount' : number,
                        "added" : added,
                        'bidMessage' : bidmessage,
                        'price' : maxbid,
                        'winner' : maxbidder
                    }

            return render(request, 'auctions/auction_view.html', context)
        elif request.method == 'POST':

            if request.user.id is None:
                return redirect('login')
            
            try:
                if request.POST["checkclose"] == 'closeit':
                    auctionlisting.status = False
                    auctionlisting.save()
                    return render(request, 'auctions/auction_view.html', context)
            except:
                pass

            if commentForm.is_valid():
                    comment_form = commentForm.save(commit=False)
                    comment_form.post = auctionlisting
                    comment_form.user = request.user
                    comment_form.save()
            if bidform.is_valid():
                try:
                    auctionlisting.price = bids.bids.order_by('-amount')[0].amount
                    maxbid = bids.bids.order_by('-amount')[0].amount
                    maxbidder = bids.bids.order_by('-amount')[0].user
                    auctionlisting.save()
                    context = {
                        'auction': auctionlisting,
                        'comments': comments,
                        'images' : images,
                        'MEDIA_ROOT' :  MEDIA_URL,
                        'commentForm': commentForm,
                        'bidForm': bidform,
                        'bids' : reversed(bids.bids.all()),
                        'user' : request.user,
                        'owner' : auctionOwner,
                        'tags' : tags,
                        'amount' : number,
                        "added" : added,
                        'bidMessage' : bidmessage,
                        'price' : maxbid,
                        'winner' : maxbidder
                    }
                except:
                    maxbid = auctionlisting.price
                    maxbidder = auctionlisting.user
                    context = {
                        'auction': auctionlisting,
                        'comments': comments,
                        'images' : images,
                        'MEDIA_ROOT' :  MEDIA_URL,
                        'commentForm': commentForm,
                        'bidForm': bidform,
                        'bids' : reversed(bids.bids.all()),
                        'user' : request.user,
                        'owner' : auctionOwner,
                        'tags' : tags,
                        'amount' : number,
                        "added" : added,
                        'bidMessage' : bidmessage,
                        'price' : maxbid,
                        'winner' : maxbidder
                    }
                
                if int(request.POST.get("amount")) > maxbid:
                    bid_form = bidform.save(commit=False)
                    bid_form.user = request.user
                    bid_form.auction = auctionlisting
                    bid_form.save()
                    bids.bids.add(bid_form)
                    bids = AuctionBid.objects.get(auction = auctionlisting)
                    maxbidder = bids.bids.order_by('-amount')[0].user
                    context = {
                        'auction': auctionlisting,
                        'comments': comments,
                        'images' : images,
                        'MEDIA_ROOT' :  MEDIA_URL,
                        'commentForm': commentForm,
                        'bidForm': bidform,
                        'bids' : reversed(bids.bids.all()),
                        'user' : request.user,
                        'owner' : auctionOwner,
                        'tags' : tags,
                        'amount' : number,
                        "added" : added,
                        'bidMessage' : bidmessage,
                        'price' : maxbid,
                        'winner' : maxbidder
                    }

                else:
                    try:
                        auctionlisting.price = bids.bids.order_by('-amount')[0].amount
                        maxbid = bids.bids.order_by('-amount')[0].amount
                        auctionlisting.save()
                        maxbidder = bids.bids.order_by('-amount')[0].user
                        context = {
                            'auction': auctionlisting,
                            'comments': comments,
                            'images' : images,
                            'MEDIA_ROOT' :  MEDIA_URL,
                            'commentForm': commentForm,
                            'bidForm': bidform,
                            'bids' : reversed(bids.bids.all()),
                            'user' : request.user,
                            'owner' : auctionOwner,
                            'tags' : tags,
                            'amount' : number,
                            "added" : added,
                            'bidMessage' : bidmessage,
                            'price' : maxbid,
                            'winner' : maxbidder
                        }
                    except:
                        maxbid = auctionlisting.price
                        maxbidder = auctionlisting.user
                        context = {
                            'auction': auctionlisting,
                            'comments': comments,
                            'images' : images,
                            'MEDIA_ROOT' :  MEDIA_URL,
                            'commentForm': commentForm,
                            'bidForm': bidform,
                            'bids' : reversed(bids.bids.all()),
                            'user' : request.user,
                            'owner' : auctionOwner,
                            'tags' : tags,
                            'amount' : number,
                            "added" : added,
                            'bidMessage' : bidmessage,
                            'price' : maxbid,
                            'winner' : maxbidder
                        }
                    bidmessage = f'You must enter a bid greater than {maxbid}'
                    context = {
                        'auction': auctionlisting,
                        'comments': comments,
                        'images' : images,
                        'MEDIA_ROOT' :  MEDIA_URL,
                        'commentForm': commentForm,
                        'bidForm': bidform,
                        'bids' : reversed(bids.bids.all()),
                        'user' : request.user,
                        'owner' : auctionOwner,
                        'tags' : tags,
                        'amount' : number,
                        "added" : added,
                        'bidMessage' : bidmessage,
                        'price' : maxbid,
                        'winner' : maxbidder
                    }

            return render(request, 'auctions/auction_view.html', context)
    else :
        return redirect('login')


def post(request):
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=3)
    #'extra' means the number of photos that you can upload   ^
    tags = Categories.objects.all()
    if request.user.is_authenticated:
        watchlist = get_object(WatchList ,request)
        
        wposts = get_wposts(WatchList,watchlist)

        number = get_number(WatchList, wposts)
        if request.method == 'POST':
        
            auctionForm = AuctionForm(request.POST)
            formset = ImageFormSet(request.POST, request.FILES,queryset=Images.objects.none())
            title = auctionForm['title'].value()
            tags = request.POST.getlist('tags', [])
            pics = request.POST.getlist('form-0-image', [])
        
        
            if auctionForm.is_valid() and formset.is_valid():
                post_form = auctionForm.save(commit=False)
                post_form.user = request.user
                post_form.save()
                for tag in tags:
                    post_form.tags.add(tag)
                
        
                for form in formset.cleaned_data:
                    #this helps to not crash if the user   
                    #do not upload all the photos
                    if form:
                        image = form['image']
                        photo = Images(post=post_form, image=image)
                        photo.save()
                return redirect(f"/listing/{title}")
            else:
                return render(request, 'auctions/newAuction.html',{
                    'message': "Fill all fields",
                    'amount' : number
                })
        else:
            auctionForm = AuctionForm()
            formset = ImageFormSet(queryset=Images.objects.none())
        return render(request, 'auctions/newAuction.html',{
            'auctionForm': auctionForm, 'formset': formset, 'tags': tags, 'amount' : number
            })
    else:
        return redirect("login")

def categories(request):
    if request.user.is_authenticated:
        watchlist = get_object(WatchList ,request)
        
        wposts = get_wposts(WatchList,watchlist)

        number = get_number(WatchList, wposts)
        tags = Categories.objects.all()
        return render(request, 'auctions/categories.html', {
            'tags' : tags,
            'amount' : number
        })
    else:
        return redirect('login')

def category(request, category):
    if request.user.is_authenticated:
        watchlist = get_object(WatchList ,request)
        
        wposts = get_wposts(WatchList,watchlist)

        number = get_number(WatchList, wposts)
        tag = category

        posts = AuctionListing.objects.filter(tags__name = tag)
        imagelist = []

        

        for post in posts:
            image =Images.objects.filter(post=post).first()
            imagelist.append(image)

        mylist = zip(posts, imagelist)
        return render(request, 'auctions/category.html', {
            'tag' : tag,
            'posts' : posts,
            'mylist' : mylist,
            'MEDIA_ROOT' :  MEDIA_URL,
            'amount' : number
        })
    else:
        return redirect('login')

def watchlist(request):
    if request.user.is_authenticated:
        user = request.user
        watchlist = get_object(WatchList ,request)
            
        posts = get_wposts(WatchList,watchlist)

        number = get_number(WatchList, posts)

        imagelist = []
        if number != 0:
            message = False
            for post in posts:
                image =Images.objects.filter(post=post).first()
                imagelist.append(image)

            mylist = zip(posts, imagelist)
            return render(request, 'auctions/watchlist.html', {
                'name':user,
                'mylist' : mylist,
                'MEDIA_ROOT' :  MEDIA_URL,
                'amount' : number
            })
        else:
            message = True
            return render(request, 'auctions/watchlist.html', {
                'name':user,
                'amount' : number,
                'message' : message
            })
    else:
        return redirect('login')

def watchlist_add(request, name):
    if request.user.is_authenticated:
        watchlist = get_object(WatchList ,request)
        
        wposts = get_wposts(WatchList,watchlist)

        number = get_number(WatchList, wposts)

        item_to_save = get_object_or_404(AuctionListing, title=name)
        images = Images.objects.filter(post = item_to_save)
        comments = Comments.objects.filter(post = item_to_save)
        auctionOwner = item_to_save.user
        tags = item_to_save.tags
        commentForm = CommentForm(request.POST)
        added = False
        context = {
            'auction': item_to_save,
            'comments': comments,
            'images' : images,
            'MEDIA_ROOT' :  MEDIA_URL,
            'commentForm': commentForm,
            'user' : request.user,
            'owner' : auctionOwner,
            'tags' : tags,
            'amount' : number,
            'added' : added
        }
        # Check if the item already exists in that user watchlist
        if WatchList.objects.filter(user=request.user, posts__title=name).exists():
            added = True
            return render(request, 'auctions/auction_view.html', context)
        # Get the user watchlist or create it if it doesn't exists
        user_list, created = WatchList.objects.get_or_create(user=request.user)
        # Add the item through the ManyToManyField (Watchlist => item)
        user_list.posts.add(item_to_save)
        return redirect('watchlist')
    return redirect("index")


def watchlist_remove(request, name):
    if request.user.is_authenticated:

        item_to_save = get_object_or_404(AuctionListing, title=name)

        # Check if the item already exists in that user watchlist
        if WatchList.objects.filter(user=request.user, posts__title=name).exists():
            data = WatchList.objects.get(user=request.user)
            data.posts.remove(item_to_save)
            return redirect('watchlist')
    return redirect("index")