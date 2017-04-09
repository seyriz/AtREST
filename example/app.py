from at_rest import AtRest

app = AtRest(__name__)

@app.view()
def index():
    return ""


def a(**kwargs):
    """ A simple method
    @methods GET, POST
    @type json
    @url /
    @uri a int
    a is an int type specific variable
    @uri b
    b is a string type specific variable
    @uri c float
    c is a float type specific variable

    @form res
    "res" is a dictionary key. parsed as string value
    @form code int
    code is a  dictionary key. parsed as int value
    :return: str
    """

    pass
