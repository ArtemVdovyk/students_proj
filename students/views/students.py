from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from datetime import datetime

from students.models.students import Student
from students.models.groups import Group


# Views for Students
def students_list(request):
    students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by == '':
        students = students.order_by('last_name')
    if order_by in ('last_name', 'first_name', 'ticket', 'id'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page result.
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:
            # errors collection
            errors = {}
            # data for student object
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = "Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = "Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = "Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = "введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = "Номер білету є обов'язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = "Оберіть групу для студента"
            else:
                group = Group.objects.filter(pk=student_group).first()
                if group:
                    data['student_group'] = group
                else:
                    errors['student_group'] = "Оберіть коректну групу"

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo

            # save student
            if not errors:
                # create student object
                student = Student(**data)
                # save it to database
                student.save()
                # redirect user to students list
                return HttpResponseRedirect(f"{reverse('home')}?status_message=Студента {data['first_name']} "
                                            f"{data['last_name']} успішно додано!")
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'),
                                                                      'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(f"{reverse('home')}?status_message=Додавання студента скасовано!")
    else:
        # initial form render
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})


class StudentUpdateForm(ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout.append(FormActions(Submit('add_button', 'Зберегти'),
                                              Submit('cancel_button', 'Скасувати', css_class='btn-danger')
                                              ))


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return f"{reverse('home')}?status_message=Студента успішно збережено!"

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(f"{reverse('home')}?status_message=Редагування студента відмінено!")
        else:
            return super().post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return f"{reverse('home')}?status_message=Студента успішно видалено!"
