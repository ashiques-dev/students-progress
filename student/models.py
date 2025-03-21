from django.db import models
from django.contrib.auth import get_user_model
from school.models import School
import os

# Create your models here.
User = get_user_model()

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]


def school_picture_upload_to(instance, filename):
    name = str(instance.name).replace(" ", "")
    filename = filename.replace(" ", "")
    return os.path.join('student_picture', f"{name}_{filename}")


class Student(models.Model):
    name = models.CharField(max_length=255)
    emis = models.CharField(max_length=255, unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    student_picture = models.ImageField(
        upload_to=school_picture_upload_to, blank=True)
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='students_created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='students_updated_by')

    class Meta:
        ordering = ['-id']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f'{self.id} {self.name}-{self.school}'


class StudentClass(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    class_name = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'class_name'], name='unique_student_class')
        ]

    def __str__(self):
        return f'{self.class_name} std {self.student.name} {self.student.id}'


class StudentClassReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)

    student_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, null=True, blank=True)

    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    numeracylevel = models.CharField(max_length=255, blank=True)
    literacylevel = models.CharField(max_length=255, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        class_name = self.student_class.class_name if self.student_class else 'N/A'
        return f'{self.student.id} {self.student.name} class {class_name}'
