from flask import render_template, redirect, request, Flask, jsonify
from app import app, models

@app.route('/')
def index():
    return "success"