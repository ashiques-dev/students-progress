from django.shortcuts import render
from django.http import JsonResponse
from student.models import Student, StudentClass, StudentClassReport

# Create your views here.


def NewReport(request, id):
    if request.method == 'POST':
        student = Student.objects.filter(id=id).first()
        if not student:
            return JsonResponse({'message': 'Student not found'}, status=404)

        latest_class = StudentClass.objects.filter(
            student=student).first()

        numeracylevel = request.POST.get('numeracylevel')
        literacylevel = request.POST.get('literacylevel')
        description = request.POST.get('description')

        report = StudentClassReport(
            student=student,
            student_class=latest_class,
            numeracylevel=numeracylevel,
            literacylevel=literacylevel,
            description=description,
            updated_by=request.user
        )
        report.save()
        data = {
            'class': report.student_class.class_name,
            'numeracylevel': report.numeracylevel,
            'literacylevel': report.literacylevel,
            'description': report.description,
            'updated_by': report.updated_by.username,
            'created_at': report.created_at.strftime('%b. %d, %Y')
        }
        return JsonResponse(data, status=200)


def upgradeClass(request, id):
    if request.method == 'GET':
        student = Student.objects.filter(id=id).first()
        if not student:
            return JsonResponse({'message': 'Student not found'}, status=404)

        latest_class = StudentClass.objects.filter(
            student=student).first()

        try:
            class_name = int(latest_class.class_name)+1
            year = int(latest_class.year)+1

            if class_name >= 12:
                return JsonResponse({'message': 'Student already in 12 th grade'}, status=400)

            new_class = StudentClass(
                student=student, class_name=class_name, year=year)
            new_class.save()
            return JsonResponse({'message': "Successfully upgraded"}, status=200)

        except:
            return JsonResponse({'message': 'Unexpected error'}, status=500)
