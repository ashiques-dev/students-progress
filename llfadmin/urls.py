from django.urls import path
from student.views import AdminAllStudents, AdminGetStudent
from school.views import AdminAllSchools, AdminGetSchool
from llfadmin.views import *
urlpatterns = [
    path('', AdminDashboard, name='admin-dashboard'),
    path('schools/', AdminAllSchools, name='admin-all-schools'),
    path('school/<int:id>/', AdminGetSchool, name='admin-get-school'),
    
    path('school/<int:id>/students/', AdminAllStudents, name='admin-all-students'),
    path('student/<int:id>/', AdminGetStudent, name='admin-get-student'),

]
