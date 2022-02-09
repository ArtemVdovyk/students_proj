import datetime
import date
from django.views.generic.base import TemplateView


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
        