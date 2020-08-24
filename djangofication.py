from os import walk

swiper = [
'<div class="swiper-wrapper">',
'    {% for element in recepies %}',
'    <div class="swiper-slide" style="padding: 100px;">',
'',
'        <ul class="list-group">',
'            {% for tabac in element.tobaccos %}',
'            <li class="list-group-item {{ tabac.have }}"><span>{{ tabac.taste }}</span></li>',
'            {% endfor %}',
'        </ul>',
'    </div>',
'    {% endfor %}',
'',
'</div>',
'<div class="swiper-button-prev"></div>',
'<div class="swiper-button-next"></div>'
]

def index():
    lines = []
    end_heads = -1
    styles = []
    style_i = -1
    style_n = 0
    with open('./index.html', 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        style = line.find('rel="stylesheet" href=')
        heads = line.find('</head>')
        if line.find('</title>') != -1:
            lines[i] += '{% load static %}\n'
        elif style != -1:
            if line.find('https://') != -1:
                continue
            style_i = i if style_i == -1 else style_i
            styles.append('<link rel="stylesheet" href="{% static ' + line[style+22:-2] + ' %}">')
            style_n += 1
        elif heads != -1:
            end_heads = heads
        elif line.find('<div class="swiper-wrapper">') != -1:
            swiper_i = i

    new_lines = lines[:style_i]
    new_lines.extend(styles)

    new_lines.extend(lines[style_i+style_n:swiper_i])
    
    new_lines.extend(swiper)
    new_lines.extend(lines[swiper_i+8:])
    print('end')

def main():
    files = {}
    
    for (dirpath, dirnames, filenames) in walk('.'):
        if dirpath == '.':
            files['html'] = filenames
        # if dirpath == './assets':

    index()


if __name__ == '__main__':
    main()