from django.urls import path
from payment_stripe.views import create_checkout_session, payment_success

urlpatterns = [
    path('create', create_checkout_session),
    path('success', payment_success),
]
