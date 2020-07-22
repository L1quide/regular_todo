from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import TDL
from .forms import TDF

def index(request):
    todo_list = TDL.objects.order_by('id')

    form = TDF()
    context = {'todo_list':todo_list, 'form': form}
    return render(request, 'TD/index.html', context)


@require_POST
def add_item(request):
    form = TDF(request.POST)
    if form.is_valid():
        new_todo = TDL(text=request.POST['text'])
        new_todo.save()

    return redirect('index')


def completeTodo(request, todo_id):
    todo = TDL.objects.get(pk=todo_id)
    todo.complete = True
    todo.save()
    return redirect('index')


def delete(request, todo_id):
    TDL.objects.get(pk=todo_id).delete()

    return redirect('index')


# Create your views here.
