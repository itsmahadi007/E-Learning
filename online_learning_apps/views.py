from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import CustomUser, Subject, Course, Teacher, Student


def home(request):
    return render(request, 'home.html')


def login_form(request):
    return render(request, 'login.html')


def do_login(request):
    if request.method == 'POST':
        username = request.POST['login-form-username']
        password = request.POST['login-form-password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.user_type == request.POST.get('gridRadios'):
                if user.user_type == '1':
                    auth.login(request, user)
                    # messages.success(request, user.user_type)
                    return redirect('teacher_course')
                elif user.user_type == '2':
                    auth.login(request, user)
                    # messages.success(request, user.user_type)
                    return redirect('student_my_course')
            else:
                messages.error(request, 'Invalid login credentials')
                return redirect('login_form')
        else:

            messages.error(request, 'Invalid login credentials 007')
            return redirect('login_form')
    messages.error(request, 'Something is Wrong, Please try again later')
    return redirect('login_form')


def do_register(request):
    if request.method == 'POST':
        firstname = request.POST['register-form-firstname']
        lastname = request.POST['register-form-lastname']
        email = request.POST['register-form-email']
        username = request.POST['register-form-username']
        password = request.POST['register-form-password']
        repassword = request.POST['register-form-repassword']
        who = request.POST['who']
        user_pos = ''
        if who == "Teacher":
            user_pos = '1'
        elif who == "Student":
            user_pos = '2'

        if password != repassword:
            messages.error(request, 'Password does not match')
            return redirect('login_form')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'This username is already used')
            return redirect('login_form')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered')
            return redirect('login_form')

        # try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=firstname,
                                              last_name=lastname, user_type=user_pos)
        user.save()
        messages.success(request, 'Successfully registered as ' + request.POST['who'])
        return redirect('login_form')
        # except Exception as e:
        #     messages.error(request, e)
        #     return redirect('login_form')

    return None


def teacher_course(request):
    course_list = Course.objects.order_by('course_name').filter(
        teacher=Teacher.objects.get(admin_id=request.user.id))

    data = {
        'course_list': course_list

    }
    # current_user = request.user.get_full_name()
    # print(current_user)
    return render(request, 'teacher-course.html', data)


def teacher_create_course(request):
    return render(request, 'teacher-create-course.html')


def create_course(request):
    if request.method == "POST":

        course_name = request.POST['courseName']
        status = True
        if request.POST['gridRadios'] == '1':
            status = True
        elif request.POST['gridRadios'] == '2':
            status = False

        obj = Teacher.objects.get(admin_id=request.user.id)

        try:
            course = Course(course_name=course_name, teacher=obj, status=status)
            course.save()

            data = {
                'course': course,
            }
            messages.success(request, "Course Created. Please Add subjects")
            return render(request, 'teacher-add-subjects.html', data)
        except Exception as e:
            print(e)
            messages.error(request, e)
            return render(request, 'teacher-create-course.html')
    else:
        messages.error(request, "something is wrong")
        return render(request, 'teacher-create-course.html')


def add_subjects(request):
    if request.method == "POST":
        course_id = request.POST["course_id"]
        sub_name = request.POST["subName"]
        obj = Course.objects.get(id=course_id)
        try:
            sub = Subject(subject_name=sub_name, course=obj)
            sub.save()

            data = {
                "course": obj,

            }

            messages.success(request, sub_name + " has been added")
            return render(request, 'teacher-add-subjects.html', data)

        except Exception as e:
            messages.error(request, e)
            return render(request, 'teacher-add-subjects.html', {"course": obj})


def teacher_course_preview(request, ids):
    # course_id = request.POST["course_id"]

    obj = get_object_or_404(Course, id=ids)
    # sub = Subject.objects.order_by('subject_name').filter(course_id=obj.id)
    try:
        sub = Subject.objects.order_by('subject_name').filter(course=obj.id)
        # print("try")
    except Subject.DoesNotExist:
        sub = {
            "subject_name": "No subject found"
        }
        # print("except")
    # for i in sub.subject_name:
    #     print(i)

    # for i in sub:
    #     print(i.subject_name)

    data = {
        "course": obj,
        "subjects": sub,
    }
    return render(request, "teacher-course-preview.html", data)


def teacher_course_update(request):
    if request.method == "POST":
        course_id = request.POST['course_id']
        obj = Course.objects.get(id=course_id)
        status = True
        if request.POST['gridRadios'] == '1':
            status = True
        elif request.POST['gridRadios'] == '2':
            status = False
        try:
            obj.status = status
            obj.save()
            # messages.success(request, obj.course_name + " has been updated")
            return redirect("teacher_course")
        except Exception as e:
            messages.error(request, e)
            print("hello except")
            return redirect("teacher_course")
    else:
        messages.error(request, "don't do that")


