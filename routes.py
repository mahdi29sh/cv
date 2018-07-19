from flask import Flask ,render_template , request ,session,redirect
from db import *
import os
from datetime import timedelta
app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static','uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes = 5)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Session = sessionmaker(bind=engine)
# session = Session()
# user = User(99,'mahdi','1234','mahdi@gmail.com',1)
# session.add(user) 
# session.commit()
@app.route('/')
def index():
    Session = sessionmaker(bind=engine)
    s = Session()  
    result = s.query(cv).all()
    
    return render_template('home.html' , cv = result )


@app.route('/login',methods=['POST','GET'])
def login():
    if session.get('logged_in'):
        return redirect('/')
    if request.method=='POST':
        username = request.form['username']
        password = request.form['pass']
        print( username + ' - ' + password)
        if  username and password:
            Session = sessionmaker(bind=engine)
            s = Session()
            try:
                query = s.query(User).filter(User.username.in_([username]))
                result = query.first()
                print(result)
                if result.password == password :
                    session['logged_in']=True
                    session['username'] = username
                    session['access'] = result.admin
                    session.permanent = True
                    return  redirect('/')
                else:
                    error = 'wrong input'
                    return render_template('login.html',error = error)
            except:
                error = 'wrong input'
                return render_template('login.html',error = error)

    return render_template('login.html')
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return index()
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['pass']
        Session = sessionmaker(bind=engine)
        s = Session()
        try:
            query = s.query(User).filter(User.username.in_([username]))
            query1 = s.query(User).filter(User.email.in_([email]))
            result = query.first()
            result1 = query1.first()
            if result or result1:    
                return render_template('register.html',error = 'username or email exist')
            else:
                Session = sessionmaker(bind=engine)
                session1 = Session()
                id = None
                user = User(id,username , password , email , 3)
                session1.add(user)
                print(user)
                session1.commit()
                return render_template('home.html')
        except:
            error='error'
            return render_template('register.html',error = error)
    return render_template('register.html')
@app.route('/changepass',methods = ["GET","POST"])
def changepass():
    
    if request.method == 'POST' and session.get('logged_in'):
        
        password = request.form['pass']
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([session['username']]))
        user = query.first()
        user.password = password
        s.commit()
        return render_template('home.html')
    else:
        return render_template('changepass.html')
    return render_template('changepass.html')
@app.route('/addcv', methods=['GET','POST'])
def addcv():
    if not session.get('logged_in'):
            return render_template('login.html')
    if request.method == 'POST':
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([session['username']]))
        user = query.first()
        uid = user.uid
        
        file_img = request.files['img']
        file_doc = request.files['doc']
        edu = request.form['education']
        content = request.form['content']
        
        file_img.save(os.path.join(app.config['UPLOAD_FOLDER'],file_img.filename))
        file_doc.save(os.path.join(app.config['UPLOAD_FOLDER'],file_doc.filename))
        cvt = cv(None , uid ,file_img.filename, edu , content , file_doc.filename )
        s.add(cvt)
        s.commit()
        return redirect("/")
    return render_template('addcv.html')
@app.route('/detail/<id>')
def detail(id):
    Session = sessionmaker(bind=engine)
    s = Session()  
    result = s.query(cv).filter(cv.cvid.in_(id)).first()
    comment = s.query(Comments).filter(Comments.cvid.in_(id)).all()

    return render_template('detail.html' , cv = result , comment = comment )

@app.route('/addcomment<cvid>', methods= ['post'])
def addcomment( cvid):
    if not session.get('logged_in'):
        return render_template('login.html')
    comment = request.form['comment']
    Session = sessionmaker(bind=engine)
    s = Session()
    uid_query = s.query(User).filter(User.username.in_([session['username']])).first()
    uid = uid_query.uid
    result = s.query(cv).filter(cv.cvid.in_(cvid)).first()
    comment_s = Comments(None , uid, comment , cvid )
    s.add(comment_s)
    s.commit()
    Session = sessionmaker(bind=engine)
    s1 = Session()
    all = s1.query(Comments).filter(Comments.cvid.in_(cvid))
    s1.commit()
    return render_template('detail.html',cv = result ,comment = all)
    
@app.route('/edit<cvid>',methods = ["GET","POST"])
def edit(cvid):
    Session = sessionmaker(bind=engine)
    s = Session()
    cv_s = s.query(cv).filter(cv.cvid.in_(cvid)).first()

    return render_template('edit.html' , cv = cv_s)
@app.route('/edit_cv<cvid>',methods = ["POST"])
def edit_cv(cvid):
    
        file_doc = request.files['doc']
        edu = request.form['education']
        content = request.form['content'] 
        file_doc.save(os.path.join(app.config['UPLOAD_FOLDER'],file_doc.filename))
        Session = sessionmaker(bind=engine)
        s = Session()
        cv_s = s.query(cv).filter(cv.cvid.in_(cvid)).first()
        cv_s.document = file_doc.filename
        cv_s.education = edu
        cv_s.content = content
        s.commit() 

        return render_template('detail.html',cv = cv_s)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
