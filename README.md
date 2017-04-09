# @REST

A simple REST API generation library based on flask.

## Description


@REST is easily defines a RESTful API endpoint using Docstring, passes parsed parameter to view function, and automatically jsonoify return value.

and creates a RESTful api endpoint using a key starting with @ as defined in the Docstring.

also supports object passing to view function parameters. This allows you to directly create a Class object from a request in the flask and pass it to the parameter.

### API doc Keys
| key | description | param style | is list | is duplicable | default |
| --- | --- | --- | --- | --- | --- |
| methods | Define allowed HTTP methods. Multiple method is allowed(comma separated) | PUT, POST | True | False | GET |
| object | The object to be passed to the function's parameters. If not, all parameters are passed to kwargs. | {type:name} | True | False | |
| url | a endpoint url | endpoint | False | False | "/" if func name is index else func name |
| uri | use uri value as parameter. ORDERD. | {name:type} | False | True | |
| form | form key value as parameter. | {name:type} | False | True | |
| response | response description of view func | HTTP_status description | False | True | 200 "" |

> Note
> 1. can apply for json(application/json), xml(application/xml), form(multipart/form-data), enc_form(application/x-www-form-urlencoded)

```python
import at_rest

app = at_rest.AtRest(__name__)

@app.view()
def history_list(user_id, date, page):
    """A simple example View func.(I know this is not RESTful. This is just example.)
    Find user's post from database
    @methods get
    @url /history
    
    @uri {user_id:str} User unique id.
    @uri {date:str} datetime.
    @uri {page:int} page number.
    
    @response 200 This is success and return json string.
    @response 404 This is not found history and return json string with error description.
    """
    return {}

```