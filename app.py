import cgi
from template import getCommentHTML,getViewHTML,getStatRegionsHTML,getStatCitiesHTML,getBaseHTML
from database import getCities, insertNewComment, deleteComment
from wsgiref.simple_server import make_server


class App():

    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        url = environ['PATH_INFO']

        if url in self.routes:
            handler = self.routes[url]
        else:
            handler = App.not_founded_handler
        data = handler(environ)
        status = '200 OK'
        response_headers = [
            ('Content-type', 'text/html'),
            ('Content-Length', str(len(data)))
        ]

        start_response(status, response_headers)
        return iter([data])

    def add_route(self, url):
        def wrapper(handler):
            self.routes[url] = handler
        return wrapper

    @staticmethod
    def not_founded_handler(environ):
        html = getBaseHTML()
        return str.encode(html,'utf-8')


application = App()


@application.add_route('/comment/')
def showCommentPage(environ):
    html = getCommentHTML()
    return str.encode(html,'utf-8')


@application.add_route('/view/')
def showViewtPage(environ):
    html = getViewHTML()
    return str.encode(html, 'utf-8')


@application.add_route('/stat/')
def showStatPage(environ):
    d = cgi.parse_qs(environ['QUERY_STRING'])
    idRegion = d.get('idRegion')
    if idRegion:
        if isinstance(idRegion,list):
            idRegion = idRegion[0]
        html = getStatCitiesHTML(idRegion)
    else:
        html = getStatRegionsHTML()
    return str.encode(html, 'utf-8')


@application.add_route('/save/')
def saveComment(env):
    if env['REQUEST_METHOD'] == 'POST':
        post = cgi.FieldStorage(
            fp=env['wsgi.input'],
            environ=env,
            keep_blank_values=1
        )

        surname = post['surname'].value
        first_name = post['first_name'].value
        middle_name = post['middle_name'].value
        region = post['region'].value
        city = post['city'].value
        phone = post['phone'].value
        email = post['email'].value
        comment = post['comment'].value
        rez = insertNewComment(surname, first_name,middle_name,region,city,phone,email,comment)
        return str.encode(rez,'utf-8')


@application.add_route('/get_city/')
def getCity(env):
    if env['REQUEST_METHOD'] == 'POST':
        post = cgi.FieldStorage(
            fp=env['wsgi.input'],
            environ=env,
            keep_blank_values=1
        )
        cities = getCities(post['region_id'].value)

        html = '<option style="display:none;"></option>\n'
        for id_city, city, id_region in cities:
            html += '<option id={id} value={id}>{region}</option>\n'.format(**{'id': id_city, 'region': city})
        return str.encode(html,'utf-8')


@application.add_route('/delete_comment/')
def getCity(env):
    if env['REQUEST_METHOD'] == 'POST':
        post = cgi.FieldStorage(
            fp=env['wsgi.input'],
            environ=env,
            keep_blank_values=1
        )
        idComment = post['idComment'].value
        rez = deleteComment(idComment)
        return str.encode(rez,'utf-8')


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()