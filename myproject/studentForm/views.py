from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student

def student_form(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_students')
    else:
        form = StudentForm()
    return render(request, 'form.html', {'form': form})

def show_students(request):
    students = Student.objects.all()
    return render(request, 'show.html', {'students': students})
