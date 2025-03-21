from django.contrib import messages
from django.shortcuts import render, redirect
from school.utils import update_or_create_school
from school.models import School, SchoolPermission
from django.contrib.auth.decorators import user_passes_test
from user.utils import check_is_user
from llfadmin.utlis import check_is_superuser, make_paginator
from django.conf import settings
from django.http import JsonResponse

# Create your views here.


@user_passes_test(check_is_superuser, login_url='/auth/sign-in/superuser', redirect_field_name='redirect')
def AdminAllSchools(request):
    if request.method == 'GET':
        schools = School.objects.values(
            'id', 'name', 'state', 'school_picture')
        media_url = settings.MEDIA_URL
        page_obj = make_paginator(request, schools, 6)
        return render(request, 'pages/admin/schools.html', {'page': page_obj, 'media_url': media_url})
    
    if request.method == 'POST':
        new_school = update_or_create_school(request)
        return JsonResponse({'school': new_school}, status=201)


@user_passes_test(check_is_superuser, login_url='/auth/sign-in/superuser', redirect_field_name='redirect')
def AdminGetSchool(request, id):
    school = School.objects.filter(id=id).first()

    if request.method == 'GET':
        if not school:
            messages.error(request, 'School not found')
            return redirect('admin-all-schools')
        return render(request, 'pages/admin/school.html', {'school': school})
    
    if request.method == 'POST':
        if not school:
            return JsonResponse({'message': 'Unable to do the task'}, status=404)
        new_school = update_or_create_school(request, school)
        return JsonResponse({'school': new_school}, status=200)


@user_passes_test(check_is_user, login_url='/auth/sign-in/user', redirect_field_name='redirect')
def UserAllSchools(request):
    if request.method == 'GET':
        schools = School.objects.filter(
            schoolpermission__user=request.user,
            schoolpermission__can_crud=True).values(
            'id', 'name', 'state', 'school_picture')

        media_url = settings.MEDIA_URL
        page_obj = make_paginator(request, schools, 6)
        return render(request, 'pages/user/schools.html', {'page': page_obj, 'media_url': media_url})


@user_passes_test(check_is_user, login_url='/auth/sign-in/user', redirect_field_name='redirect')
def UserGetSchool(request, id):
    school = School.objects.filter(
        schoolpermission__user=request.user,
        schoolpermission__can_crud=True,
        schoolpermission__school_id=id).first()
    
    if request.method == 'GET':
        if not school:
            messages.error(
                request, 'you dont have the permission to access this school')
            return redirect('user-all-schools')
        return render(request, 'pages/user/school.html', {'school': school})
    
    if request.method == 'POST':
        if not school:
            return JsonResponse({'message': 'Unable to do the task'}, status=404)

        new_school = update_or_create_school(request, school)
        return JsonResponse({'school': new_school}, status=200)
