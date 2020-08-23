from django.views import View
from django.template.response import TemplateResponse
from website.models import Recipe, Tabacco, Feedback
from website.management.commands.tabaccos import construct_tobacco
from django.shortcuts import redirect
from django.db.models import Q


# Create your views here.

def GetRecipies():
    tabaccos = Tabacco.objects.filter(Have=True).all()
    recepies = Recipe.objects.all()

    recepies = [{'tabaccos': [{'taste': str(t),
                               'have': 'list-group-item-primary'
                               if ((t.Mark == 'любой' and len(tabaccos.filter(Taste=t.Taste)) > 0) or len(tabaccos.filter(Mark=t.Mark, Taste=t.Taste)) > 0)
                               else 'list-group-item-danger'} for t in e.TabaccoList.all()],
                 'value': e.price()}
                for e in recepies]
    return recepies


class HookahIndex(View):

    template = 'index'
    tabaccos = ''
    recepies = ''

    def get(self, request, *args, **kwargs):
        page = self.template + '.html'
        if self.template != 'statistic':
            recepies = GetRecipies()
            HookahIndex.recepies = sorted(recepies, key=lambda x: -x['value'])
            tabaccos = Tabacco.objects.all().filter(Have=True)
            HookahIndex.tabaccos = [{'mark': t.Mark, 'taste': t.Taste, 'icon': t.Icon, 'mass': t.Mass if t.Mass != 0 else None}
                                    for t in tabaccos]
            return TemplateResponse(request, page, context={'tabaccos': HookahIndex.tabaccos, 'recepies': HookahIndex.recepies})
        else:
            temp = Feedback.objects.all().exclude(TabaccoMark=None)
            feedbacks = {}
            for f in temp:
              if f.TabaccoMark in feedbacks:
                feedbacks[f.TabaccoMark]["count"] += 1
                feedbacks[f.TabaccoMark]["mark"] += f.Mark
              else:
                feedbacks[f.TabaccoMark] = {"count":1,"mark":f.Mark}
            
            for f in feedbacks:
              f["mark"] /= f["count"]
              
            return TemplateResponse(request, page, context={'feedbacks': feedbacks})

    def post(self, request, *args, **kwargs):

        if request.path == '/add':
          if request.POST.get('type') == "delete":
            taste = request.POST.get('taste')
            mark = request.POST.get('mark')
            t = Tabacco.objects.get(Mark=mark, Taste=taste)
            t.Have = False
            t.save()

          else:
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

        return redirect('/add')
