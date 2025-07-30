from django.shortcuts import render
import stripe
from BackendServer.settings import NGROK_URL, STRIPE_SECRET_KEY
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
stripe.api_key = STRIPE_SECRET_KEY
from django.http import JsonResponse


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
                        'unit_amount': 10 * 100,
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=f'https://{NGROK_URL}/payment_stripe/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'https://{NGROK_URL}/payment_stripe/cancel',
        )
        return Response({
            'checkout_url': session.url,
            'session_id': session.id
        })
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
    session_id = request.GET.get('session_id')
    wants_json = request.GET.get('json', None)

    if not session_id:
        data = {
            "message": "No session_id provided.",
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "payment_status": "error"
        }
        return JsonResponse(data) if wants_json else Response(data, status=status.HTTP_400_BAD_REQUEST)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            data = {
                "message": "Pago completado exitosamente.",
                "statusCode": status.HTTP_200_OK,
                "payment_status": "success"
            }
            if wants_json:
                return JsonResponse(data)
            else:
                return render(request, 'redirect.html', {
                    **data,
                    'session_id': session_id
                })
        else:
            data = {
                "message": "El pago no fue completado.",
                "statusCode": status.HTTP_402_PAYMENT_REQUIRED,
                "payment_status": "failed"
            }
            return JsonResponse(data) if wants_json else Response(data, status=status.HTTP_402_PAYMENT_REQUIRED)
    except Exception as e:
        data = {
            "message": str(e),
            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "payment_status": "error"
        }
        return JsonResponse(data) if wants_json else Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)