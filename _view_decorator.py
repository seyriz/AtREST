import functools

import flask as fl
from werkzeug.datastructures import FileStorage


class View:
    """
    It decorates the function as a Flask view function and passes the object to the target function.
    """
    def __init__(self):
        pass

    def __call__(self, f):
        """
        Make decorator and set variables
        TODO: parse url args
        :param f: Function to decorate
        :return: Decorated function
        """
        @functools.wraps(f)
        def deco(*args, **kwargs):
            if self.obj:
                args = list(args)
                if isinstance(self.obj, (list, set, tuple)):
                    for ov in self.obj:
                        args.append(self._makeObject(ov, **kwargs))
                else:
                    args.append(self._makeObject(self.obj, **kwargs))
                print("args", args)
                return f(*args)
            else:
                return f(*args, **kwargs)

        deco.__dict__['is_view'] = True
        if self.rule:
            rule = self.rule if self.rule.startswith("/") \
                else '/' + self.rule
            deco.__dict__['rule'] = rule
        else:
            if deco.__name__ == "index":
                deco.__dict__['rule'] = '/'
            else:
                deco.__dict__['rule'] = '/' + deco.__name__
        self.options['methods'] = self.methods
        deco.__dict__['options'] = self.options
        return deco

    def _get_form(self):
        """
        Get data from request
        :return: parsed form data as dict
        """
        form_value = dict()
        if fl.request.headers.get('Content-Type', "").count("application/x-www-form-urlencoded") or \
            fl.request.headers.get('Content-Type', "").count("multipart/form-data"):
            for k in fl.request.form.keys():
                value = fl.request.form.getlist(k)
                if isinstance(value, (list, set, tuple)):
                    if len(value) == 1:
                        form_value[k] = value[0]
                    else:
                        form_value[k] = value
                if isinstance(value, (str, int, bool, float)):
                    form_value[k] = value
            if not fl.request.headers.get('Content-Type', "").count("application/x-www-form-urlencoded"):
                for k in fl.request.files.keys():
                    value = fl.request.files.getlist(k)
                    if isinstance(value, (list, set, tuple)):
                        if len(value) == 1:
                            form_value[k] = value[0]
                        else:
                            form_value[k] = value
                    if isinstance(value, FileStorage):
                        form_value[k] = value
        elif fl.request.headers.get('Content-Type', "").count("application/json"):
            form_value = fl.request.get_json()
        return form_value

    def _makeObject(self, target_type=type, **kwargs):
        """
        make required object from request
        :param target_type: required object Type
        :return: parsed reuired object instance
        """
        param_obj = target_type()
        form = self._get_form()
        for k in form.keys():
            if(k in dir(param_obj)):
                setattr(param_obj, k, form.get(k, None))
        if kwargs:
            for k in kwargs.keys():
                if(k in dir(param_obj)):
                    setattr(param_obj, k, kwargs.get(k, None))
        return param_obj