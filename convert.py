import json

def convert_spectrum():
  with open('class.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
  res = []
  for l in lines:
    l = l.replace('\n','')
    res.append({
      "brand": "spectrum",
      "name": l.split(',')[0],
      "taste": l.split(',')[1].split(' '),
      "strength": 4
    })
  with open('class.json', 'wb') as f:
    f.write(json.dumps(res,ensure_ascii=False).encode('utf-8'))

  with open('hard.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
  res = []
  for l in lines:
    l = l.replace('\n','')
    res.append({
      "brand": "spectrum hard",
      "name": l.split(',')[0],
      "taste": l.split(',')[1].split(' '),
      "strength": 6
    })
  with open('hard.json', 'wb') as f:
    f.write(json.dumps(res,ensure_ascii=False).encode('utf-8'))

def convert_sever():
  with open('sever.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
  res = []
  for l in lines:
    l = l.replace('\n','')
    res.append({
      "brand": "sever",
      "name": l.split(',')[0],
      "taste": l.split(',')[1].split(' '),
      "strength": 4
    })
  with open('hard.json', 'wb') as f:
    f.write(json.dumps(res,ensure_ascii=False).encode('utf-8'))

def convert_elment_air():
  with open('a', 'r', encoding='utf-8') as f:
    lines = f.readlines()
  res = []
  for l in lines:
    l = l.replace('\n','')
    res.append({
      "brand": "element-air",
      "name": l.split(',')[0].lower(),
      "taste": l.split(',')[1].split(' '),
      "strength": 4
    })
  with open('a.json', 'wb') as f:
    f.write(json.dumps(res,ensure_ascii=False).encode('utf-8'))

def convert_b3():
  with open('b.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
  res = []
  for l in lines:
    l = l.replace('\n','')
    res.append({
      "brand": "b3",
      "name": l.split('-')[0].lower(),
      "taste": l.split('-')[1].split(','),
      "strength": 3
    })
  with open('a.json', 'wb') as f:
    f.write(json.dumps(res,ensure_ascii=False).encode('utf-8'))

if __name__ == '__main__':
  convert_b3()