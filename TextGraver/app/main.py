#! /usr/bin/env python

from flask import Flask, render_template, send_from_directory, flash, request, redirect, url_for, g, Response
from app import app

@app.route("/")
def index():
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/reports")
def reports():
    return render_template('reports.html')

@app.route("/guidely")
def guidely():
    return render_template('guidely.html')

@app.route("/charts")
def charts():
    return render_template('charts.html')

@app.route("/shortcodes")
def shortcodes():
    return render_template('shortcodes.html')

@app.route("/icons")
def icons():
    return render_template('icons.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/pricing")
def pricing():
    return render_template('pricing.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/sunburst")
def sunburst():
    return render_template('sunburst.html')

@app.route("/graph")
def graph():
    return render_template('graph.html')

@app.route("/sunburstt")
def sunburstt():
    return render_template('sunburstt.html')

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/flowchart")
def flowchart():
    return render_template('flowchart.html')

@app.route("/api")
def api():
    return render_template('api.html')

@app.route("/phylo")
def phylo():
    return render_template('phylo.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'),404
