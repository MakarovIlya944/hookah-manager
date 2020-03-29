from django.views import View
from django.template.response import TemplateResponse
from hookah.models import Recipe, Tabacco
from hookah.management.commands.tabaccos import construct_tobacco
from django.shortcuts import redirect


# Create your views here.


class HookahIndex(View):

    tabaccos = ''
    recepies = ''

    def get(self, request, *args, **kwargs):
        recepies = Recipe.objects.all()
        recepies = [{'tobaccos': [{'taste': str(t),
                                   'have': 'list-group-item-primary' if t.Have else 'list-group-item-danger'} for t in e.TabaccoList.all()],
                     'value': e.price()}
                    for e in recepies]
        HookahIndex.recepies = sorted(recepies, key=lambda x: -x['value'])
        tabaccos = Tabacco.objects.all().filter(Have=True)
        HookahIndex.tabaccos = [{'mark': t.Mark, 'taste': t.Taste, 'icon': t.Icon, 'mass': t.Mass if t.Mass != 0 else None}
                                for t in tabaccos]
        return TemplateResponse(request, "hookah/index.html", context={'tabaccos': HookahIndex.tabaccos, 'recepies': HookahIndex.recepies})

    def post(self, request, *args, **kwargs):

        mass = request.POST.get('mass')
        taste = request.POST.get('taste')
        mark = request.POST.get('mark')
        # if mass == '' or taste == '' or mark == '':
        #     return TemplateResponse(request, "hookah/index.html",
        #                             context={'tabaccos': HookahIndex.tabaccos,
        #                                      'recepies': HookahIndex.recepies,
        #                                      'error': {'mark': mark,
        #                                                'taste': taste,
        #                                                'mass': mass}})
        t = construct_tobacco({'mark': mark, 'taste': taste})
        t.Mass = mass
        t.Have = True
        t.save()

        return redirect('/hookah')
