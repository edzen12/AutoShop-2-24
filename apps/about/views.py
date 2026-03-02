from django.views.generic import TemplateView
from apps.about.models import AboutContent, PlusAbout, BlogAbout, Faq, Testimonials


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['about'] = AboutContent.objects.latest('-id')
        context['plusAbout'] = PlusAbout.objects.all()[:3]
        context['blogAbout'] = BlogAbout.objects.all()[:3]
        context['faq'] = Faq.objects.all()
        context['testimonials'] = Testimonials.objects.all()[:5]
        
        return context
