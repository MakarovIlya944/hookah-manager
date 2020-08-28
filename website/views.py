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
                               if ((t.Mark == 'any' and len(tabaccos.filter(Taste=t.Taste)) > 0) or len(tabaccos.filter(Mark=t.Mark, Taste=t.Taste)) > 0)
                               else 'list-group-item-danger'} for t in e.TabaccoList.all()],
                 'value': e.price()}
                for e in recepies]
    return recepies


class HookahIndex(View):

    template = 'index'
    tabaccos = ''
    recepies = ''
    selectorMarks = ''

    def get(self, request, *args, **kwargs):
        page = self.template + '.html'
        recepies = GetRecipies()
        HookahIndex.recepies = sorted(recepies, key=lambda x: -x['value'])
        tabaccos = Tabacco.objects.all()
        HookahIndex.tabaccos = [{'mark': t.Mark, 'taste': t.Taste, 'icon': t.Icon, 'have': t.Have, 'mass': t.Mass if t.Mass != 0 else None}
                                for t in tabaccos]
        marks = list(Tabacco.objects.values('Mark').distinct())
        marks = [m["Mark"] for m in marks]
        HookahIndex.selectorMarks = {}
        for i,m in enumerate(marks):
          HookahIndex.selectorMarks[m] = []
          for t in HookahIndex.tabaccos:
            if t["mark"] == m:
              HookahIndex.selectorMarks[m].append(t["taste"])
        
        if self.template != 'statistic':
            return TemplateResponse(request, page, context={'tabaccos': HookahIndex.tabaccos, 'recepies': HookahIndex.recepies, 'selectors': HookahIndex.selectorMarks})
        else:
            temp = Feedback.objects.all().exclude(TabaccoMark=None)
            feedbacks = []
            for f in temp:
              for el in feedbacks:
                if el["title"] == f.TabaccoMark.short():
                  el["count"] += 1
                  el["mark"] += f.Mark
                  break
              else:
                feedbacks.append({"title":f.TabaccoMark.short() ,"count":1,"mark":f.Mark})
            for f in feedbacks:
              f["mark"] /= f["count"]
              
            # sorted(feedbacks, key=lambda x: x["mark"])
            return TemplateResponse(request, page, context={'feedbacks': feedbacks, 'tabaccos': HookahIndex.tabaccos, 'recepies': HookahIndex.recepies, 'selectors': HookahIndex.selectorMarks})

    def post(self, request, *args, **kwargs):

        if request.path == '/add':
          if request.POST.get('taste') and request.POST.get('mark'):
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
        elif request.path == '/stat':
          if request.POST.get('taste') and request.POST.get('mark'):
            if request.POST.get('type') == "tabac":
              mass = request.POST.get('mass')
              taste = request.POST.get('taste')
              mark = request.POST.get('mark')
              t = Tabacco.objects.get(Taste=taste, Mark=mark)
              f = Feedback(TabaccoMark=t, Mark=mass, RecipeMark=None).save()

          return redirect('/stat')

