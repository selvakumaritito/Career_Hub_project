from flask import Flask, render_template ,request,jsonify,flash,redirect,url_for,session
from database import register_to_db, load_jobs_from_db, load_job_from_db, add_application_to_db,login_from_db
import bcrypt


app=Flask(__name__)   

app.secret_key="123"


@app.route("/CareerHub",methods=['GET','POST'])     
def hello_everyone():
    jobs =load_jobs_from_db()
    return render_template('home.html', jobs=jobs)

@app.route('/job/<id>')
def show_job(id):
    job = load_job_from_db(id)

    if not job:
        return "Not Foud", 404
    
    return render_template('jobpage.html', job=job)


@app.route('/job/<id>/apply', methods=['POST'])
def apply_to_job(id):
        try:
            data = {key: value for key, value in request.form.items()}
            print(data)
            job=load_job_from_db(id)
            add_application_to_db(data,id)
            flash("Application Added Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return render_template('jobpage.html', job=job)



@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login',methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    print(name,password)
    user_data=login_from_db(name,password)
    if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[2].encode('utf-8')):
        session['loggedin'] = True
        session['name']=user_data[1]
        return redirect("CareerHub")
    else:
        flash("Username or Password Mismatch","danger")
        return redirect(url_for("index"))


@app.route('/register', methods=['GET'])
def show_registration_form():
   return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
        try:
            data = {key: value for key, value in request.form.items()}
            print(data)
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
            data['password'] = hashed_password.decode('utf-8')
            data['salt'] = salt.decode('utf-8')
            register_to_db(data)
            flash("Record Added Successfully","success")
            return redirect(url_for("index"))
        except Exception as e:
            flash("Error in Insert Operation: The contact number is too long. Please provide a valid phone number.", "danger")
            return redirect(url_for("index"))

   
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/api/job/<id>")
def show_job_json(id):
  job = load_job_from_db(id)
  return jsonify(job)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)