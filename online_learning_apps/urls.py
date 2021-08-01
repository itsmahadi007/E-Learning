from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_form, name='login_form'),
    path('do_login', views.do_login, name="do_login"),
    path('do_register', views.do_register, name="do_register"),
    path('teacher_course', views.teacher_course, name='teacher_course'),
    path('teacher_create_course', views.teacher_create_course, name='teacher_create_course'),
    path('add_subjects', views.add_subjects, name='add_subjects'),
    path('create_course', views.create_course, name='create_course'),
    path('teacher_course_preview/<int:ids>', views.teacher_course_preview, name='teacher_course_preview'),

    path('teacher_course_update', views.teacher_course_update, name='teacher_course_update'),
    path('teacher_enrolled_students', views.teacher_enrolled_students, name='teacher_enrolled_students'),

    path('student_browse_course', views.student_browse_course, name='student_browse_course'),
    path('student_my_course', views.student_my_course, name='student_my_course'),
    path('student_course_preview/<int:ids>', views.student_course_preview, name='student_course_preview'),
    path('student_course_update', views.student_course_update, name='student_course_update'),

    path('log_out', views.log_out, name='log_out'),

]
