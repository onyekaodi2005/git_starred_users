import requests, json
from multiprocessing import Pool, cpu_count
from copy import deepcopy
from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gitStarredRepo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class GitModel(db.Model):
    repository_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.String(255), nullable=True)
    last_push_date = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    stars = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        data = {'REPOSITORY ID': self.repository_id, 'NAME': self.name, 'URL': self.url, 'CREATED DATE': self.created_date, 'PUSH DATE': self.last_push_date, 'DESCRIPTION':self.description, 'STARS ⭐️⭐️⭐️': self.stars}
        return f"{json.dumps(data)}"

db.create_all()

def getApiData(url, kwargs):
    result = requests.get(url=url, params=kwargs)
    if result.status_code == 200:
        for i in result.json()['items']:
            result = GitModel.query.filter_by(repository_id=i.get('id')).first()
            if result:
                continue
            else:
                data = GitModel(repository_id=i.get('id'), name=i.get('name'), url=i.get('url'), created_date=i.get('created_at'), last_push_date=i.get('pushed_at'), description=i.get('description'), stars=i.get('stargazers_count'))
                db.session.add(data)
                db.session.commit()

@app.route("/")
def home():
    m = GitModel.query.order_by(GitModel.stars.desc()).all()
    x = json.loads(str(m))
    return render_template("index.html", data=x)

@app.route('/')
@app.route('/<path:unknown>')
def fallback(unknown=None):
    return redirect(url_for("home"))

if '__main__' == __name__:
    params = {'page': 0, 'per_page': 100, 'order': 'desc','sort': 'stars'}
    URL = 'https://api.github.com/search/repositories?q=language:python'
    pool = Pool(processes=(cpu_count() - 1))
    
    x = []
    for i in range(10):
        newdata = deepcopy(params)
        newdata.update({'page':i+1})
        x.append(newdata)

    for i in x:
        pool.apply_async(getApiData, args=(URL, i))
    pool.close()
    pool.join()
    app.run(debug=True)

        
