import importlib
import functools
import re
import inspect
import flask as fl

from _view_decorator import View

class AtRest:

    _types = {
        "str": str,
        "string": str,
        "int": int,
        "integer": int,
        "float": float,
        "boolean": bool,
        "bool": bool,
        "list": list,
        "tuple": tuple,
        "set": set,
        "dict": dict,
    }

    app = fl.Flask

    def __init__(self, import_name, **kwargs):
        self.app = fl.Flask(import_name=import_name, **kwargs)

    def get_flask(self):
        """
        Get Flask app instance.
        :return: Flask app instance
        """
        return self.app

    def add_custom_types(self, type_=type):
        self._types[type_.__name__] = type_

    def view(self, f, *args, **kwargs):
        print("view deco called")
        @functools.wraps(f)
        def decorator():
            return f
        decorator.__dict__['is_view'] = True
        decorator.__dict__['params'] = self._process_doc(f)
        decorator.__dict__['params']['view_func'] = decorator
        self._add_view_func(decorator)
        return decorator

    def run(self, host=None, port=None, debug=None, **options):
        """Runs the application on a local development server.

        Do not use ``run()`` in a production setting. It is not intended to
        meet security and performance requirements for a production server.
        Instead, see :ref:`deployment` for WSGI server recommendations.

        If the :attr:`debug` flag is set the server will automatically reload
        for code changes and show a debugger in case an exception happened.

        If you want to run the application in debug mode, but disable the
        code execution on the interactive debugger, you can pass
        ``use_evalex=False`` as parameter.  This will keep the debugger's
        traceback screen active, but disable code execution.

        It is not recommended to use this function for development with
        automatic reloading as this is badly supported.  Instead you should
        be using the :command:`flask` command line script's ``run`` support.

        .. admonition:: Keep in Mind

           Flask will suppress any server error with a generic error page
           unless it is in debug mode.  As such to enable just the
           interactive debugger without the code reloading, you have to
           invoke :meth:`run` with ``debug=True`` and ``use_reloader=False``.
           Setting ``use_debugger`` to ``True`` without being in debug mode
           won't catch any exceptions because there won't be any to
           catch.

        .. versionchanged:: 0.10
           The default port is now picked from the ``SERVER_NAME`` variable.

        :param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
                     have the server available externally as well. Defaults to
                     ``'127.0.0.1'``.
        :param port: the port of the webserver. Defaults to ``5000`` or the
                     port defined in the ``SERVER_NAME`` config variable if
                     present.
        :param debug: if given, enable or disable debug mode.
                      See :attr:`debug`.
        :param options: the options to be forwarded to the underlying
                        Werkzeug server.  See
                        :func:`werkzeug.serving.run_simple` for more
                        information.
        """
        self.app.run(host, port, debug, **options)

    def _add_view_func(self, view):
        if view.__dict__.get("is_view", False):
            options = view.__dict__['params']
            print(options)
            rules = options['rules']
            for rule in options['rules']:
                self.app.add_url_rule(rule=rule, view_func=view, methods=options['methods'])
            # rule, endpoint = None, view_func = None, ** options
            # self.app.add_url_rule(**params)

    def _process_doc(self, func):
        """
        {"methods": str, "url": str, "return": type, "type": str(json or form or form-enc or xml), "form": dict, ""}
        :param func:
        :return:
        """
        params = dict()
        for l in inspect.getdoc(func).split("\n"):
            if l.startswith("@methods"):
                params['methods'] = self._parse_methods(params.get("methods", None), l)
            elif l.startswith("@url"):
                params['rules'] = self._parse_rules(params.get("rules", None), l)
            elif l.startswith("@object"):
                params['objects'] = self._parse_type_val(params.get("objects", None), l)
            elif l.startswith("@header"):
                params['headers'] = self._parse_type_val(params.get("headers", None), l)
            elif l.startswith("@param"):
                params['params'] = self._parse_type_val(params.get("params", None), l)
            elif l.startswith("@form"):
                params['forms'] = self._parse_type_val(params.get("forms", None), l)
        if params.get("methods", None) is None:
            params['methods'] = ['GET']
        if params.get("rules", None) is None:
            if func.__name__ == "index":
                params['rules'] = ["/"]
            else:
                params['rules'] = ["/" + func.__name__]
        self.add_rules_with_param(params.get("rules", None), params.get("params"))
        return params

    def _parse_type_val(self, list_, param):
        if list_ is None:
            list_ = list()
        p_lines = param.split(" ")
        name = p_lines[1]
        type_match = re.compile("\{\w+\}")
        type_r = type_match.findall(param)
        if len(type_r):
            type_str = type_r[0].replace("{", "").replace("}", "")
            if type_str == "str":
                type_str = ""
        else:
            type_str = ""
        type_ = self._types.get(type_str.lower(), None)
        list_.append([name, type_])
        return list_

    def _parse_rules(self, list_, param):
        if list_ is None:
            list_ = list()
        p_lines = param.split(" ")
        name = p_lines[1]
        list_.append(name)
        return list_

    def _parse_methods(self, list_, param):
        if list_ is None:
            list_ = list()
        method_match = re.compile("\{.+\}")
        p_lines = method_match.findall(param)[0].replace("{", "").replace("}", "").split(",")
        for m in p_lines:
            list_.append(m.strip().upper())
        return list_

    def add_rules_with_param(self, list_, params):
        if params:
            rule_string = list_[0]
            for p in params:
                if p[1]:
                    rule_string += ("/<{}{}>".format(p[1].__name__ + ":", p[0]))
                else:
                    rule_string += ("/<{}>".format(p[0]))
            list_.append(rule_string)
