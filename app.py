from flask import Flask, render_template
import pdfkit

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/GerarDanfe")
def GerarDanfe():
    pdfkit.from_file('templates/nfe.html', 'nfe.pdf')
    return render_template('nfe.html')