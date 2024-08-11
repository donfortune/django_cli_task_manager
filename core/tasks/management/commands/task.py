from django.core.management.base import BaseCommand
from tasks.models import Task
from datetime import datetime

class Command(BaseCommand):
    help = 'Manage tasks from the command line'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action to perform: add, view, update, delete')
        parser.add_argument('--title', type=str, help='Title of the task')
        parser.add_argument('--description', type=str, help='Description of the task')
        parser.add_argument('--status', type=str, help='Status of the task')
        parser.add_argument('--due_date', type=str, help='Due date of the task (YYYY-MM-DD)')

    def handle(self, *args, **kwargs):
        action = kwargs['action']

        if action == 'add':
            self.add_task(kwargs)
        elif action == 'view':
            self.view_tasks()
        elif action == 'update':
            self.update_task(kwargs)
        elif action == 'delete':
            self.delete_task(kwargs)
        else:
            self.stdout.write(self.style.ERROR('Invalid action!'))

    def add_task(self, kwargs):
        title = kwargs['title']
        description = kwargs['description']
        due_date = datetime.strptime(kwargs['due_date'], '%Y-%m-%d').date()

        task = Task.objects.create(title=title, description=description, due_date=due_date)
        task.save()
        self.stdout.write(self.style.SUCCESS(f'Task "{title}" added successfully!'))

    def view_tasks(self):
        tasks = Task.objects.all()
        for task in tasks:
            self.stdout.write(f'{task.id}: {task.title} - {task.status} - Due: {task.due_date}')

    def update_task(self, kwargs):
        task_id = kwargs['id']
        task = Task.objects.get(id=task_id)
        if 'title' in kwargs:
            task.title = kwargs['title']
        if 'description' in kwargs:
            task.description = kwargs['description']
        if 'status' in kwargs:
            task.status = kwargs['status']
        if 'due_date' in kwargs:
            task.due_date = datetime.strptime(kwargs['due_date'], '%Y-%m-%d').date()
        task.save()
        self.stdout.write(self.style.SUCCESS(f'Task "{task.title}" updated successfully!'))

    def delete_task(self, kwargs):
        task_id = kwargs['id']
        task = Task.objects.get(id=task_id)
        task.delete()
        self.stdout.write(self.style.SUCCESS(f'Task "{task.title}" deleted successfully!'))
