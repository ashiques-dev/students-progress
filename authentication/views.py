from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.http import JsonResponse
from authentication.utils import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model


# Create your views here.
User = get_user_model()


def redirect_authenticated_user(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(
                request, 'you\'ve already finished your authentication')
            if request.user.is_superuser:
                return redirect('/super-user/')
            else:
                return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@redirect_authenticated_user
def SignUp(request):

    if request.method == 'GET':
        return render(request, 'pages/auth/sign_up.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        errors = validate_auth_fields('signup',
                                 username, email, password, confirm_password)

        if errors:
            return JsonResponse(errors, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': "User with same email already exist"}, status=400)

        new_user = User.objects.create_user(
            username=username, email=email, password=password)

        try:
            send_verification_mail(request, new_user)
        except:
            new_user.delete()
            return JsonResponse({'message': "Unable to send user verification mail please try register later"}, status=500)

        messages.success(
            request, 'Your account has been successfully created. Please check your email to verify your account')
        return JsonResponse({'message': 'User created successfully!'}, status=201)


def SignIn(request, role):
    if role != 'superuser':
        role = 'user'
    if request.method == 'GET':
        redirect_url = request.GET.get('redirect')
        if not redirect_url:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    return redirect('/superuser/')
                else:
                    return redirect('/')
        return render(request, 'pages/auth/sign_in.html', {'role': role})

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        errors = validate_auth_fields('signin',
                                 email=email, password=password)

        if errors:
            return JsonResponse(errors, status=400)

        user = authenticate(email=email, password=password)
        if user is not None:
            pos = 'superuser' if user.is_superuser else 'user'
            if role != pos:
                return JsonResponse({'message': "You do not have the required permissions to access this role."}, status=400)
            if not user.is_verified:
                try:
                    send_verification_mail(request, user)
                except:
                    return JsonResponse({'message': "Your account has not been verified. Unable to send user verification mail please try again later"}, status=500)

                return JsonResponse({'message': "Your account has not been verified. A verification email has been sent to your inbox. Please check your email."}, status=400)
            if user.is_blocked:
                return JsonResponse({'message': "Your account has been blocked."}, status=400)
            login(request, user)
            return JsonResponse({'role': role}, status=200)
        else:
            return JsonResponse({'message': "Invalid user credentials"}, status=400)


@redirect_authenticated_user
def VerifyOtp(request, uid, token):

    if request.method == 'GET':
        user, verify_otp = check_uid_token(uid, token)
        if not (user and verify_otp):
            messages.error(request, 'The activation link is invalid.')
            return redirect('/auth/sign-in/user')
        return render(request, 'pages/auth/verify_otp.html')

    if request.method == 'POST':
        user, verify_otp = check_uid_token(uid, token)

        if not (user and verify_otp):
            messages.error(request, 'The activation link is invalidf.')
            return JsonResponse({}, status=404)

        if not verify_otp.valid_until >= timezone.now():
            return JsonResponse({"message": 'The OTP is expired. Try clicking on Resend OTP'}, status=400)

        otp = request.POST.get('otp')

        if not re.match(otp_regex, otp):
            return JsonResponse({"message": "Please enter a valid OTP."}, status=400)

        otp = int(otp)

        if verify_otp.otp == otp:
            user.is_verified = True
            user.save()
            verify_otp.delete()
            login(request, user)
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({"message": 'Invalid OTP'}, status=400)


@redirect_authenticated_user
def ResendVerifyOtp(request, uid, token):

    user, verify_otp = check_uid_token(uid, token)
    if not (user and verify_otp):
        messages.error(request, 'The activation link is invalidf.')
        return JsonResponse({}, status=404)
    otp, valid_until = generate_otp_and_validity()

    try:
        auth_send_email(request, user.username, user.email, uid, token, valid_until,
                        otp=otp)
    except:
        return JsonResponse({'message': "Unable to send mail try again later"}, status=500)

    verify_otp.otp = otp
    verify_otp.valid_until = valid_until
    verify_otp.save()
    return JsonResponse({}, status=200)


@redirect_authenticated_user
def ForgotPassword(request):

    if request.method == 'GET':
        return render(request, 'pages/auth/forgot_password.html')

    if request.method == 'POST':
        email = request.POST.get('email')

        if not re.match(email_regex, email):
            return JsonResponse({"message": "Please enter a valid email address."}, status=400)

        try:
            user = User.objects.get(email=email)

        except:
            return JsonResponse({'message': 'User not found'}, status=404)

        try:
            change_password(request, user, 'reset-password')
        except:
            return JsonResponse({'message': "Unable to send the password reset link mail"}, status=500)

        role = 'superuser' if user.is_superuser else 'user'

        messages.success(
            request, "Password reset email has been sent. Please check your inbox.")
        return JsonResponse({'role': role}, status=200)


@redirect_authenticated_user
def ResetPassword(request, uid, token):
    if request.method == 'GET':
        user, reset_link = check_uid_token(uid, token, is_password_reset=True)

        if not (user and reset_link):
            messages.error(request, 'The activation link is invalid.')
            return redirect('/auth/forgot-password')

        if not reset_link.valid_until >= timezone.now():
            messages.error(request, 'The activation link is expired')
            return redirect('/auth/forgot-password')

        return render(request, 'pages/auth/reset_password.html')

    if request.method == 'POST':
        user, reset_link = check_uid_token(uid, token, is_password_reset=True)

        if not (user and reset_link):
            messages.error(request, 'The activation link is invalid.')
            return JsonResponse({}, status=404)

        if not reset_link.valid_until >= timezone.now():
            messages.error(request, 'The activation link is expired.')
            return JsonResponse({}, status=404)

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        errors = validate_auth_fields('reset-password',
                                 password=password, confirm_password=confirm_password)

        if errors:
            return JsonResponse(errors, status=400)

        if check_password(password, user.password):
            return JsonResponse({'message': "You cannot reuse on of your previous password. Please choose a new one."}, status=400)

        try:
            change_password(request, user, 'reset-success')
        except:
            return JsonResponse({'message': "Unable to change password please try later"}, status=500)

        user.set_password(password)
        user.save()
        reset_link.delete()
        messages.success(
            request, "Password has changed successfully")
        role = 'superuser' if user.is_superuser else 'user'
        return JsonResponse({'role': role}, status=200)
