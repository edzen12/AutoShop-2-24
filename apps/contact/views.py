from django.views.generic import FormView
from django.urls import reverse_lazy
from apps.contact.models import ContactPage
from apps.contact.forms import ContactRequestForm


class ContactView(FormView):
    template_name = 'pages/contact.html'
    success_url = reverse_lazy('contact')
    form_class = ContactRequestForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contactPage'] = ContactPage.objects.latest('-id')
        return context