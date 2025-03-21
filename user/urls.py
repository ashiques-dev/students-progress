from django.urls import path
from student.views import UserAllStudents, UserGetStudent
from user.views import *
from school.views import UserGetSchool, UserAllSchools

urlpatterns = [
    path('', UserAllSchools, name='user-all-schools'),
    path('school/<int:id>/', UserGetSchool, name='user-get-school'),

    path('school/<int:id>/students/', UserAllStudents, name='user-all-students'),
    path('school/<int:school_id>/student/<int:id>/',
         UserGetStudent, name='user-get-student'),

    path('reports/<int:id>/', NewReport, name='new-report'),
    path('upgrade-class/<int:id>/', upgradeClass, name='upgrade-class'),

]
