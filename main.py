#!flask/bin/python
from flask import url_for
from src import app
from src.routes import simple_page


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def list_routes():
    import urllib

    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    return str(sorted(output))


if __name__ == "__main__":
    app.register_blueprint(simple_page, url_prefix='/checker')
    app.run(debug=True)
