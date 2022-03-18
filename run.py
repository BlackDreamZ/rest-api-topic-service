# -*- encoding: utf-8 -*-

from api import app, db
import os

@app.shell_context_processor
def make_shell_context():
    return {"app": app,
            "db": db
            }


if __name__ == '__main__':
    print(os.environ)
    port = int(os.environ.get('PORT', 5000) )  # as per OP comments default is 17995
    # TODO сделать переключатель Debug
    app.run(debug=True,host="0.0.0.0",port=port)
