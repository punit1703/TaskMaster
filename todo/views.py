from django.shortcuts import redirect, render, get_object_or_404
from todo.forms import TodoForm
from .models import Task, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def homePage(request):
    categories = Category.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    tasks = Task.objects.filter(
        Q(title__icontains=q) |
        Q(category__name__icontains=q) |
        Q(description__icontains=q)
    )
    context = {'tasks':tasks, 'categories': categories}
    return render(request,'todo/home.html',context)

@login_required
def todoView(request,pk):
    task = Task.objects.get(id=pk)
    context = {'task':task}
    return render(request,'todo/todo-view.html',context)    

@login_required
def todoUpdate(request,pk):
    task = Task.objects.get(id=pk)
    form = TodoForm(instance=task)
    categories = Category.objects.all()

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')

        category_name = request.POST.get('category')
        if category_name:
            category,created = Category.objects.get_or_create(name=category_name,user=request.user)
            task.category = category
        task.save()
        return redirect('home')
    
    context = {'form':form,'task':task,'categories':categories}
    return render(request,'todo/update-form.html',context)

@login_required
def createTodo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('home')
    else:
        form = TodoForm()
    return render(request, 'todo/create-form.html', {'form': form})

def deleteTodo(request,pk):
    task = get_object_or_404(Task, id=pk)
    task.delete()
    return redirect('home')

def toggle_completion(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == "POST":
        task.is_completed = not task.is_completed
        task.save()
    return redirect('home')