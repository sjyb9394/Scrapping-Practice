from flask import Flask, render_template, request, redirect, send_file
from so_scrapper import so_get_jobs
from indeed_scrapper import indeed_get_jobs
from monster_scrapper import monster_get_jobs
from export import save_to_file

app = Flask("Scrapping Web")
db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  web = request.args.get('web')
  if word and web!="none":
    word = word.lower()
    if web == "Stack Overflow":
      jobs = so_get_jobs(word)
    elif web == "Indeed":
      jobs = indeed_get_jobs(word)
    elif web == "Monster":
      jobs = monster_get_jobs(word)
    web = web.lower()
    key = word+" "+web
    db[key] = jobs
  else:
    return redirect("/")
  return render_template(
    "report.html", 
    searchingBy=word, 
    resultsNumber = len(jobs),
    jobs = jobs,
    website = web
  )

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    web = request.args.get('web')
    if not word:
      raise Exception()
    word = word.lower()
    web = web.lower()
    key = word+" "+web
    jobs = db.get(key)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("Jobs.csv",as_attachment=True)
  except:
    return redirect("/") 
 
app.run(host="0.0.0.0")