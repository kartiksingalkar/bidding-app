from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/new", views.post, name="new"),
    path("listing/<str:auction>", views.listing_view, name="listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<str:name>", views.watchlist_add, name="watchlist_add"),
    path("watchlist/delete/<str:name>", views.watchlist_remove, name="watchlist_remove"),
    # path("<str:user>/watchlist", views.watchlist, name="watchlist"),
    
]