class geeks:
    def __init__(self, first_name, last_name, course_name, id):
        self.first_name = first_name
        self.last_name = last_name
        self.course_name = course_name
        self.id = id


def teacher_enrolled_students(request):
    # course_list = Course.objects.filter(teacher_id=Teacher.objects.get(admin_id=request.user.id))
    # cou = course_list.student_course.all()
    # global student_obj
    course = Course.objects.order_by("course_name").filter(teacher=Teacher.objects.get(admin_id=request.user.id))

    # for s in range(len(course)):
    #     student_obj = Student.objects.filter(course=course[s])

    t_list = []

    # course_list_with_students = []
    for s in course:
        course_name = s.course_name
        student_obj1 = Student.objects.filter(course=s)
        for s_o in student_obj1:
            t_list.append(geeks(s_o.admin.first_name, s_o.admin.last_name, course_name, s_o.id))
            # c_list.append(s_o.admin.get_full_name())
            # print(s_o.admin.get_full_name())
            # s_list.append(course_name)
            # print(course_name)

    # for i in range(len(c_list)):
    # print(c_list)

    # list = []
    #
    # # appending instances to list
    # list.append(geeks('Akash', 2))
    # list.append(geeks('Deependra', 40))
    # list.append(geeks('Reaper', 44))
    #
    # for obj in list:
    #     print(obj.name, obj.roll, sep=' ')

    # course_list_with_students.append(student_obj)
    # course = course_obj.course.order_by('course_name')
    # data = {
    #     'course': course,
    # }
    # for i in course:
    #     print(i.course_name)

    # for j in student_obj:
    #     print(j.admin.get_full_name())

    # for i in range(len(course_list_with_students)):

    # for j in course_list_with_students:
    #     print(j.admin.get_full_name())

    # print(student_obj.get(admin=1))
    data = {
        'total_list': t_list,

        'course': course
    }
    return render(request, 'teacher-enrolled-students.html', data)


def student_browse_course(request):
    course_list = Course.objects.order_by('course_name').filter(status=True)

    data = {
        'course_list': course_list

    }

    return render(request, 'student-browse-course.html', data)


def student_my_course(request):
    course_obj = Student.objects.get(admin_id=request.user.id)
    course = course_obj.course.order_by('course_name')
    data = {
        'course': course,
    }
    # obj = Student.objects.order_by('course__course_name').filter(id=request.user.id)
    # print("hello")
    # for i in course:
    #     print(i.course_name)
    # Course.objects.order_by('course_name').filter(
    # teacher_id=Teacher.objects.get(admin_id=request.user.id))
    return render(request, 'student-my-course.html', data)


def student_course_preview(request, ids):
    obj = get_object_or_404(Course, id=ids)
    # sub = Subject.objects.order_by('subject_name').filter(course_id=obj.id)
    try:
        sub = Subject.objects.order_by('subject_name').filter(course=obj.id)
        # print("try")
    except Subject.DoesNotExist:
        sub = {
            "subject_name": "No subject found"
        }
    enroll_status = False

    if Student.objects.filter(course=obj.id, admin_id=request.user.id).exists():
        enroll_status = True
    # print("try")
    # print("except")
    data = {"course": obj,
            "subjects": sub,
            'enroll_status': enroll_status
            }
    return render(request, "student-course-preview.html", data)


def student_course_update(request):
    if request.method == "POST":

        course_id = Course.objects.get(id=request.POST['course_id'])
        student_obj = Student.objects.get(admin_id=request.user.id)
        try:
            student_obj.course.add(course_id)
            # student_obj.save()
            messages.success(request, course_id.course_name + " course is Enrolled now")
            print("try")
            return redirect("student_browse_course")
        except Exception as e:
            messages.error(request, e)
            print("except")
            return redirect("student_browse_course")
        # try:
        #     obj.status = status
        #     obj.save()
        #     # messages.success(request, obj.course_name + " has been updated")
        #     return redirect("student_browse_course")
        # except Exception as e:
        #     messages.error(request, e)
        #     print("hello except")
        #     return redirect("student_browse_course")
    else:
        messages.error(request, "don't do that")


def log_out(request):
    # messages.success(request, 'you have logged out')
    logout(request)
    return HttpResponseRedirect("/")
