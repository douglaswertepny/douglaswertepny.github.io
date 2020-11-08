from flask import Flask, render_template, request, redirect, Markup


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/rolling')
def rolling():
  return render_template('rolling_mean.html')

@app.route('/growth')
def growth():
  return render_template('yearly_growth.html')
  
@app.route('/conclusions')
def conclusions():
  return render_template('conclusions.html')

@app.route('/about')
def about():
  return render_template('about.html')
 

if __name__ == '__main__':
  app.run(port=33507, debug=True)