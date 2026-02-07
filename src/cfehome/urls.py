from django.contrib import admin
from django.urls import path, include
from subscriptions import views as subscriptions_views
from checkouts import views as checkout_views
from .views import (
    home_view,
    about_view,
    pw_protected_view,
    user_only_view,
    staff_only_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    # Checkout
    path(
        "checkout/sub-price/<int:price_id>/",
        checkout_views.product_price_redirect_view,
        name="sub-price-checkout",
    ),
    path(
        "checkout/start/",
        checkout_views.checkout_redirect_view,
        name="stripe-checkout-start",
    ),
    path(
        "checkout/success/",
        checkout_views.checkout_finalize_view,
        name="stripe-checkout-end",
    ),
    # Pricing
    path("pricing/", subscriptions_views.subscription_price_view, name="pricing"),
    path(
        "pricing/<str:interval>/",
        subscriptions_views.subscription_price_view,
        name="pricing_interval",
    ),
    # Other pages
    path("about/", about_view),
    path("hello-world/", home_view),
    path("hello-world.html", home_view),
    # Billing / Accounts
    path(
        "accounts/billing/",
        subscriptions_views.user_subscription_view,
        name="user_subscription",
    ),
    path(
        "accounts/billing/cancel",
        subscriptions_views.user_subscription_cancel_view,
        name="user_subscription_cancel",
    ),
    path("accounts/", include("allauth.urls")),
    # Protected
    path("protected/user-only/", user_only_view),
    path("protected/staff-only/", staff_only_view),
    path("protected/", pw_protected_view),
    # Profiles
    path("profiles/", include("profiles.urls")),
    # Admin
    path("admin/", admin.site.urls),
]
