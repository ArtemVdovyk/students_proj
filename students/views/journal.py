from datetime import datetime, date
from django.views.generic.base import TemplateView
from django.urls import reverse

from .models import Student


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super().get_context_data(**kwargs)

        # перевіряємо чи передали нам місяць в параметрі
        # якщо ні - вичисляємо поточний;
        # поки що ми віддаємо лише поточний;
        today = datetime.today()
        month = date(today.year, today.month, 1)

        # обчислюємо поточний рік, попередній і наступний місяці
        # а поки прибиваємо їх статично
        context['prev_month'] = '2020-06-01'
        context['next_month'] = '2020-08-01'
        context['year'] = 2014

        # також поточний місяць;
        # змінну cur_month ми використовуватимемо пізніше в пагінації; а month_verbose в навігації помісячній;
        context['cur_month'] = '2020-07-01'
        context['month_verbose'] = 'Липень'

        # тут будемо обчислювати список днів у місяці, а поки заб'ємо статично:
        context['month-header'] = [
            {'day': 1, 'verbose': 'Пн'},
            {'day': 2, 'verbose': 'Вт'},
            {'day': 3, 'verbose': 'Ср'},
            {'day': 4, 'verbose': 'Чт'},
            {'day': 5, 'verbose': 'Пт'}
        ]

        # витягуємо усіх студентів посортованих по прізвищу
        queryset = Student.objects.order_by('last_name')

        # це адреса для посту AJAX запиту, як бачите, ми робитимемо його на цю ж в'юшку;
        # в'юшка журналу буде і показувати журнал і обслуговувати запити типу пост на оновлення журналу
        update_url = reverse('journal')

        # пробігаємось по усіх студентах і збираємо необхідні дані
        students = []
        for student in queryset:
            # TODO: витягуємо журнал для студента і вибраного місяця

            # набиваємо дні для студента
            days = []
            for day in range(1, 31):
                days.append({
                    'day': day,
                    'present': True,
                    'date': date(2020, 7, day).strftime('%Y-%m-%d'),
                })

            # набиваємо усі решту даних для студента
            students.append({
                'fullname': f'{student.last_name} {student.first_name}',
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        # застосовуємо пагінацію до списку студентів
        context = paginate(student, 10, self.request, context, var_name='students')

        # повертаємо оновлений словник із даними
        return context
