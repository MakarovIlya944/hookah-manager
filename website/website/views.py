from django.views import View
from django.template.response import TemplateResponse
from website.models import Recipe, Tabacco
from website.management.commands.tabaccos import construct_tobacco
from django.shortcuts import redirect


# Create your views here.


class HookahIndex(View):

    template = 'index'
    tabaccos = ''
    recepies = ''

    def get(self, request, *args, **kwargs):
        recepies = Recipe.objects.all()
        recepies = [{'tabaccos': [{'taste': str(t),
                                   'have': 'list-group-item-primary' if t.Have else 'list-group-item-danger'} for t in e.TabaccoList.all()],
                     'value': e.price()}
                    for e in recepies]
        HookahIndex.recepies = sorted(recepies, key=lambda x: -x['value'])
        tabaccos = Tabacco.objects.all().filter(Have=True)
        HookahIndex.tabaccos = [{'mark': t.Mark, 'taste': t.Taste, 'icon': t.Icon, 'mass': t.Mass if t.Mass != 0 else None}
                                for t in tabaccos]
        page = "index.html" if self.template == 'index' else "add.html"
        return TemplateResponse(request, page, context={'tabaccos': HookahIndex.tabaccos, 'recepies': HookahIndex.recepies})

    def post(self, request, *args, **kwargs):

        if HookahIndex.template == 'add':
            mass = request.POST.get('mass')
            taste = request.POST.get('taste')
            mark = request.POST.get('mark')
            # if mass == '' or taste == '' or mark == '':
            #     return TemplateResponse(request, "index.html",
            #                             context={'tabaccos': HookahIndex.tabaccos,
            #                                      'recepies': HookahIndex.recepies,
            #                                      'error': {'mark': mark,
            #                                                'taste': taste,
            #                                                'mass': mass}})
            t = construct_tobacco({'mark': mark, 'taste': taste})
            t.Mass = mass
            t.Have = True
            t.save()

        return redirect('/')
