from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from llfadmin.utlis import check_is_superuser

# Create your views here.


@user_passes_test(check_is_superuser, login_url='/auth/sign-in/superuser', redirect_field_name='redirect')
def AdminDashboard(request):
    return render(request, 'pages/admin/dashboard.html')
