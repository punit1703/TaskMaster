from django.shortcuts import redirect, render, get_object_or_404
from todo.forms import TodoForm
from .models import Task, Category
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def homePage(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    categories = Category.objects.annotate(
        task_count=Count('task', filter=Q(task__user=request.user))
    )
            
    tasks = Task.objects.filter(user = request.user).filter(
        Q(title__icontains=q) |
        Q(category__name__icontains=q) |
        Q(description__icontains=q) |
        Q(is_completed__icontains=q)
    )

    tasks_count = tasks.count()
    all_tasks_count = Task.objects.filter(user = request.user).count()
    completed_count = Task.objects.filter(user = request.user, is_completed=True).count()
    not_completed = all_tasks_count - completed_count

    context = {
        'tasks':tasks, 
        'categories': categories, 
        'tasks_count': tasks_count, 
        'completed_count':completed_count,
        'not_completed': not_completed, 
        'selected_category':q
    }

    return render(request,'todo/home.html',context)

def todoView(request,pk):
    task = Task.objects.get(id=pk)
    context = {'task':task}
    return render(request,'todo/todo-view.html',context)    

def todoUpdate(request,pk):
    task = Task.objects.get(id=pk)
    form = TodoForm(instance=task)
    form.initial['category'] = str(task.category)

    categories = Category.objects.all()
    completed = False

    if request.method == 'POST':

        if request.POST.get('is_completed') == 'on':
            completed = True
        category_name = request.POST.get('category')
        category,created = Category.objects.get_or_create(name=category_name,user=request.user)
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.category = category
        task.due_date = request.POST.get('due_date')
        task.priority = request.POST.get('priority')
        task.is_completed = completed
        task.save()
        category = task.category
    
        if category:
            remaining_tasks = Task.objects.filter(category=category, user=request.user).count()
            if remaining_tasks == 0:
                category.delete()
        return redirect('home')
    
    context = {'form':form,'task':task,'categories':categories}
    return render(request,'todo/update-form.html',context)

@login_required(login_url='login')
def createTodo(request):
    form = TodoForm()
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        category_name = request.POST.get('category')
        category,created = Category.objects.get_or_create(name=category_name,user=request.user)

        Task.objects.create(
            user = request.user,
            title = request.POST.get('title'),
            description = request.POST.get('description'),
            category = category,
            due_date = request.POST.get('due_date'),
            priority = request.POST.get('priority'),
            is_completed = False
        )
        return redirect('home')

    context = {'form': form, 'categories': categories}

    return render(request, 'todo/create-form.html', context)

def deleteTodo(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    category = task.category 
    task.delete()
    
    if category:
        remaining_tasks = Task.objects.filter(category=category, user=request.user).count()
        if remaining_tasks == 0:
            category.delete()
            
    return redirect('home')