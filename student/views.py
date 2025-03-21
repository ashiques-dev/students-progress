from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from student.utils import update_or_create_student
from student.models import Student, StudentClass, StudentClassReport
from school.models import School
from user.utils import check_is_user
from llfadmin.utlis import check_is_superuser, make_paginator
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.


@user_passes_test(check_is_superuser, login_url='/auth/sign-in/superuser', redirect_field_name='redirect')
def AdminAllStudents(request, id):
    school = School.objects.filter(id=id).first()
    if request.method == 'GET':
        if school:
            class_name = request.GET.get('class_name')
            year = request.GET.get('year')
            if class_name and year:
                students = Student.objects.filter(
                    school=school, studentclass__class_name=class_name, studentclass__year=year,).values('dob', 'emis', 'gender', 'id', 'name', 'school',  'student_picture',)
            else:
                students = Student.objects.filter(
                    school=school).values('dob', 'emis', 'gender', 'id', 'name', 'school',  'student_picture',)
            media_url = settings.MEDIA_URL
            page_obj = make_paginator(request, students, 12)
            return render(request, 'pages/admin/students.html', {'page': page_obj,  'media_url': media_url})
        else:
            messages.error(request, 'Unable to find the students list')
            return redirect('admin-all-schools')

    if request.method == 'POST':
        if not school:
            return JsonResponse({'message': 'Unable to find the school info to add student'}, status=404)

        data, error = update_or_create_student(request, school=school)
        if error:
            return JsonResponse(error, status=400)
        if data:
            return JsonResponse(data, status=200)


@user_passes_test(check_is_superuser, login_url='/auth/sign-in/superuser', redirect_field_name='redirect')
def AdminGetStudent(request, id):
    student = Student.objects.filter(id=id).first()
    if request.method == 'GET':
        if not student:
            messages.error(request, 'Student not found')
            return redirect('admin-all-students')
        else:
            class_name = request.GET.get('class')
            class_id = request.GET.get('class_id')
            student_class = StudentClass.objects.filter(
                student=student).first()
            latest_class = student_class

            if class_name and class_id:
                student_class = StudentClass.objects.filter(
                    class_name=class_name, id=class_id, student=student).first()
                if not student_class:
                    messages.error(request, 'Invalid student class')
                    return redirect('admin-get-student',  id)

            reports = StudentClassReport.objects.filter(
                student_class=student_class)
            classes = StudentClass.objects.filter(
                student=student)

            return render(request, 'pages/admin/student.html', {'student': student, 'classes': classes, 'reports': reports,  'id': id, 'student_class': student_class, 'latest_class': latest_class})

    if request.method == 'POST':
        if not student:
            return JsonResponse({'message': 'Unable to find the student'}, status=404)
        try:
            data, error = update_or_create_student(
                request, student.school, student)
            if error:
                return JsonResponse(error, status=400)
            if data:
                return JsonResponse(data, status=200)
        except Exception as e:
            return JsonResponse({'message': 'user in same classname already exist'}, status=500)


@user_passes_test(check_is_user, login_url='/auth/sign-in/user', redirect_field_name='redirect')
def UserAllStudents(request, id):
    school = School.objects.filter(
        schoolpermission__user=request.user,
        schoolpermission__can_crud=True,
        schoolpermission__school_id=id).first()

    if request.method == 'GET':
        if school:
            class_name = request.GET.get('class_name')
            year = request.GET.get('year')
            if class_name and year:
                students = Student.objects.filter(
                    school=school, studentclass__class_name=class_name, studentclass__year=year,).values('dob', 'emis', 'gender', 'id', 'name', 'school',  'student_picture',)

            else:

                students = Student.objects.filter(
                    school=school).values('dob', 'emis', 'gender', 'id', 'name', 'school',  'student_picture',)
            media_url = settings.MEDIA_URL
            page_obj = make_paginator(request, students, 12)
            return render(request, 'pages/user/students.html', {'page': page_obj,  'media_url': media_url, 'id': id})

        else:
            messages.error(
                request, 'you dont have the permission to access this school')
            return redirect('user-all-schools')
    if request.method == 'POST':
        if not school:
            return JsonResponse({'message': 'Unable to find the school info to add student'}, status=404)

        data, error = update_or_create_student(request, school=school)
        if error:
            return JsonResponse(error, status=400)
        if data:
            return JsonResponse(data, status=200)


@user_passes_test(check_is_user, login_url='/auth/sign-in/user', redirect_field_name='redirect')
def UserGetStudent(request, school_id, id):
    school = School.objects.filter(
        schoolpermission__user=request.user,
        schoolpermission__can_crud=True,
        schoolpermission__school_id=school_id).first()

    if request.method == 'GET':
        if not school:
            messages.error(
                request, 'you dont have the permission to access this school')
            return redirect('user-all-schools')

        student = Student.objects.filter(id=id, school=school).first()
        if not student:
            messages.error(request, 'Student not found')
            return redirect('user-all-students', school_id)

        class_name = request.GET.get('class')
        class_id = request.GET.get('class_id')

        student_class = StudentClass.objects.filter(
            student=student).first()

        latest_class = student_class

        if class_name and class_id:
            student_class = StudentClass.objects.filter(
                class_name=class_name, id=class_id, student=student).first()
            if not student_class:
                messages.error(request, 'Invalid student class')
                return redirect('user-get-student', school_id, id)

        reports = StudentClassReport.objects.filter(
            student_class=student_class)

        classes = StudentClass.objects.filter(
            student=student)
        return render(request, 'pages/user/student.html', {'student': student, 'classes': classes, 'reports': reports, 'school_id': school_id, 'id': id, 'student_class': student_class, 'latest_class': latest_class})

    if request.method == 'POST':
        if not school:
            return JsonResponse({'message': 'Unable to find the school info to add student'}, status=404)

        student = Student.objects.filter(id=id, school=school).first()
        if not student:
            return JsonResponse({'message': 'Unable to find the student'}, status=404)
        try:
            data, error = update_or_create_student(request, school, student)
            if error:
                return JsonResponse(error, status=400)
            if data:
                return JsonResponse(data, status=200)
        except Exception as e:
            return JsonResponse({'message': 'user in same classname already exist'}, status=500)
