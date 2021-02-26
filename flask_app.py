from flask import Flask
from flask import render_template, url_for
from main import *

app = Flask(__name__)


@app.route('/<id>')
def thepist(id):

    therapist = postgres.get_therapist_by_id(id)
    return render_template('therapist.html',
                           photo=therapist['photo'],
                           name=therapist['name'],
                           methods=therapist['methods'].split(', '))
@app.route('/')
def choice():


    data = []

    for i in airtables_data:
        data.append([
            i[0],
            i[1],
            url_for("thepist", id=i[0])
        ])
    return render_template('therapists_selection.html',
                           data=data)

if __name__=="__main__":
    app.run()