from django.views import View
from django.db.models import Sum
from django.shortcuts import render, HttpResponseRedirect, redirect
from .utilities import get_employee_tasks
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Employee, Project, Ips, Attendance, Task, Resource
from datetime import datetime, time, timedelta, date
# from django.contrib.admin.views.decorators import staff_member_required
from .forms import SignUpForm, LoginForm, IpsForm, ProjectForm, EditEmployeeForm, EmployeePasswordChangeForm, CheckoutForm, ResourceForm, TaskForm, ReportForm, NewIpsForm
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Max
from django.contrib.auth.decorators import login_required


def add_employee(request):
    if request.user.is_authenticated:
        if request.user.hr == True:
            # emp_code = 1001 if Employee.objects.count() == 0 else Employee.objects.aggregate(max=Max('emp_id'))['max']+1
            print("HR >>> True...")
            form = SignUpForm()
            if request.method == "POST":
                
                form = SignUpForm(request.POST,request.FILES)
                if form.is_valid():
                    messages.success(request, 'Employee Created Successfully.')
                    new_contact = form.save(commit=False)
                    print("not committed...")
                    new_contact.emp_id = 1001 if Employee.objects.count() == 0 else Employee.objects.aggregate(max=Max('emp_id'))['max']+1
                    print("emp id...>>>",new_contact.emp_id)
                    new_contact.save()
                    print("Form saved...")
                    return HttpResponseRedirect('/view-employee/')
            return render(request, "app/add_employee.html", {'form':form,'active':'btn-primary'})
        messages.warning(request, 'Only HR...')
        return HttpResponseRedirect('/employee-profile/')        
    return HttpResponseRedirect('/login/')


def view_employee(request):
    if request.user.is_authenticated:
        if request.user.hr == True:
            print("matched...")
            employee_list = Employee.objects.all()
            return render(request,'app/employee_list.html',{'employee_list':employee_list,'active':'btn-primary'})
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


def employee_details(request):
    if request.user.is_authenticated:
        print("matched...")
        employee_list = Employee.objects.all()
        return render(request,'app/employee_detail.html',{'employee_list':employee_list})
    else:
        return HttpResponseRedirect('/login/')
    

def home(request):
    return render(request,'app/home.html',{'active':'btn-primary'})


def edit_employee(request, pk):
    if request.user.is_authenticated:
        if request.user.hr == True:
            emp = Employee.objects.get(pk=pk)
            form = EditEmployeeForm(instance=emp)
            if request.method == "POST":
                form = EditEmployeeForm(request.POST,request.FILES,instance=emp)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/view-employee/')  
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')            
                
    return render(request, "app/edit_employee.html", {'form':form, 'emp':emp,})


def delete_employee(request, pk):
    if request.user.is_authenticated:
        if request.user.hr == True:
            if request.method == 'POST':
                pi = Employee.objects.get(pk=pk)
                pi.delete()
                return HttpResponseRedirect('/view-employee/')
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


# def delete_employee_profile(request, pk):
#     if request.user.is_authenticated:
#         if request.user.hr == True:
#             if request.method == 'POST':
#                 pi = EmployeeProfile.objects.get(pk=pk)
#                 pi.delete()
#                 return HttpResponseRedirect('/view-employee-profile/')
#         else:
#             messages.warning(request, 'Only HR...')
#             return HttpResponseRedirect('/employee-profile/')
#     else:
#         return HttpResponseRedirect('/login/')


