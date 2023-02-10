from .models import Task, Employee, Resource, Ips, Project, Attendance
from django.db.models import Sum
from datetime import timedelta


def get_employee_tasks(employee, projects):
    employee_tasks = []
    for project in projects:
        tasks = Task.objects.filter(project=project)
        for task in tasks:
            resource = Resource.objects.filter(task=task, employee=employee).first()
            if resource:
                assigned_hours = resource.hours
                ahr = int(assigned_hours.total_seconds() / 3600)
                ips = Ips.objects.filter(task=task, employee=employee).aggregate(total=Sum('hours'))
                consumed_hours = ips['total'] if ips['total'] else timedelta(hours=0,minutes=0)
                chr = int(consumed_hours.total_seconds() / 3600)
                employee_tasks.append({
                    'project': project.project_name,
                    'task': task.name,
                    'assigned_hours': ahr,
                    'consumed_hours': chr,
                })

    return employee_tasks
