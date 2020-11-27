from django.views import View
from django.template.response import TemplateResponse
from .models import *
from .management.commands.tabaccos import construct_tobacco
from django.shortcuts import redirect
from django.db.models import Q


def GetHookerRecipies(username, is_super):
  tabaccos = Tabacco.objects.all()
  if not is_super:
    tabaccos = tabaccos.filter(Keepers__username=username)
  allrecepies = Recipe.objects.all()
  recepies = []
  for r in allrecepies:
    rtabacs = []
    if len(r.Tabaccos.all()) > 0:
      for t in r.Tabaccos.all():
        rtabacs.append({'name': str(t)})
        if (len(tabaccos.filter(Brand=t.Brand, Name=t.Name)) > 0):
          rtabacs[-1]['have'] = 'list-group-item-primary'
        else:
          rtabacs[-1]['have'] = 'list-group-item-danger'
    else:
      for t in r.Tastes.all():
        rtabacs.append({'taste': str(t)})
        if (len(tabaccos.filter(Tastes__Taste=t.Taste)) > 0):
          rtabacs[-1]['have'] = 'list-group-item-primary'
        else:
          rtabacs[-1]['have'] = 'list-group-item-danger'
    recepies.append({'tabaccos': rtabacs, 'value':r.price(username)})

  return sorted(recepies, key=lambda x: -x['value'])

def GetHookerTabaccos(username, is_super):
  tabaccos = Tabacco.objects.all()
  if not is_super:
    tabaccos = tabaccos.filter(Keepers__username=username)
  return [{'strength': t.Strength, 'brand': t.Brand, 'name': t.Name, 'id':t.id, 'tastes': [str(taste) for taste in t.Tastes.all()], 'icon': t.Icon.icon()} for t in tabaccos]

def GetSelectors():
  tabaccos = Tabacco.objects.all()
  tabaccos = [{'strength': t.Strength, 'brand': t.Brand, 'id':t.id, 'name': t.Name, 'tastes': [str(taste) for taste in t.Tastes.all()], 'icon': t.Icon.Icon} for t in tabaccos]
  marks = list(Tabacco.objects.values('Brand').distinct())
  marks = [m["Brand"].replace(' ','-') for m in marks]
  selectorMarks = {}
  for i,m in enumerate(marks):
    selectorMarks[m] = []
    for t in tabaccos:
      if t["brand"].replace(' ','-') == m:
        selectorMarks[m].append({'id':t['id'], 'name':t["name"]})
  return selectorMarks

def GetTabaccosStat():
  temp = Feedback.objects.all().exclude(TabaccoList=None)
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
    recepies = GetHookerRecipies(request.user.username, request.user.is_superuser)
    tabaccos = GetHookerTabaccos(request.user.username, request.user.is_superuser)
    selectorMarks = GetSelectors()
    context = {'tabaccos': tabaccos, 'recepies': recepies, 'selectors': selectorMarks}
    
    if self.template != 'statistic':
      return TemplateResponse(request, page, context=context)
    elif self.template == 'swiper':
      return TemplateResponse(request, page, context=context)
    else:
      context['feedbacks'] = GetTabaccosStat()
      return TemplateResponse(request, page, context=context)

  def post(self, request, *args, **kwargs):
    if request.path == '/add':
      if request.POST.get('input-brand') and request.POST.get('input-name'):
        id = request.POST.get('input-name')[len('taste-'):]
        id = int(id)
        t = Tabacco.objects.get(id=id)
        if request.POST.get('input-type') == "delete":
          h = Hooker.objects.get(username=request.user.username)
          if h.has_perm('website.change_tabacco'):
            t.Keepers.remove(h)

        elif request.POST.get('input-type') == "add":
          h = Hooker.objects.get(username=request.user.username)
          if h.has_perm('website.change_tabacco'):
            t.Keepers.add(h)
        t.save()
      return redirect('/add')
    elif request.path == '/stat':
      if request.POST.get('taste') and request.POST.get('mark'):
        if request.POST.get('type') == "tabac":
          name = request.POST.get('taste')
          brand = request.POST.get('mark')
          t = Tabacco.objects.get(Brand=brand, Name=name)
          h = Hooker.objects.get(username=request.user.username)
          f = Feedback(Mark=mark, RecipeList=None, Author=h)
          f.save()
          f.TabaccoList.add(t)
          f.save()

      return redirect('/stat')
