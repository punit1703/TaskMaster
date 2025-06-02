from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

from .models import Task, Category
from .forms import TodoForm


def _update_task_statuses(user):
    """Auto-update task completion and deletion based on due date."""
    today = timezone.now().date()

    # Auto-complete past-due tasks
    Task.objects.filter(user=user, is_completed=False, due_date__lt=today).update(is_completed=True)

    # Delete tasks older than 15 days past due date
    old_date = today - timedelta(days=15)
    Task.objects.filter(user=user, due_date__lt=old_date).delete()


@login_required(login_url='login')
def homePage(request):
    _update_task_statuses(request.user)

    q = request.GET.get('q', '')
    
    categories = Category.objects.annotate(
        task_count=Count('task', filter=Q(task__user=request.user))
    )

    tasks = Task.objects.filter(user=request.user).filter(
        Q(title__icontains=q) |
        Q(category__name__icontains=q) |
        Q(priority__icontains=q) |
        Q(description__icontains=q) |
        Q(is_completed__icontains=q)
    )

    context = {
        'tasks': tasks,
        'categories': categories,
        'tasks_count': tasks.count(),
        'completed_count': Task.objects.filter(user=request.user, is_completed=True).count(),
        'not_completed': Task.objects.filter(user=request.user, is_completed=False).count(),
        'selected_category': q
    }
    return render(request, 'todo/home.html', context)


def todoView(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    return render(request, 'todo/todo-view.html', {'task': task})


@login_required(login_url='login')
def createTodo(request):
    form = TodoForm()
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        data = request.POST
        category, _ = Category.objects.get_or_create(name=data.get('category'), user=request.user)

        Task.objects.create(
            user=request.user,
            title=data.get('title'),
            description=data.get('description'),
            category=category,
            due_date=data.get('due_date'),
            priority=data.get('priority'),
            is_completed=False
        )
        return redirect('home')

    return render(request, 'todo/create-form.html', {'form': form, 'categories': categories, 'title': 'create'})


@login_required(login_url='login')
def todoUpdate(request, pk):
    task = Task.objects.get(id=pk)
    form = TodoForm(instance=task)
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        data = request.POST
        category, _ = Category.objects.get_or_create(name=data.get('category'), user=request.user)

        task.title = data.get('title')
        task.description = data.get('description')
        task.category = category
        task.due_date = data.get('due_date')
        task.priority = data.get('priority')
        task.is_completed = data.get('is_completed') == 'on'
        task.save()

        return redirect('home')

    context = {
        'form': form,
        'task': task,
        'categories': categories,
        'title': 'update'
    }
    return render(request, 'todo/create-form.html', context )

@login_required(login_url='login')
def deleteTodo(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    category = task.category
    task.delete()

    if category and not Task.objects.filter(category=category, user=request.user).exists():
        category.delete()

    return redirect('home')
