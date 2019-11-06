from django.views.generic import TemplateView
from photocontest.models import Participants

class IndexPageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['participants'] = Participants.objects.all()
        print("participants", context['participants'])
        return context


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