def delete_ips(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            if request.method == 'POST':
                pi = Ips.objects.get(pk=pk)
                pi.delete()
                return HttpResponseRedirect('/view-ips/')
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


def delete_resource(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            if request.method == 'POST':
                pi = Resource.objects.get(pk=pk)
                pi.delete()
                return HttpResponseRedirect('/view-resource/')
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


def delete_task(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            if request.method == 'POST':
                pi = Task.objects.get(pk=pk)
                pi.delete()
                return HttpResponseRedirect('/view-task/')
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


def delete_project(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            if request.method == 'POST':
                pi = Project.objects.get(pk=pk)
                pi.delete()
                return HttpResponseRedirect('/view-project/')
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')


def employee_login(request):
    print("login entered....")
    if not request.user.is_authenticated:
        print("not authenticated.....")
        if request.method == 'POST':
            print("inside post request.....")
            form = LoginForm(data=request.POST)
            print("form....")
            # form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                print(email)
                epass=form.cleaned_data['password']
                print(epass)
                user = authenticate(email=email,password=epass)
                print(user)
                if user:
                    login(request, user)
                    today = date.today()
                    checkin_exists = Attendance.objects.filter(employee=user, date=today, checkin__isnull=False).exists()
                    print("check-in-exist: ",checkin_exists)
                    if not checkin_exists:
                        print("Checkin not exist..")
                        attendance = Attendance(employee=user, checkin= datetime.now(), date=today)
                        attendance.save()
                        print("Login saved...")
                        messages.success(request,'Checked-IN Successfully for today!!')
                        return redirect('/employee-dashboard/')
                    print("Login after attendance....")
                    messages.success(request,'Log-IN Successfully!!')
                    return redirect('/employee-dashboard/')
                messages.success(request,'Wrong Credentials!!')
                return redirect('/login/')        
                        
        else:            
            form = LoginForm()
        
    else:
        return HttpResponseRedirect('/employee-profile/')
    return render(request, 'app/login.html', {'form':form})


def employee_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def task_hours_view(request):
    projects = Project.objects.filter(status="IP")
    employees = Employee.objects.all()
    employee_tasks = {}
    for employee in employees:        
        employee_tasks[employee.name] = []
        # print("employee_tasks : ",employee_tasks)
        for project in projects:
            # print("Projects: ",project)
            tasks = Task.objects.filter(project=project)
            # print("Tasks: ",tasks)
            for task in tasks:
                resource = Resource.objects.filter(task=task, employee=employee).first()
                if resource:
                    assigned_hours = resource.hours
                    print("type: ", type(assigned_hours))
                    ips = Ips.objects.filter(task=task, employee=employee).aggregate(total=Sum('hours'))
                    consumed_hours = ips['total'] if ips['total'] else timedelta(hours=0,minutes=0)
                    print("type: ", type(consumed_hours))
                    print("Break...")
                    print("Consumed Hours: ", consumed_hours)
                    assigned_hour = int(assigned_hours.total_seconds() / 3600)
                    consumed_hour = int(consumed_hours.total_seconds() / 3600)
                    employee_tasks[employee.name].append({
                        'project': project.project_name,
                        'task': task.name,
                        'assigned_hours': assigned_hour,
                        'consumed_hours': consumed_hour,
                    })

    context = {
        'employee_tasks': employee_tasks
    }
    return render(request, 'app/task_hours.html', context)


def add_ips(request,id=None):
    if request.user.is_authenticated:
        print("Authenticated")
        form = IpsForm(request.POST or None, user=request.user)
        print("Form...")
        context = {
            'form':form
                }
        if form.is_valid():
            print("forms validated")
            bf = form.save(commit=False)
            print("not committed...")
            bf.employee = request.user
            print("applied request.user...")
            bf.save()
            print("saved...")
            messages.success(request, 'Ips submitted Successfully.')
            return HttpResponseRedirect('/view-ips/')
    else:
        return HttpResponseRedirect('/login/')
    return render(request, "app/add_ips.html", context)


def add_resource(request):
    if request.user.is_authenticated:
        print("Authenticated")
        form = ResourceForm(request.POST or None)
        print("Form...")
        context = {
            'form':form
                }
        if form.is_valid():
            print("forms validated")
            form.save()
            print("saved...")
            messages.success(request, 'Resource allocated Successfully.')
            return HttpResponseRedirect('/add-resource/')
    else:
        return HttpResponseRedirect('/login/')
    return render(request, "app/add_resource.html", context)


def add_task(request):
    if request.user.is_authenticated:
        print("Authenticated")
        form = TaskForm(request.POST or None)
        print("Form...")
        context = {
            'form':form
                }
        if form.is_valid():
            print("forms validated")
            form.save()
            print("saved...")
            messages.success(request, 'Task created successfully.')
            return HttpResponseRedirect('/view-task/')
    else:
        return HttpResponseRedirect('/login/')
    return render(request, "app/add_task.html", context)


def view_ips(request):
    if request.user.is_authenticated:
        ips_list = Ips.objects.filter(employee=request.user)
        return render(request,'app/view_ips.html',{'ips_list':ips_list})
    else:
        return HttpResponseRedirect('/login/')


def view_resource(request):
    if request.user.is_authenticated:
        resource_list = Resource.objects.all()
        return render(request,'app/resource_list.html',{'resource_list':resource_list})
    else:
        return HttpResponseRedirect('/login/')


def view_ips_all(request):
    if request.user.is_authenticated:
        if request.user.hr == True:
            ips_list = Ips.objects.all()
            return render(request,'app/ips_list.html',{'ips_list':ips_list})
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/view-ips/')
    else:
        return HttpResponseRedirect('/login/')


def edit_ips(request, pk):
    if request.user.is_authenticated:
        if request.user.hr == True:
            ips = Ips.objects.get(pk=pk)
            form = IpsForm(request.POST or None, instance=ips)
            if request.method == "POST":
                if form.is_valid():

                    form.save()
                    return HttpResponseRedirect('/view-ips/')
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/view-ips/')


    else:
        return HttpResponseRedirect('/login/')            
                
    return render(request, "app/edit_ips.html", {'form':form, 'ips':ips,})


def edit_resource(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            resource = Resource.objects.get(pk=pk)
            form = ResourceForm(request.POST or None, instance=resource)
            if request.method == "POST":
                if form.is_valid():

                    form.save()
                    return HttpResponseRedirect('/view-resource/')
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/view-resource/')


    else:
        return HttpResponseRedirect('/login/')            
                
    return render(request, "app/edit_resource.html", {'form':form, 'resource':resource})


def edit_task(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            task = Task.objects.get(pk=pk)
            form = TaskForm(request.POST or None, instance=task)
            if request.method == "POST":
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/view-task/')
        else:
            messages.warning(request, 'Only HR...')
            return HttpResponseRedirect('/view-task/')


    else:
        return HttpResponseRedirect('/login/')            
                
    return render(request, "app/edit_task.html", {'form':form, 'task':task,})


def add_project(request,id=None):
    if request.user.is_authenticated:
        if request.user.acc == True:
            print("matched....")
            form = ProjectForm()
            print("Project Form...")
            if request.method == "POST":
                form = ProjectForm(request.POST)
                if form.is_valid():
                    print("form validated")
                    bf = form.save()
                    print("saved...")
                    messages.success(request, 'Project Added Successfully.')
                    return HttpResponseRedirect('/view-project/')
        else:
            messages.warning(request, 'Only Accounts Staff..')
            return HttpResponseRedirect('/employee-profile/')
    else:
        return HttpResponseRedirect('/login/')
    return render(request, "app/add_project.html", {'form':form})


def view_project(request):
    if request.user.is_authenticated:
        if request.user.acc == True:
            pro_list = Project.objects.all()
            return render(request,'app/project_list.html',{'pro_list':pro_list})
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/view-project/')
    else:
        return HttpResponseRedirect('/login/')


def view_task(request):
    if request.user.is_authenticated:
        if request.user.acc == True:
            task_list = Task.objects.all()
            return render(request,'app/task_list.html',{'task_list':task_list})
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/view-task/')
    else:
        return HttpResponseRedirect('/login/')


def edit_project(request, pk):
    if request.user.is_authenticated:
        if request.user.acc == True:
            pro = Project.objects.get(pk=pk)
            form = ProjectForm(request.POST or None, instance=pro)
            if request.method == "POST":
                if form.is_valid():

                    form.save()
                    return HttpResponseRedirect('/view-project/')
        else:
            messages.warning(request, 'Only ACCOUNTS...')
            return HttpResponseRedirect('/employee-profile/')


    else:
        return HttpResponseRedirect('/login/')            
                
    return render(request, "app/edit_project.html", {'form':form, 'pro':pro})


def employee_profile(request):
    if request.user.is_authenticated:
        emp = Employee.objects.get(email=request.user)
        return render(request, 'app/profile.html', {'emp': emp})
    return HttpResponseRedirect('/login/')


@login_required
def attendance_record(request):
    attendance_list = Attendance.objects.all()

    return render(request,'app/attendance_record.html',{'attendance_list':attendance_list})


def my_attendance_record(request):
    if request.user.is_authenticated:
        emp = request.user
        attendance_list = Attendance.objects.filter(employee=emp)
        return render(request,'app/attendance_record.html',{'attendance_list':attendance_list})
    return HttpResponseRedirect('/login/')   
    

@login_required
def report_view(request):
    form = ReportForm(request.GET)
    queryset = form.get_queryset()
    print("QuerySet: ",queryset)
    return render(request, 'app/report_view.html', {'form': form, 'data': queryset})


@login_required
def employee_task_view(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    for employee in employees:
        employee_tasks = []
        resources = Resource.objects.filter(employee=employee)
        for resource in resources:
            project = resource.task.project
            if project.status == True:
                employee_tasks.append({
                    'task': resource.task,
                    'assigned_hours': resource.task.hours,
                    'consumed_hours': resource.hours
                })
        context[employee.id] = employee_tasks

    return render(request, 'employee_task_view.html', context)


def employee_dashboard(request):
    if request.user.is_authenticated:
        checkout_form = CheckoutForm()
        employee = Employee.objects.get(email=request.user)
        projects = Project.objects.filter(status="IP")
        employee_tasks = get_employee_tasks(employee, projects)

        # Check if the employee has checked in today
        today = datetime.today()
        aaj = date.today()
        print("TODAY....",today)
        print("AAJ....",aaj)
        checkin = Attendance.objects.filter(employee=employee, date=aaj, checkin__isnull=False).first()
        print("This is Check-IN Time: ",checkin)
        # tasks = Task.objects.filter(resource__employee=emp, project__status="IP")
        # print("tasks: ",tasks)
        if checkin:
            supposed = checkin.checkin + timedelta(hours=9,minutes=15)
            print("Supposed checkout for today: ",supposed)
        else:
            supposed = None
        checkout = Attendance.objects.filter(employee=employee, date=aaj, checkout__isnull=False).first()
        print("This is Check-OUT Time: ",checkout)
        
        if request.method == 'POST':
            post_data = request.POST.copy()
            post_data['checkout'] = datetime.now()
            print("POST CheckOut : ",post_data['checkout'])
            form = CheckoutForm(post_data)

            print("This is Checkout FOrm with post request: ",form)
            print("REQUEST.POST....",request.POST['checkout'])
            c = request.POST['checkout']
            print("Type of checkout: ",type(post_data['checkout']))
            if form.is_valid() and checkin and not checkout:
                checkout_time = datetime.now()
                checkin.checkout = checkout_time
                print("Type checkout: ",type(checkout_time))
                print("Type checkin: ",type(checkin.checkin))
                aza = checkout_time-checkin.checkin
                print("Difference : ",aza)
                print("Type of difference : ",type(aza))
                checkin.difference = aza
                checkin.save()
                
                
                messages.success(request, 'Successfully Checked-OUT for today!')
                return HttpResponseRedirect('/employee-dashboard/')
            messages.success(request, 'Check-OUT already done for today!')
            
                        
            
        return render(request, 'app/employee_dashboard.html', {'emp': employee, 'checkout_form': checkout_form, 'checkin': checkin, 'checkout': checkout,'supposed':supposed, 'employee_tasks':employee_tasks})
    else:
        return HttpResponseRedirect('/login/')


# def add_employee_profile(request,id=None):
#     if request.user.is_authenticated:
#         if request.user.hr == True:
#             print("Authenticated")
#             form = EmployeeProfileForm(request.POST or None)
#             print("Form...")
#             context = {
#                 'form':form
#                 }
#             if form.is_valid():
#                 print("forms validated")
#                 form.save()
#                 print("form saved...")
#                 messages.success(request, 'Profile Created Successfully.')
#                 return HttpResponseRedirect('/view-employee-profile/')
#         else:
#             messages.warning(request, 'Only HR...')
#             return HttpResponseRedirect('/employee-profile/')            
#     else:
#         return HttpResponseRedirect('/login/')
#     return render(request, "app/add_employee_profile.html", context)


# def employee_profile_list(request):
#     if request.user.is_authenticated:
#         if request.user.hr == True:
#             print("matched...")
#             employee_profile_list = EmployeeProfile.objects.all()
#             return render(request,'app/employee_profile_list.html',{'employee_profile_list':employee_profile_list})
#         messages.warning(request, 'Only HR...')
#         return HttpResponseRedirect('/employee-profile/')


# def edit_employee_profile(request, pk):
#     if request.user.is_authenticated:
#         if request.user.hr == True:
#             emp_pro = EmployeeProfile.objects.get(pk=pk)
#             form = EmployeeProfileForm(request.POST or None, instance=emp_pro)
#             if request.method == "POST":
#                 if form.is_valid():

#                     form.save()
#                     return HttpResponseRedirect('/view-employee-profile/')
#         else:
#             messages.warning(request, 'Only HR...')
#             return HttpResponseRedirect('/employee-profile/')
#     else:
#         return HttpResponseRedirect('/login/')            
                
#     return render(request, "app/edit_employee_profile.html", {'form':form, 'emp_pro':emp_pro})
