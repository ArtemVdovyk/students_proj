from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.views.generic.edit import FormView


class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # call original initializator
        super().__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper(self)

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('send_button', 'Надіслати'))

    from_email = forms.EmailField(label="Ваша Емейл Адреса")
    subject = forms.CharField(label="Заголовок листа",
                              max_length=128
                              )
    message = forms.CharField(label="Текст повідомлення",
                              max_length=2560,
                              widget=forms.Textarea
                              )


def contact_admin(request):
    # check if form was posted
    if request.method == 'POST':
        # create a form instance and populate in with data from the request
        form = ContactForm(request.POST)

        # check whether user data is valid
        if form.is_valid():
            # send email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [settings.ADMIN_EMAIL])
            except Exception:
                message = 'Під час відправки листа виникла непередбачувана помилка. ' \
                          'Спробуйте скористатись даною формою пізніше'
            else:
                message = 'Повідомлення успішно надіслане!'

            # redirect to same contact page with success message
            return HttpResponseRedirect(f"{reverse('contact_admin')}?status_message={message}")
        # if there was not POST render blank form
    else:
        form = ContactForm()
        return render(request, 'contact_admin/form.html', {'form': form})


# class ContactView(FormView):
#     template_name = 'contact_form.html'
#     form_class = ContactForm
#     success_url = '/email-sent/'
#
#     def form_valid(self, form):
#         """This method is called for valid data"""
#         subject = form.cleaned_data['subject']
#         message = form.cleaned_data['message']
#         from_email = form.cleaned_data['from_email']
#
#         send_mail(subject, message, from_email, ['admin@gmail.com'])
#
#         return super().form_valid(form)