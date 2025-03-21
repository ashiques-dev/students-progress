from datetime import datetime
from student.models import Student, StudentClass
from django.core.files.storage import default_storage


def update_or_create_student(request,  school=None, student=None):
    error = {}
    data = {}

    emis = request.POST.get('emis')
    if student:
        if Student.objects.exclude(id=student.id).filter(emis=emis).exists():
            error['emis'] = 'Student with same Emis ID already exist.'
            return data, error

    else:
        if Student.objects.filter(emis=emis).exists():
            error['emis'] = 'Student with same Emis ID already exist.'
            return data, error

    name = request.POST.get('name')
    dob = request.POST.get('dob')
    gender = request.POST.get('gender')
    class_name = request.POST.get('class_name')
    year = request.POST.get('year')
    student_picture = request.FILES.get('student_picture')

    if student:
        student.name = name
        student.emis = emis
        student.dob = dob
        student.gender = gender
        student.updated_by = request.user

        if student_picture:
            if student.student_picture:
                old_file_path = student.student_picture.path
                if default_storage.exists(old_file_path):
                    default_storage.delete(old_file_path)
            student.student_picture = student_picture

        student.save()

        student_class = StudentClass.objects.filter(
            student=student).first()
        student_class.class_name = class_name
        student_class.year = year

        student_class.save()

        data['name'] = student.name
        data['emis'] = student.emis
        data['dob'] = datetime.strptime(
            student.dob, '%Y-%m-%d').strftime('%b. %d, %Y')
        data['gender'] = student.gender
        data['class_name'] = student_class.class_name
        data['year'] = student_class.year
        return data, error

    else:

        student = Student(name=name, emis=emis, dob=dob,
                          gender=gender, student_picture=student_picture, created_by=request.user, school=school)
        student.save()

        student_class = StudentClass(
            student=student,  class_name=class_name, year=year
        )
        student_class.save()

        data['id'] = student.id
        data['name'] = student.name
        data['emis'] = student.emis
        data['dob'] = datetime.strptime(
            student.dob, '%Y-%m-%d').strftime('%b. %d, %Y')
        data['gender'] = student.gender
        return data, error
