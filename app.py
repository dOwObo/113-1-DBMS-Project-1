from flask import Flask
from api.api import *
from api.sql import *
from backstage.views.manager import *

app = Flask(__name__)
app.secret_key = 'Your Key' 

app.register_blueprint(api, url_prefix='/')
app.register_blueprint(manager, url_prefix='/backstage')

login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('login.html')

if __name__ == '__main__':
    app.debug = True
    app.secret_key = "Your Key"
    app.run()