from flask import Flask, render_template
from example_blueprint import summarize

app = Flask(__name__)
app.register_blueprint(summarize)

@app.route('/')
def index():
    return render_template('home.html',summary_text="")