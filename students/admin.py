from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.urls import reverse

from .models.students import Student
from .models.groups import Group
from .models import MonthJournal


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        """Check if student is leader in any group.
        If yes, then ensure it's the same as selected group."""
        # get group where current student is a leader
        group = Group.objects.filter(leader=self.instance).first()
        if group and self.cleaned_data['student_group'] != group:
            raise ValidationError('Cтудент є старостою іншої групи.', code='invalid')

        return self.cleaned_data['student_group']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
    form = StudentFormAdmin

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})


class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        """Check if student is in this group."""
        # get students in current group
        students = Student.objects.filter(student_group=self.instance)
        if students and self.cleaned_data['leader'] not in students:
            raise ValidationError('Cтудент не належить до поточної групи.', code='invalid')

        return self.cleaned_data['leader']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_filter = ['title']
    list_per_page = 10
    search_fields = ['title', 'leader', 'notes']
    form = GroupFormAdmin

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(MonthJournal)
