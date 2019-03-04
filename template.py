import codecs
import os
import string
from database import getRegions, getComments, getStatRegion, getStatCity

files_path = {
    'css': {'path': 'static/css', 'name': "style.css"},
    'base': {'path': 'static', 'name': "base.html"},
    'formComment': {'path': 'static', 'name': "formAddComment.html"},
    'view': {'path': 'static', 'name': "view.html"},
    'row': {'path': 'static', 'name': "row list.html"},
    'statistics': {'path': 'static', 'name': "statistics.html"},
    'tableRegion': {'path': 'static', 'name': "tableRegion.html"},
    'tableCity': {'path': 'static', 'name': "tableCity.html"},
    'stat': {'path': 'static/js', 'name': "stat.js"},
    'addComJs': {'path': 'static/js', 'name': "addComment.js"},
    'comList': {'path': 'static/js', 'name': "comList.js"},
}


def regionHtml():
    regs = getRegions()
    html = '<option style="display:none;"></option>\n'
    for id, name in regs:
        html += '<option id={id} value={id}>{region}</option>\n'.format(**{'id': id, 'region': name})
    return html


def regionStatHTML():
    regStat = getStatRegion()
    html = ''
    for idReg, state, kol in regStat:
        row = string.Template(get_template('tableRegion'))
        html += row.substitute(idRegion=idReg, region=state, countCom=kol)
    return html


def citiesStatHTML(idRegion):
    citiesStat = getStatCity(idRegion)
    html = ''
    for city, kol in citiesStat:
        row = string.Template(get_template('tableCity'))
        html += row.substitute(city=city, countCom=kol)
    return html


def commentsHTML():
    comments = getComments()
    html = ''
    for record in comments:
        context = dict(zip(['commentid', 'surname', 'firstname', 'content', 'city', 'region'], record))
        row = string.Template(get_template('row'))
        html += row.substitute(context) + '\n'
    return html


def get_template(name):
    cur_dir = os.path.abspath(os.getcwd())
    path = os.path.join(cur_dir, files_path[name]['path'])
    filename = os.path.join(path, files_path[name]['name'])
    if not os.path.exists(path):
        raise FileNotFoundError('File {} not found at {}'.format(name, path))
    return read_html_file(filename)


def read_html_file(filename):
    with codecs.open(filename, "r", "utf-8") as f:
        html = f.read()
        return html


def getCommentHTML():
    template = string.Template(get_template('base'))
    css = get_template('css')
    regions = regionHtml()
    content = string.Template(get_template('formComment'))
    content = content.substitute(regions=regions)
    js = get_template('addComJs')
    return template.substitute(css=css, content=content, javascpipt=js)


BASE_TEMPLATE = string.Template(get_template('base'))
BASE_CSS = get_template('css')

def getBaseHTML():
    return BASE_TEMPLATE.substitute(css=BASE_CSS, content='', javascpipt='')


def getViewHTML():
    content = string.Template(get_template('view'))
    listComment = commentsHTML()
    content = content.substitute(list=listComment)
    js = get_template('comList')
    return BASE_TEMPLATE.substitute(css=BASE_CSS, content=content, javascpipt=js)


def getStatRegionsHTML():
    content = string.Template(get_template('statistics'))
    table_rowsStat = regionStatHTML()
    content = content.substitute(table_rows=table_rowsStat,head='Город')
    js = get_template('stat')
    return BASE_TEMPLATE.substitute(css=BASE_CSS, content=content, javascpipt=js)


def getStatCitiesHTML(idRegion):
    content = string.Template(get_template('statistics'))
    table_rowsStat = citiesStatHTML(idRegion)
    content = content.substitute(head='Город',table_rows=table_rowsStat)
    js = get_template('stat')
    return BASE_TEMPLATE.substitute(css=BASE_CSS, content=content, javascpipt=js)
