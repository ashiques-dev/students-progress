import re
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from authentication.models import OTPVerification, PasswordReset
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


username_regex = r'^(?=.*[a-zA-Z])[a-zA-Z .]{4,30}$'
email_regex = r'^[a-zA-Z0-9._]{2,30}@[a-zA-Z0-9.-]{2,30}\.[a-zA-Z]{2,30}$'
password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z0-9!@#$%^&*()_+=\-[\]{}|\\:;"\'<>,.?/~]{8,30}$'
combined_regex = r'^(?=.*[a-zA-Z])[a-zA-Z0-9_.-]{4,30}$|^[a-zA-Z0-9._]{2,30}@[a-zA-Z0-9.-]{2,30}\.[a-zA-Z]{2,30}$'
otp_regex = r"^\d{6}$"

User = get_user_model()

def validate_auth_fields(action, username=None, email=None, password=None, confirm_password=None):
    errors = {}
    if action == "signup":
        if not re.match(username_regex, username):
            errors['username'] = 'Username must be 4-30 characters long and contain only alphanumeric characters.'

    if action in ["signup", "signin", ]:
        if not re.match(email_regex, email):
            errors['email'] = 'Please enter a valid email address.'

    if action in ["signup", "signin", "reset-password"]:
        if not re.match(password_regex, password):
            errors['password'] = 'Password should be 8-30 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.'
    if action in ["signup", "reset-password"]:
        if password != confirm_password:
            errors['confirm_password'] = "Password and Confirm password didn't match."

    return errors


def auth_send_email(request, username, email,  uid=None, token=None, valid_until=None, html_for=None, otp=None):
    subject = ''
    emailcontext = {
        'username': username,
        'valid_until': valid_until,
    }

    if html_for == 'reset-password':
        subject = 'Password Reset Request'
        emailcontext['url'] = f'{
            request.scheme}://{request.get_host()}/auth/reset-password/{uid}/{token}'
        message = render_to_string('email/reset-password.html', emailcontext)

    elif html_for == 'reset-success':
        subject = 'Confirmation of Password Change'
        emailcontext['url'] = f'{
            request.scheme}://{request.get_host()}/auth/reset-password/{uid}/{token}'
        message = render_to_string('email/reset-success.html', emailcontext)

    else:
        subject = 'Account Verification Email'
        emailcontext['url'] = f'{
            request.scheme}://{request.get_host()}/auth/verify-otp/{uid}/{token}'

        emailcontext['otp'] = otp
        message = render_to_string(
            'email/otp-verification.html', emailcontext)

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    email.send()


def generate_otp_and_validity():
    otp = get_random_string(length=6, allowed_chars='9876543210')
    valid_until = timezone.localtime() + timedelta(minutes=10)
    return otp, valid_until


def generate_uid_and_token(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uid, token


def send_verification_mail(request, user):
    otp, valid_until = generate_otp_and_validity()
    uid, token = generate_uid_and_token(user)

    auth_send_email(request,
                    user.username, user.email, uid, token, valid_until,
                    otp=otp)

    user_otp, created = OTPVerification.objects.get_or_create(user=user,  defaults={
        'otp': otp, 'token': token, 'valid_until': valid_until, 'uid': uid})

    if not created:
        user_otp.otp = otp
        user_otp.uid = uid
        user_otp.token = token
        user_otp.valid_until = valid_until
        user_otp.save()


def check_uid_token(uid, token, is_password_reset=False):
    try:
        pk = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=pk)
        if is_password_reset:
            reset_link = PasswordReset.objects.get(
                user=user, uid=uid, token=token)
            return user, reset_link

        else:
            verify_otp = OTPVerification.objects.get(
                user=user, uid=uid, token=token,)
            return user, verify_otp
    except Exception:
        return None, None


def change_password(request, user, for_html):
    valid_until = timezone.localtime() + timedelta(minutes=20)
    uid, token = generate_uid_and_token(user)

    auth_send_email(
        request, user.username, user.email,  uid, token, valid_until, for_html)
    reset_link, created = PasswordReset.objects.get_or_create(user=user,  defaults={
        'token': token, 'valid_until': valid_until, 'uid': uid})

    if not created:
        reset_link.uid = uid
        reset_link.token = token
        reset_link.valid_until = valid_until
        reset_link.save()
