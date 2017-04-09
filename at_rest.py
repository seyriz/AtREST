import flask as fl

from _view_decorator import View


class AtRest:

    app = fl.Flask
    api_module_name = ""
    api_modules_dir = ""

    def __init__(self, import_name, api_module_name=None, api_modules_dir=None, **kwargs):
        self.app = fl.Flask(import_name=import_name, **kwargs)
        self.api_module_name = api_module_name
        self.api_modules_dir = api_modules_dir

    def get_app(self):
        """
        Get Flask app instance.
        :return: Flask app instance
        """
        return self.app

    def load_modules(self):
        pass

    def view(self):
        return View

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

    def _process_doc(self, func):
        """
        {"methods": str, "url": str, "return": type, "type": str(json or form or form-enc or xml), "form": dict, ""}
        :param func:
        :return:
        """
        params = dict()
        for l in func.__doc__.split("\n"):
            li = l.strip()
            if li.startswith("@"):
                ps = li.split(" ")
                param = dict(name=ps[0][1:], val=ps[1])
