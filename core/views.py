from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
import random

@login_required
def ai_suggestions(request):
    suggestions = [
        "Start your day with the most important task.",
        "Avoid multitasking to improve focus.",
        "Take short breaks every 1 hour.",
        "Complete high priority tasks first.",
        "Review your completed tasks at night.",
    ]

    plan = random.sample(suggestions, 3)

    return render(request, 'ai.html', {
        'plan': plan
    })


@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    else:
        form = TaskForm()

    return render(request, 'home.html', {
        'tasks': tasks,
        'form': form,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks
    })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('home')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('home')