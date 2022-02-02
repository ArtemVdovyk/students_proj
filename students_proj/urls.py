from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from students.views import students, groups, journal, contact_admin

urlpatterns = [
    # Students urls
    path('', students.students_list, name='home'),
    path('students/add/', students.students_add, name='students_add'),
    path('students/<int:pk>/edit/', students.StudentUpdateView.as_view(), name='students_edit'),
    path('students/<int:pk>/delete/', students.StudentDeleteView.as_view(), name='students_delete'),

    # Groups urls
    path('groups/', groups.groups_list, name='groups'),
    path('groups/add/', groups.GroupAddView.as_view(), name='groups_add'),
    path('groups/<int:pk>/edit/', groups.GroupUpdateView.as_view(), name='groups_edit'),
    path('groups/<int:pk>/delete/', groups.GroupDeleteView.as_view(), name='groups_delete'),

    # Journal urls
    path('journal/', journal.students_visits, name='journal'),

    # Contact Admin Form
    path('contact-admin/', contact_admin.contact_admin, name='contact_admin'),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
