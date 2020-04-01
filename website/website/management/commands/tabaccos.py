from django.core.management.base import BaseCommand, CommandError
from website.models import Recipe, Tabacco
import json


def read_mixes(file):
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data


def construct_tobacco(data):
    if type(data) == str:
        taste = data
        mark = 'любой'
    else:
        taste = data.get('taste')
        mark = data.get('mark')
        mark = mark.lower() 
    taste = taste.lower()
    try:
        return Tabacco.objects.get(Taste=taste, Mark=mark)
    except Exception:
        try:
            t = Tabacco.objects.get(Taste=taste, Mark='любой')
            t.Mark = mark
            t.Save()
        except Exception:
            Tabacco(Mark=mark, Taste=taste).save()
    return Tabacco.objects.get(Taste=taste, Mark=mark)


class Command(BaseCommand):
    help = 'Read recepies from file'

    def add_arguments(self, parser):
        parser.add_argument('mode', nargs='+', type=str)
        parser.add_argument('file', nargs='+', type=str)
        parser.add_argument('--my',
                            action='store_true',
                            dest='my',
                            default=False)

    def handle(self, *args, **options):
        if options["mode"][0] == "read":
            data = read_mixes(options["file"][0])
            if options["my"]:
                i = 0
                for r in data:
                    try:
                        t = construct_tobacco(r)
                        if t.Mark == 'darkside':
                            t.Icon = 'fas fa-space-shuttle'
                        elif t.Mark == 'sebero':
                            t.Icon = 'fas fa-paw'
                        elif t.Mark == 'element':
                            t.Icon = 'fab fa-elementor'
                        elif t.Mark == 'dailyhookah':
                            t.Icon = 'icon-support'
                        t.Mass = r.get('mass')
                        t.Have = True
                        t.save()
                        print(str(t))
                        i += 1
                    except Exception as ex:
                        print(ex.args)
                        print(str(t))
                self.stdout.write(self.style.SUCCESS(
                    f'Added {i} tabaccos'))
            else:
                i = len(Recipe.objects.all())
                for r in data:
                    try:
                        tobac_list = []
                        optional_list = []
                        flask = "water"
                        desc = ""
                        for t in r["recipe"]:
                            # R.TabaccoList.add(construct_tobacco(t))
                            tobac_list.append(construct_tobacco(t))
                        R = Recipe.objects.create(RecipeId=i, Flask=r.get(
                            'flask') or flask, Description=r.get('description') or desc)
                        R.TabaccoList.set(tobac_list)
                        if r.get("optional"):
                            for t in r["optional"]:
                                optional_list.append(construct_tobacco(t))
                        R.OptionalList.set(optional_list)
                        R.save()
                        i += 1
                        print(str(t))
                    except Exception as ex:
                        print(ex.args)
                        print(str(t))

                self.stdout.write(self.style.SUCCESS(
                    f'Added {len(data)} recipies'))
