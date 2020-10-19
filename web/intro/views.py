from django.views.generic import TemplateView


class IntroView(TemplateView):
    template_name = 'intro.html'
