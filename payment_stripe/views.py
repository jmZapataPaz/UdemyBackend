from django.shortcuts import render
import stripe
from BackendServer.settings import NGROK_URL, STRIPE_SECRET_KEY
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
stripe.api_key = STRIPE_SECRET_KEY

@api_view(['POST'])
@permission_classes([AllowAny])
def create_checkout_session(request):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'zapatos deportivos',
                        },
                        'unit_amount': 10 *100,  #Se trabaja en centavos
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=f'https://{NGROK_URL}/payment_stripe/success',
            cancel_url=f'https://{NGROK_URL}/payment_stripe/cancel',
        )
        return Response({'checkout_url': session.url})
    
    except Exception as e:
        return Response(
            {
                "message": str(e), 
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
@api_view(['GET'])
@permission_classes([AllowAny])
def payment_success(request):
    return render(request, 'redirect.html')