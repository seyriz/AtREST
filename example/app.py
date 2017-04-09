from at_rest import AtRest

app = AtRest(__name__)


@app.view
def index():
    """Index page

    @response 200 normal state
    """

@app.view
def history_list(user_id, date, page):
    """A simple example View func.
    Find user's post from database
    @methods {get}
    @url /history

    @param user_id {str} User unique id.
    @param date {str} datetime.
    @param page {int} page number.

    @response 200 This is success and return json string.
    @response 404 This is not found history and return json string with error description.
    """
    return {}


@app.view
def login(user_id, passwd):
    """A simple example View func for login
    @methods {post}

    @form user_id user id for login
    @form passwd passwd for login

    @response 200 This is success and return json string about user info.
    @response 403 This is failed to login.
    """
    return {}

@app.view
def new_post():
    """A simple example View func for register new post
    @methods {put}

    @header csrf csrf token for check is valid request.

    @param board_id {int}
    """


print(app.get_flask().url_map)