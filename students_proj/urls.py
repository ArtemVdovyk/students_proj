from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from students.views import students, groups, journal

urlpatterns = [
    # Students urls
    path('', students.students_list, name='home'),
    path('students/add/', students.students_add, name='students_add'),
    path('students/<int:sid>/edit/', students.students_edit, name='students_edit'),
    path('students/<int:sid>/delete/', students.students_delete, name='students_delete'),

    # Groups urls
    path('groups/', groups.groups_list, name='groups'),
    path('groups/add/', groups.groups_add, name='groups_add'),
    path('groups/<int:gid>/edit/', groups.groups_edit, name='groups_edit'),
    path('groups/<int:gid>/delete/', groups.groups_delete, name='groups_delete'),

    # Journal urls
    path('journal/', journal.students_visits, name='journal'),


    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
