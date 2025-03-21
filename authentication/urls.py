
from django.urls import path
from authentication.views import *

urlpatterns = [
    path('sign-up/', SignUp, name='sign-up'),
    path('sign-in/<str:role>/', SignIn, name='sign-in'),
    path('verify-otp/<str:uid>/<str:token>/', VerifyOtp,
         name='verify-otp'),
    path('resend-otp/<str:uid>/<str:token>/',
         ResendVerifyOtp, name='resend-verification-otp/'),
    path('forgot-password/', ForgotPassword, name='forgot-password'),
    path('reset-password/<str:uid>/<str:token>/',
         ResetPassword, name='reset-password'),
]
