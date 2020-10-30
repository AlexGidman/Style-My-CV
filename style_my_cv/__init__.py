"""
Style My CV

An application that increases your chances of getting hired by creating a 
professionally formatted CV, targeted at the role you're applying for.
"""

import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure Flask application"""

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'cv.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        # raise OSError("Problem creating or reading instance folder")

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import views
    app.register_blueprint(views.bp)
    app.add_url_rule('/', endpoint='index')

    return app