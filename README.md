# Django Student Form Project

A simple Django project to collect and display student information using forms and templates.

---

## 🛠️ Prerequisite: Install Django

Before starting, make sure you have Django installed. Run:

```bash
pip install django
```

---

## 📁 Project Structure

- Project: `myproject`
- App: `studentForm`
- Features:
  - Add student details
  - View all student records in a table

---

## ✅ Step-by-Step Setup

### 1. Create Django Project & App

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp studentForm
```

---

### 2. Install App

In `myproject/settings.py`, add `'studentForm',` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'studentForm',
]
```

---

### 3. Link App URLs

In `myproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('studentForm.urls')),
]
```

---

### 4. Create Model

In `studentForm/models.py`:

```python
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    roll = models.CharField(max_length=20)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name
```



---

### 5. Create Form (No Validation)

In `studentForm/forms.py`:

```python
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
```

---

### 6. Create Templates

📁 Create directory: `studentForm/templates/`

#### ➤ form.html

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Student Form</title>
  </head>
  <body>
    <h1>Enter Student Details</h1>
    <form method="post">
      {% csrf_token %} {{ form.as_p }}
      <input type="submit" value="Submit" />
    </form>
    <a href="/show/">Show Students</a>
  </body>
</html>
```

#### ➤ show.html

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Student List</title>
  </head>
  <body>
    <table>
      <tr>
        <th>Name</th>
        <th>Dept</th>
        <th>Roll</th>
        <th>Age</th>
        <th>Email</th>
      </tr>
      {% for student in students %}
      <tr>
        <td>{{ student.name }}</td>
        <td>{{ student.dept }}</td>
        <td>{{ student.roll }}</td>
        <td>{{ student.age }}</td>
        <td>{{ student.email }}</td>
      </tr>
      {% endfor %}
    </table>
    <a href="/">Back to Form</a>
  </body>
</html>
```

---

### 7. Create Views

In `studentForm/views.py`:

```python
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
```

---

### 8. Create URLs

Create `studentForm/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_form, name='student_form'),
    path('show/', views.show_students, name='show_students'),
]
```

---

### 9. Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 10. Run the Server

```bash
python manage.py runserver
```

Visit:  
📍 `http://127.0.0.1:8000/` – for the form  
📍 `http://127.0.0.1:8000/show/` – to view records

---

### 11. (Optional) Use the Admin Site
---

#### 11.1. Register Model in Admin Site

If you want to manage students via the Django admin interface, register the `Student` model in `studentForm/admin.py`:

```python
from .models import Student
from django.contrib import admin

admin.site.register(Student)
```
#### 11.2. Create a superuser
To use the Django admin interface to manage students:

1. Create a superuser (if you haven't already):
   ```cmd
   python manage.py createsuperuser
   ```
2. Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with your superuser credentials.
3. You can now add, edit, or delete student records via the admin UI.

---

### 12. (Optional) Add Bootstrap for Better Styling

To enhance the appearance of your forms and tables, you can include [Bootstrap](https://getbootstrap.com/) in your templates:

- In `studentForm/templates/form.html` and `show.html`, add the following line inside the `<head>` tag:

  ```html
  <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    rel="stylesheet"
  />
  ```

- Optionally, update your HTML structure to use Bootstrap classes for better layout and styling.

This step is optional but will make your app look more modern and user-friendly.

---
