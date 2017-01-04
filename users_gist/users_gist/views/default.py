from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..security import check_credentials
from passlib.apps import custom_app_context as pwd_context


@view_config(route_name="home", renderer="../templates/home.jinja2")
def home_list(request):
    """View for the home page."""
    try:
        query = request.dbsession.query(MyModel)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'users': query}


@view_config(route_name='login',
             renderer='../templates/login.jinja2',
             require_csrf=False)
def login(request):
    """Login View."""
    if request.method == 'POST':
        username = request.params.get('Username', '')
        password = request.params.get('Password', '')
        if check_credentials(username, password, request):
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('home'),
                             headers=headers)
    return {}


@view_config(route_name="user", renderer="../templates/user.jinja2", permission="write")
def detail(request):
    """View for the detail page."""
    query = request.dbsession.query(MyModel)
    user_dict = query.filter(MyModel.user_name == request.matchdict['user']).first()
    import pdb; pdb.set_trace()
    return {"user": user_dict}


@view_config(route_name="register", renderer="../templates/register.jinja2")
def create(request):
    """View for new entry page."""
    if request.method == "POST":
        username = request.params.get('Username', '')
        password = request.params.get('Password', '')

        first_name = request.params.get('first_name', '')
        last_name = request.params.get('last_name', '')

        email = request.params.get('email', '')
        food = request.params.get('food', '')

        new_model = MyModel(first_name=first_name,
                            last_name=last_name,
                            user_name=username,
                            email=email,
                            fav_food=food,
                            password=pwd_context.hash(password))
        request.dbsession.add(new_model)
        return HTTPFound(location=request.route_url('home'))
    return {}


# @view_config(route_name="update", renderer="../templates/edit_entry.jinja2")
# def update(request):
#     """View for update page."""
#     if request.method == "POST":
#         title = request.POST["title"]
#         body = request.POST["body"]
#         creation_date = datetime.date.today().strftime("%m/%d/%Y")
#         query = request.dbsession.query(Entry)
#         post_dict = query.filter(Entry.id == request.matchdict['id'])
#         post_dict.update({"title": title, "body": body, "creation_date": creation_date})
#         return HTTPFound(location=request.route_url('home'))
#     query = request.dbsession.query(Entry)
#     post_dict = query.filter(Entry.id == request.matchdict['id']).first()
#     return {"post": post_dict}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_users_gist_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
