from flask import Flask,render_template,request,url_for,redirect,flash,abort, session, jsonify
import json
import os.path,datetime
from werkzeug.utils import secure_filename

# at some point you got to create flask app

app = Flask(__name__) # __name__ is name of current module (hello)
app.secret_key = 'jsanc7ccsdhcd4rub738eu93e0beifb833huiebfsdjbjdjadb'
# app.secret_keyallows us to securely send messages back and forth from the user to make
# #sure that those trying to snooping on the connection cannot see this information.

@app.route('/')
def home():
    return render_template('home_page.html', name='Amey', age='21',codes= session.keys())
#  We have created a new flask project and inside of it created a flask app.
# In which we created one single route to say, if you go to the home page, return back the following text
@app.route('/about')
def about():
    return "about AMEY MAHAJAN "

# @app.route('/your-url') # this is code for simple GET request
# def your_url():
#     return render_template('your_url.html', code=request.args['code'])
@app.route('/your-url', methods = ['POST','GET'])
def your_url():
    if request.method == 'POST':
        # reason we have uses "form" instead of "args" is we are using POST request
        urls = {}
        if os.path.exists('urls.json'): # checks if urls.json file is already in place
            with open('urls.json') as url_file:
                urls = json.load(url_file)
        if request.form['code'] in urls.keys(): # used to check if shortname is unique or not
            flash("Short name <{}> has already been taken. Try another one".format(request.form['code']))
            return redirect(url_for('home'))
        if 'url' in request.form.keys(): # Checking if there is URL or FILE type
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file'] # getting the file from Form
            full_name = request.form['code'] + secure_filename(f.filename) # naming it
            f.save('static/user_files/'+full_name) # saving in server
            urls[request.form['code']] = {'file': full_name} # Adding to Json
        # This code is creating a dictionary like {Short_name : {'url': Url_entered}
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            session[request.form['code']] = datetime.datetime.now() # we have used time stamp just to know when user entered URL
        return render_template('your_url.html', code=request.form['code'])
    else:
        # return "Simple GET request is not valid {}".format(request.method)
        # return render_template('/') OR
        return redirect(url_for('home'))

# now lets work on real problem
# when someone enters our URL/shortname they will be redirected to the site they want
@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_files:
            urls = json.load(urls_files)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url']) # return URL
                else:
                    return redirect(url_for('static', filename='user_files/'+urls[code]['file'])) # return FILE
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
#0
# if __name__ == '__main__':
#     redirect_to_url('go')
#     print(os.path.exists('url.json'))