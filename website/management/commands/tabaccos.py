from django.core.management.base import BaseCommand, CommandError
from website.models import *
import json
from traceback import *


def read(file):
    with open(file, 'rb') as f:
        data = json.load(f)
    return data

def write(file, data):
    with open(file, 'wb') as f:
        f.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def construct_taste(data):
    is_new = False
    try:
        t = Taste.objects.get(Taste=data)
    except Exception:
        t = Taste(Taste=data)
        is_new = True
        t.save()
    return t, is_new

def construct_tobacco(data):
    tastes = []
    for taste in data.get('taste'):
        tastes.append(construct_taste(taste)[0])

    name = data.get('name')
    brand = data.get('brand').lower()
    is_new = False
    try:
        t = Tabacco.objects.get(Name=name)
    except Exception:
        t = Tabacco(Name=name)
        t.save()
        is_new = True
    t.Tastes.set(tastes)
    t.Brand = brand
    t.Strength = data.get('strength')
    t.Icon = Icon(Icon=Icon.choose_icon(brand))
    t.Icon.save()
    t.save()
    return t, is_new

def construct_recipe(data):
    # TODO add create with tabaccos not tastes
    tastes = [construct_taste(t)[0] for t in data.get('tastes')]
    t = ''
    is_new = False
    try:
        t = Recipe(Tastes=tastes)
    except Exception:
        t = Recipe()
        t.save()
        is_new = True
    t.Tastes.set(tastes)
    t.Description = data.get('desc')
    t.Flask = data.get('flask')
    t.save()
    return t, is_new

class Command(BaseCommand):
    help = 'Read, write, migrate recepies from, to file'

    def add_arguments(self, parser):
        parser.add_argument('mode', nargs=1, type=str, help="Can be read, write or migrate")
        parser.add_argument('file', nargs='+', type=str, help="Processing files")
        parser.add_argument('-t', '--taste',
                            action='store_true',
                            dest='taste',
                            default=False, help="Process taste")
        parser.add_argument('-b', '--tabacco',
                            action='store_true',
                            dest='tabacco',
                            default=False, help="Process tabacco")
        parser.add_argument('-r', '--recipe',
                            action='store_true',
                            dest='recipe',
                            default=False, help="Process recipe")
        parser.add_argument('-u', '--users',
                            action='store_true',
                            dest='users',
                            default=False, help="Process users")

    def handle(self, *args, **options):
        if options["mode"][0] == "read":
            data = read(options["file"][0])
            i = 0
            one_option = False
            if options["taste"]:
                one_option = True
                for t in data:
                    t, j = construct_taste(t)
                    i += int(j)
                    print(("Created: " if j else "Already exist: ") + str(t))

                self.stdout.write(self.style.SUCCESS(
                    f'Added {i} tastes'))
            elif options["tabacco"]:
                if one_option:
                    self.stdout.write(self.style.WARNING(f'Previous option already apply! Tabacco option doesn\'t apply'))
                    return
                one_option = True
                for r in data:
                    t = ''
                    try:
                        t, j = construct_tobacco(r)
                        print(("Created: " if j else "Already exist: ") + str(t))
                        i += int(j)
                    except Exception as ex:
                        print(ex.args)
                        print(format_exc())
                        if t in locals():
                            print(str(t))
                self.stdout.write(self.style.SUCCESS(
                    f'Added {i} tabaccos'))
            elif options["recipe"]:
                if one_option:
                    self.stdout.write(self.style.WARNING(f'Previous option already apply! Recipe option doesn\'t apply'))
                    return
                one_option = True
                for r in data:
                    t = ''
                    try:
                        t, j = construct_recipe(r)
                        print(("Created: " if j else "Already exist: ") + str(t))
                        i += int(j)
                    except Exception as ex:
                        print(ex.args)
                        print(format_exc())
                        if t in locals():
                            print(str(t))
                self.stdout.write(self.style.SUCCESS(
                    f'Added {i} recipes'))
        elif options["mode"][0] == "write":
            write(options["file"][0], [r.toJson() for r in Recipe.objects.all()])
            write(options["file"][1], [r.toJson() for r in Tabacco.objects.all()])
            write(options["file"][2], [r.Taste for r in Taste.objects.all()])
        elif options["mode"][0] == "migrate":
            if options["taste"]:
                data = read(options["file"][0])
                tastes = []
                for d in data:
                    if d["mark"] == "any":
                        tastes.append(d["taste"])
                write(options["file"][1], tastes)
            elif options["tabacco"]:
                data = read(options["file"][0])
                tabaccos = []
                for d in data:
                    if d["mark"] != "any":
                        tabaccos.append({
                            'taste':[], 
                            'brand':d["mark"],
                            'name':d["taste"],
                            'strength':-1,
                        })
                write(options["file"][1], tabaccos)
            elif options["recipe"]:
                data = read(options["file"][0])
                recipes = [
                    {"flask":d["flask"],
                    "desc":d["desc"],
                    "tastes": [t["taste"] for t in d["tabaccos"]]}  
                    for d in data]
                write(options["file"][1], recipes)