from sys import stdout
import requests
import re
import os
import json
import zipfile,os.path
import shutil
from bs4 import BeautifulSoup

from django.template import Template, Context
from django.conf import settings

from sets import Set

keywords = ['cocos2d', 'libunity','unityengine','andengine',\
'bigworld','cryengine','spritekit','appkit', 'godot','ofappeglwindow',\
'blitz','cryengine','gamebryo','gamemaker','klayengine',\
'heroengine','havok','infernal','marmalade','rapid2d','shiva','unreal','kobold2d','libgdx']


def download_file(url,filename,totalsize):
    # NOTE the stream=True parameter
    if os.path.isfile(filename):
        return filename
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        downloadsize = 0
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
                downloadsize += 1024
                #print str(stats) + 'k',
                stdout.write("\r%.1f%%" %(downloadsize*100/totalsize))
                stdout.flush()
    stdout.write("\n")
    return filename

def check_engine(filename, chunksize=8192):
    _engine = []
    for keyword in keywords:
        i = filename.lower().find(keyword)
        #print keyword
        #print i
        if i > 0:
            print filename
            _detected = keyword
            if(keyword == 'libunity' or keyword == 'unityengine'):
                _detected = 'unity'
            if(_engine.count(_detected) == 0):
                #print 'detected in name:' + keyword
                _engine.append(_detected)
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                #print chunk
                for keyword in keywords:
                    i = chunk.lower().find(keyword)
                    if i > 0:
                        print chunk[i:i+48]
                        _detected_ = keyword
                        if(keyword == 'libunity' or keyword == 'unityengine'):
                            print keyword
                            _detected_ = 'unity'
                        if(_engine.count(_detected_) == 0):
                            print 'detected in file:' + _detected_
                            _engine.append(_detected_)
            else:
                break
    return _engine

def scan(path):
    _engine2 = []
    for root, dirs, files in os.walk(path):   
        for file in files:
            if file.endswith(".so"):
                print file
                fPath = os.path.join(root, file)
                check = check_engine(fPath)
                #print check
                for item in check:
                    #print 'check:'+item
                    #print _engine2.count(item)
                    if(_engine2.count(item) == 0):
                        #print '_engine2 add:' + item
                        _engine2.append(item)
    return _engine2

# def unzip(source_filename, dest_dir):
#     print source_filename
#     with zipfile.ZipFile(source_filename) as zf:
#         for member in zf.infolist():
#             # Path traversal defense copied from
#             # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
#             words = member.filename.split('/')
#             path = dest_dir
#             for word in words[:-1]:
#                 drive, word = os.path.splitdrive(word)
#                 head, word = os.path.split(word)
#                 if word in (os.curdir, os.pardir, ''): continue
#                 path = os.path.join(path, word)
#             zf.extract(member, path)

def unzip(source_filename, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    execCmd = u"tar zxf %s -C %s " % (source_filename, dest_dir)
    execCmd = execCmd.encode("utf-8")
    ret = os.system(execCmd)
    if ret != 0:
        os.remove(source_filename)
        return False
    else:
        return True

def get_app_list(url):
    r = requests.get(url)

    if(r.status_code is not 200):
        print 'http reqeust error, please check your network connections'
        
    #diagnose(r.text)
    print r.text
    soup = BeautifulSoup(r.text)
    app_data = {}
    applist = []

    for script in soup.find_all('script'):
        #print script.get_text()
        values = re.findall(r'var G_appData =\s*(.*?);', script.get_text(), re.DOTALL | re.MULTILINE)
        for value in values:
            app_data = json.loads(value)

    for tag in soup.find_all('div', attrs={'class':'app-rank'}):
        appitem = {}
        appitem['rank'] = tag.span.text
        app = tag.parent.parent
        for child in app.descendants:
            if child.name == 'p':
                appitem['desc']=child.span.string
        appitem['pname']=app['data-pname']
        appitem['id'] = app['data-sid']
        for data in app_data:
            if data['id'] == app['data-sid']:
                appitem['name'] = data['name']
                appitem['size'] = data['size']
                appitem['down_url'] = data['down_url']
                break
        applist.append(appitem)

    return applist

def collect_stats(url):
    detected = []
    app_list = get_app_list(url)
    for item in app_list:
        _filename = item['id']+'.apk'
        print 'Download '+item['name'] + ' start...'
        ok = False
        while ok is not True:
            download_file(item['down_url'], _filename, int(item['size']))
            unzip_folder = './' + item['id']+'/'
            ok = unzip(_filename, unzip_folder)
        engine_list = scan(unzip_folder)
        for n, i in enumerate(engine_list):
            if i == 'cocos2d':
                engine_list[n] = 'cocos2d-x'
        if(len(engine_list) == 0):
            item['engine'] = 'others'
        else:
            item['engine'] = ' '.join(engine_list)
        detected.append(item)
    return detected
    

top50_url = "http://openbox.mobilem.360.cn/app/list/" + \
"cid/2/start/0/num/100/order/weekdownload/format/rankhtml" + \
"/title/%E4%B8%8B%E8%BD%BD%E6%A6%9C?webpg=yxxz&fm=gm002_yxxz&m=4cc8407ea1de620ee85453d8cc1c771b&" + \
"m2=15db19e7da088101cc3e567600ab89fb&v=1.11.0.9&re=1&ch=600000&os=10&model=U8860&sn=4.081878922098005&cu=huawei+u8860lp+board"



#collect_stats(top50_url)
cocos2d_game = collect_stats(top50_url)
print cocos2d_game

# settings.configure()


# template = """
# <html>
# <head>
# <title>Cocos2d popularity in Top 50 games (by download) in 360 platform</title>
# </head>
# <table>
# {% for item in game_list %}
# {% if forloop.counter0|divisibleby:4 %}<tr>{% endif %}
# <td>{{ item }}</td>
# {% if forloop.counter|divisibleby:4 or forloop.last %}</tr>{% endif %}
# {% endfor %}
# </table>
# </html>
# """

# t = Template(template)

# c = Context({"game_list": cocos2d_game})
# stats = t.render(c)
# #print stats
with open("cocos2d-stats.csv", "w") as stats_file:
    stats_file.write('rank,game-name                   ,weekly-download              ,detected-engine\n')
    for game in cocos2d_game:
        stats_file.write(game['rank'])
        stats_file.write(',')
        stats_file.write(game['name'].encode('gb2312','ignore'))
        stats_file.write(',')
        stats_file.write(game['desc'].encode('gb2312','ignore'))
        stats_file.write(',')
        stats_file.write(game['engine'])
        stats_file.write('\n')
