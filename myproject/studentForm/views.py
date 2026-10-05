import csv
import io

from django.http import HttpResponse
from django.shortcuts import render, redirect

import vobject

from .forms import StudentForm
from .models import Student

CSV_FIELDS = ['name', 'dept', 'roll', 'age', 'email']

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

def export_vcards(request):
    cards = []
    for student in Student.objects.all():
        card = vobject.vCard()
        card.add('uid').value = f'student-{student.pk}@vgp'
        card.add('fn').value = student.name
        card.add('n').value = vobject.vcard.Name(family=student.name)
        card.add('email').value = student.email
        card.add('note').value = (
            f'Dept: {student.dept}; Roll: {student.roll}; Age: {student.age}'
        )
        cards.append(card.serialize())
    response = HttpResponse(''.join(cards), content_type='text/vcard')
    response['Content-Disposition'] = 'attachment; filename="students.vcf"'
    return response

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.DictWriter(response, fieldnames=CSV_FIELDS)
    writer.writeheader()
    for student in Student.objects.all():
        writer.writerow({
            'name': student.name,
            'dept': student.dept,
            'roll': student.roll,
            'age': student.age,
            'email': student.email,
        })
    return response

def import_csv(request):
    errors = []
    if request.method == 'POST':
        upload = request.FILES.get('file')
        if not upload:
            errors.append('No file uploaded.')
        else:
            try:
                reader = csv.DictReader(io.TextIOWrapper(upload.file, encoding='utf-8'))
            except UnicodeDecodeError:
                reader = None
                errors.append('File must be UTF-8 encoded CSV.')
            if reader is not None:
                if not reader.fieldnames or not set(CSV_FIELDS) <= set(reader.fieldnames):
                    errors.append(f'CSV must have header row: {",".join(CSV_FIELDS)}.')
                else:
                    for lineno, row in enumerate(reader, start=2):
                        form = StudentForm(data={k: row.get(k, '') for k in CSV_FIELDS})
                        if form.is_valid():
                            form.save()
                        else:
                            details = '; '.join(
                                f'{field}: {", ".join(msgs)}'
                                for field, msgs in form.errors.items()
                            )
                            errors.append(f'Row {lineno}: {details}')
                    if not errors:
                        return redirect('show_students')
    return render(request, 'import.html', {'errors': errors})
