from django import forms
import datetime
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ValidationError, ModelForm
from .models import Employee, Ips, Project, Attendance, Task, Resource
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation, authenticate


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password Again',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = Employee
        fields = ['email', 'name', 'gender', 'phone', 'date_of_birth', 'joining_date', 'qualification', 'designation', 'address', 'ctc','resume', 'picture','edu_docs', 'aadhar', 'pan','certificate','additional_certificate']
        labels = {'email':'Email'}
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'joining_date':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'designation':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'ctc':forms.NumberInput(attrs={'class':'form-control'}),
            'resume':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'picture':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'edu_docs':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'aadhar':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'pan':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'certificate':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'additional_certificate':forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if Employee.objects.filter(email=email).exists():
                raise ValidationError("A User with this Email already exists")
        return self.cleaned_data
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditEmployeeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = Employee
        # fields = ['email', 'name', 'gender', 'emp_code', 'phone', 'date_of_birth', 'joining_date', 'qualification', 'designation', 'address', 'resume', 'edu_docs', 'identity_docs', 'skill_docs']
        fields = '__all__'
        exclude = ('hr','acc','is_active','is_admin','emp_id', 'password')
        labels = {'email':'Email'}
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'joining_date':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'designation':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'ctc':forms.NumberInput(attrs={'class':'form-control'}),
            'resume':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'picture':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'edu_docs':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'aadhar':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'pan':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'certificate':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'additional_certificate':forms.ClearableFileInput(attrs={'class':'form-control'}),
        }    


class LoginForm(forms.Form):
    email=forms.CharField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control'}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    

        # widgets = {
        #     'email':forms.EmailInput(attrs={'class':'form-control'}),
        #     # 'password':forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'})
        #     }
    def clean(self):
        if self.is_valid():

            email=self.cleaned_data.get('email')
            password=self.cleaned_data.get('password')

            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid LOGIN")    
# class LoginForm(AuthenticationForm):
#     email = UsernameField(widget=forms.EmailInput(attrs={'autofocus':True,'class':'form-control'}))
#     password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class IpsForm(forms.ModelForm):
    class Meta:
        model = Ips
        fields = ['task', 'comments','hours']
        widgets = {
            'task':forms.Select(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'hours':forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['task'].queryset = Task.objects.filter(resource__employee=user)


class NewIpsForm(forms.ModelForm):
    class Meta:
        model = Ips
        fields = ['task', 'comments','hours']
        widgets = {
            'task':forms.Select(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'hours':forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['task'].queryset = Task.objects.filter(resource__employee=user)
        


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'project','hours']
        widgets = {
            'name':forms.Select(attrs={'class':'form-control'}),
            'project':forms.Select(attrs={'class':'form-control'}),
            'hours':forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control'}),
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['employee', 'task', 'hours']
        widgets = {
            'employee':forms.Select(attrs={'class':'form-control'}),
            'task':forms.Select(attrs={'class':'form-control'}),
            'hours':forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'company_name', 'client_name', 'hours', 'max_hours', 'project_value', 'currency', 'project_type', 'sales_rep', 'project_manager', 'status']
        widgets = {
            'project_name':forms.TextInput(attrs={'class':'form-control'}),
            'company_name':forms.TextInput(attrs={'class':'form-control'}),
            'client_name':forms.TextInput(attrs={'class':'form-control'}),
            'hours':forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control'}),
            'max_hours':forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control'}),
            'project_value':forms.NumberInput(attrs={'class':'form-control'}),
            'currency':forms.Select(attrs={'class':'form-control'}),
            'project_type':forms.Select(attrs={'class':'form-control'}),
            'sales_rep':forms.TextInput(attrs={'class':'form-control'}),
            'project_manager':forms.TextInput(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'delivery_date':forms.DateInput(attrs={'class':'form-control'}),
        }


class EmployeePasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))



class CheckoutForm(forms.ModelForm):
    checkout = forms.DateTimeField(initial=datetime.datetime.now(), 
        widget=forms.HiddenInput())
    class Meta:
        model = Attendance
        fields = ['checkout']


class ReportForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    model = forms.ChoiceField(choices=[
        ('ips', 'Ips'),
        ('resource', 'Resource'),
        ('task', 'Task'),
        ('project', 'Project'),
        ('employee', 'Employee'),
    ])

    def get_queryset(self):
        if not self.is_valid():
            return None

        model = self.cleaned_data['model']
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        if model == 'ips':
            return Ips.objects.filter(date__range=(start_date, end_date))
        elif model == 'resource':
            return Resource.objects.filter(date__range=(start_date, end_date))
        elif model == 'task':
            return Task.objects.filter(date__range=(start_date, end_date))
        elif model == 'project':
            return Project.objects.filter(date__range=(start_date, end_date))
        elif model == 'employee':
            return Employee.objects.filter(created_at__range=(start_date, end_date))
        else:
            return None

