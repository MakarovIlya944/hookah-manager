from django.views import View
from django.template.response import TemplateResponse
from .models import *
from .management.commands.tabaccos import construct_tobacco
from django.shortcuts import redirect
from django.db.models import Q


def GetHookerRecipies(username):
  tabaccos = Tabacco.objects.filter(Keepers__username=username)
  allrecepies = Recipe.objects.all()
  recepies = []
  for r in allrecepies:
    rtabacs = []
    if r.Tabaccos:
      for t in r.Tabaccos.all():
        rtabacs.append({'name': str(t)})
        if (len(tabaccos.filter(Brand=t.Brand, Name=t.Name)) > 0):
          rtabacs[-1]['have'] = 'list-group-item-primary'
        else:
          rtabacs[-1]['have'] = 'list-group-item-danger'
    else:
      rtabacs.append({'taste': str(t)})
      if (len(tabaccos.filter(Taste__Taste=t.Taste)) > 0):
        rtabacs[-1]['have'] = 'list-group-item-primary'
      else:
        rtabacs[-1]['have'] = 'list-group-item-danger'
    recepies.append({'tabaccos': rtabacs, 'value':r.price(username)})

  return sorted(recepies, key=lambda x: -x['value'])

def GetHookerTabaccos(username):
  tabaccos = Tabacco.objects.filter(Keepers__username=username)
  return [{'strength': t.Strength, 'brand': t.Brand, 'taste': str(t.Tastes), 'icon': t.Icon, 'mass': t.Mass if t.Mass != 0 else None} for t in tabaccos]

def GetSelectors():
  tabaccos = Tabacco.objects.all()
  tabaccos = [{'strength': t.Strength, 'brand': t.Brand, 'taste': str(t.Tastes), 'icon': t.Icon, 'mass': t.Mass if t.Mass != 0 else None} for t in tabaccos]
  marks = list(Tabacco.objects.values('Brand').distinct())
  marks = [m["Brand"] for m in marks]
  selectorMarks = {}
  for i,m in enumerate(marks):
    selectorMarks[m] = []
    for t in tabaccos:
      if t["brand"] == m:
        selectorMarks[m].append(t["taste"])
  return selectorMarks

def GetTabaccosStat():
  temp = Feedback.objects.all().exclude(TabaccoBrand=None)
  feedbacks = []
  for f in temp:
    for el in feedbacks:
      if el["title"] == f.TabaccoBrand.short():
        el["count"] += 1
        el["mark"] += f.Mark
        break
    else:
      feedbacks.append({"title":f.TabaccoBrand.short() ,"count":1,"mark":f.Mark})
  for f in feedbacks:
    f["mark"] /= f["count"]

class HookahIndex(View):

  template = 'index'

  def get(self, request, *args, **kwargs):
    page = self.template + '.html'
    recepies = GetHookerRecipies(request.user.username)
    tabaccos = GetHookerTabaccos(request.user.username)
    selectorMarks = GetSelectors()
    context = {'tabaccos': tabaccos, 'recepies': recepies, 'selectors': selectorMarks}
    
    if self.template != 'statistic':
      return TemplateResponse(request, page, context=context)
    else:
      context['feedbacks'] = GetTabaccosStat()
      return TemplateResponse(request, page, context=context)

  def post(self, request, *args, **kwargs):
    if request.path == '/add':
      if request.POST.get('taste') and request.POST.get('mark'):
        if request.POST.get('type') == "delete":
          taste = request.POST.get('taste')
          mark = request.POST.get('mark')
          t = Tabacco.objects.get(Mark=mark, Tastes=taste)
          t.Have = False
          t.save()

        else:
          mass = request.POST.get('mass')
          taste = request.POST.get('taste')
          mark = request.POST.get('mark')
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
          t = Tabacco.objects.get(Tastes=taste, Mark=mark)
          f = Feedback(TabaccoMark=t, Mark=mass, RecipeMark=None).save()

      return redirect('/stat')

