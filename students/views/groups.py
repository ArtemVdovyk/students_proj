from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView
from datetime import datetime

from students.models.groups import Group

from ..util import paginate, get_current_group


# Views for Groups
def groups_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        groups = current_group
    else:
        # otherwise, show all students
        groups = Group.objects.all()

    # try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by == '':
        groups = groups.order_by('title')
    if order_by in ('title', 'leader', 'id'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    # apply pagination, 3 students per page
    context = paginate(groups, 3, request, {}, var_name='groups')

    return render(request, 'students/groups_list.html', context)


class GroupForm(ModelForm):

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # add form or edit form
        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False

        # set form tag attributes
        if add_form:
            self.helper.form_action = reverse('groups_add')
        else:
            reverse_groups_edit = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})
            self.helper.form_action = reverse_groups_edit
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-12 col-form-label'
        self.helper.field_class = 'col-sm-10'

        # add button
        if add_form:
            submit = Submit('add_button', 'Додати')
        else:
            submit = Submit('save_button', 'Зберегти')
        self.helper.layout.append(FormActions(submit, Submit('cancel_button', 'Скасувати', css_class='btn_danger')
                                              ))


class BaseGroupFormView:

    def get_success_url(self):
        return f"{reverse('groups')}?status_message=Зміни успішно збережено!"

    def post(self, request, *args, **kwargs):
        # handle cancel button
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('group') + '?status_message=Зміни скасовано!')
        else:
            return super().post(request, *args, **kwargs)


class GroupAddView(BaseGroupFormView, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'


class GroupUpdateView(BaseGroupFormView, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        return f"{reverse('groups')}?status_message=Групу успішно видалено!"
