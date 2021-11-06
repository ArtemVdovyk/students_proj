from django.shortcuts import render
from django.http import HttpResponse


# Views for Journal
def students_visits(request):
    students = (
        {'id': 1,
         'name': 'Літвінов Дмитро'},
        {'id': 2,
         'name': 'Віталій Подоба'},
    )
    return render(request, 'students/students_visits.html', {'students': students})
