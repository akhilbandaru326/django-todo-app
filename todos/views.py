from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Todo
from .forms import TodoForm

def todo_list(request):
    """List all todos with optional filtering."""
    filter_by = request.GET.get('filter', 'all')

    todos = Todo.objects.all()
    if filter_by == 'active':
        todos = todos.filter(completed=False)
    elif filter_by == 'completed':
        todos = todos.filter(completed=True)

    context = {
        'todos':     todos,
        'filter_by': filter_by,
        'total':     Todo.objects.count(),
        'completed': Todo.objects.filter(completed=True).count(),
        'pending':   Todo.objects.filter(completed=False).count(),
    }
    return render(request, 'todos/todo_list.html', context)


def todo_create(request):
    """Create a new todo."""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()
            messages.success(request, f'Todo "{todo.title}" created successfully!')
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todos/todo_form.html', {'form': form, 'action': 'Create'})


def todo_update(request, pk):
    """Update an existing todo."""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Todo "{todo.title}" updated successfully!')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/todo_form.html', {'form': form, 'action': 'Update', 'todo': todo})


def todo_delete(request, pk):
    """Delete a todo."""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        title = todo.title
        todo.delete()
        messages.success(request, f'Todo "{title}" deleted successfully!')
        return redirect('todo_list')
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})


def todo_toggle(request, pk):
    """Toggle the completed status of a todo."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    status = 'completed' if todo.completed else 'marked as pending'
    messages.info(request, f'Todo "{todo.title}" {status}.')
    return redirect('todo_list')