import os
from flask import Flask
from pathlib import Path
from datetime import datetime  
from flask import render_template, request

# creates a Flask application, named app
app = Flask(__name__,template_folder='./templates', static_folder='./templates/static')
app.config.from_object(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    #print('enter getJSONReuslt', flush=True)
    
    return render_template('index.html')

# run the application
if __name__ == "__main__":  
    app.run(debug=True)