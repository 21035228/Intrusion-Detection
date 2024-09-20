import re
import time

import dload
from flask import *
from random import *

from flask import Flask, render_template
import datetime
from dbconnect import *
import dbconnect
import random
import string
import math
import io
import urllib.request
from mailsend import *
from viruscheck import *
from firenaseurl import *
import pyautogui
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

import random
import string

def generate_password():
    # Define sets of characters to use for each requirement
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits

    # Initialize the password with one character from each requirement
    password = [
        random.choice(lowercase),
        random.choice(uppercase),

        random.choice(numbers)
    ]

    # Fill the rest of the password with random characters
    remaining_length = 12 - len(password)
    all_characters = lowercase + uppercase + numbers

    for _ in range(remaining_length):
        password.append(random.choice(all_characters))

    # Shuffle the characters to randomize the password
    random.shuffle(password)

    # Convert the list to a string
    return ''.join(password)



def generate_unique_id(length):
    # Define the characters to include in the ID
    characters = string.ascii_letters + string.digits  # Letters and numbers
    unique_id = ''.join(random.choice(characters) for _ in range(length))
    return unique_id
def bytesconversion(bytes):
    convert_string=""
    if(bytes==0):
        convert_string="0 kb"
    else:
        kilobytes_value = math.ceil((bytes / 1024))
        if(kilobytes_value>=1024):
            migabytes_value = math.ceil(kilobytes_value / 1024)
            convert_string=str(migabytes_value)+" Mb"
        else:
            convert_string = str(kilobytes_value) + " Kb"
    return convert_string

@app.route('/')
def index():

    return render_template("index.html")

@app.route('/passwoedchange', methods=["GET", "POST"])
def passwoedchange():

    uid = session['id']
    pic = session['pic']
    sessionName = session['name']
    cpass = request.form["cpass"]
    npass = request.form["npass"]
    passw = request.form["pass"]
    sql = 'SELECT * FROM user WHERE id = "%s" ' % \
          (uid)
    user = recoredselect(sql)
    if(cpass==passw):
        inserquery('update user set password="%s" where id="%s"' % \
                   (npass, uid))
        sql = 'SELECT * FROM user WHERE id = "%s" ' % \
              (uid)
        user = recoredselect(sql)
        return render_template("profile.html", pro=pic,key=sessionName, userinfo=user)

    return render_template("profile.html", pro=pic,key=sessionName,userinfo=user,title="Change Psssword Status",show_sweetalert=True,mess='Incorrect Password',icon="error")

@app.route('/profile')
def profile():
    uid=session['id']
    sessionName=session['name']
    pic=session['pic']
    sql = 'SELECT * FROM user WHERE id = "%s"' % \
          (uid)
    print(sql)
    user = recoredselect(sql)
    return render_template("profile.html",pro=pic, key=sessionName,userinfo=user)



@app.route('/accountcreation', methods=["GET", "POST"])
def accountcreation():
    username = request.form["username"]
    email = request.form["email"]
    contact = request.form["mobile"]
    password = request.form["password"]
    show_sweetalert = True

    sql='SELECT * FROM user WHERE email = "%s" ' % \
     (email)
    print(sql)
    user=recoredselect(sql)
    print(user)
    if len(user)>0:
        return render_template('index.html',show_sweetalert=show_sweetalert, mess='User already exists with that email',icon="error")
    inserquery('INSERT INTO user (name, email,mno,password,profile,astatus) VALUES ("%s", "%s", "%s", "%s","%s","%s")'% \
     (username, email, contact,password,"static/assets/img/default.jpg","active"))
    return render_template("index.html",show_sweetalert=show_sweetalert,mess='Sucessfull Account created',icon="success")



@app.route('/changeprofile', methods=["GET", "POST"])
def changeprofile():
    uid = session['id']
    sessionName = session['name']
    pic = session['pic']
    username = request.form["username"]
    contact = request.form["mobile"]

    inserquery('update user set name="%s" ,mno="%s" where id="%d"'% \
     (username,  contact,uid))
    sql = 'SELECT * FROM user WHERE id = "%s" ' % \
          (uid)
    user = recoredselect(sql)
    return render_template("profile.html",pro=pic, key=sessionName, userinfo=user)

@app.route('/forget', methods=["GET", "POST"])
def forget():
    return render_template("forget.html")

@app.route('/forgetpass', methods=["GET", "POST"])
def forgetpass():
    email=request.form["email"]
    sql = 'SELECT * FROM user WHERE email = "%s" ' % \
          (email)
    user = recoredselect(sql)
    print(user)
    if(len(user)>0):

        password = generate_password()
        message=f'''
        New Password : {password}
        '''
        emailsend(email,message)
        inserquery('update user set password="%s" ,astatus="%s" where email="%s"' % \
                   (password,"active", email))

        return render_template("forget.html", show_sweetalert=True, mess='Password Send to Email Id', icon="success")
    return render_template("forget.html", show_sweetalert=True, mess='Incorrect Email Id', icon="error")





@app.route('/accesslog', methods=["GET", "POST"])
def accesslog():
    uid = session['id']
    pic = session['pic']
    sessionName = session['name']
    email = request.form["email"]
    fid = request.form["fid"]
    sql = 'SELECT * FROM user WHERE email = "%s" ' % \
          (email)
    print(sql)

    user = recoredselect(sql)
    filedata = fildetails()


    print(user)
    if len(user) == 0:
        return render_template("download.html", fileinfo=filedata, show_sweetalert=True, title="File Access User Status",
                               mess='Invalid Email Id',
                               icon="error",pro=pic, key=sessionName)
    inserquery('INSERT INTO fileaccesslog (fileurl, accessid) VALUES ("%s", "%s")' % \
               (fid, user[0][0]))
    return render_template("download.html", fileinfo=filedata, show_sweetalert=True, title="File Access User Status",
                           mess='Access Permission Granted',
                           icon="success",pro=pic, key=sessionName)

@app.route('/filesend', methods=["GET", "POST"])
def filesend():
    uid = session['id']
    pic = session['pic']
    sessionName = session['name']
    email = request.form["email"]
    fid = request.form["fid"]
    sql = 'SELECT * FROM user WHERE email = "%s" ' % \
          (email)
    print(sql)

    user = recoredselect(sql)
    filedata = fildetails()

    created_at = datetime.datetime.now()
    formatted_datetime = created_at.strftime("%Y-%m-%d %H:%M:%S")
    print(user)
    if len(user) == 0:
        return render_template("download.html", fileinfo=filedata, show_sweetalert=True, title="File Shareing status",
                               mess='Invalid Email Id, File Cannot be shared',
                               icon="error",pro=pic, key=sessionName)
    sql = 'SELECT * FROM filedetail WHERE id = "%s" ' % \
          (fid)
    print(sql)

    filedetails = recoredselect(sql)
    inserquery('INSERT INTO fileshare (senderid, fileid,receivermailid,filename,receiveddate) VALUES ("%s", "%s", "%s", "%s", "%s")' % \
               (uid, fid, user[0][0],filedetails[0][1],formatted_datetime))
    return render_template("download.html", fileinfo=filedata, show_sweetalert=True, title="File Shareing status",
                           mess='File Sucessfully Shared',
                           icon="success",pro=pic, key=sessionName)






@app.route('/emailsenddetail', methods=["GET", "POST"])
def emailsenddetail():
    uid = session['id']
    pic = session['pic']
    sessionName = session['name']
    email = request.form["email"]
    url = request.form["url"]
    message=f'''
    dowmload File : {url}
    '''
    emailsend(email,message)
    filedata = fildetails()
    return render_template("download.html", fileinfo=filedata, show_sweetalert=True, title="Link share Status",mess='Sucessfully link Shared',
                           icon="success",pro=pic, key=sessionName)


@app.route('/loginpage', methods=["GET", "POST"])
def loginpage():
    email = request.form["email"]
    password = request.form["password"]
    show_sweetalert=True
    sql='SELECT * FROM user WHERE email = "%s" AND password = "%s" AND astatus= "%s"'  % \
         (email, password,"active")
    print(sql)
    user=recoredselect(sql)
    if(dbconnect.login_check==3):
        dbconnect.login_check=0
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save("intrusion.png")
        emailsendwithattachement(email)
        inserquery('update user set astatus="%s" where email="%s"' % \
                   ("deactive", email))

        return render_template("login.html", show_sweetalert=show_sweetalert, mess='Intrusion Detected, Account Locked',
                               icon="error")

    if len(user)>0:
        session['id']=user[0][0]
        session['name'] = user[0][1]
        session['email'] = user[0][2]
        session['pic'] = user[0][5]
        sessionName=user[0][1]
        pic=user[0][5]
        dbconnect.login_check=0
        return render_template("index1.html", show_sweetalert=show_sweetalert,mess='Welcome '+user[0][1]+ ' !!',icon="success",pro=pic, key=sessionName)
    else:
        dbconnect.login_check+=1
        return render_template("login.html",show_sweetalert=show_sweetalert,mess='Authentication Failed',icon="error")
    dbconnect.login_check+=1
    return render_template("login.html",show_sweetalert=show_sweetalert,mess='Authentication Failed',icon="error")




@app.route('/profileupdate', methods=["GET", "POST"])
def profileupdate():
    uid = session['id']
    sessionName = session['name']

    file = request.files['fileinfo']
    path_yo_cloud = file.filename
    pathinfo="static/profile/"+str(uid)+sessionName+path_yo_cloud
    file.save(pathinfo)
    inserquery('update user set profile="%s" where id="%s"' % \
                   (pathinfo, uid))
    sql = 'SELECT * FROM user WHERE id = "%s" ' % \
          (uid)
    user = recoredselect(sql)
    session['pic']=pathinfo
    pic = session['pic']

    return render_template("profile.html",pro=pic,key=sessionName,userinfo=user,title="Profile Image Update",show_sweetalert=True,mess='update sucessfullly',icon="sucess")

@app.route('/fileupload', methods=["GET", "POST"])
def fileupload():
    file = request.files['fileinfo']
    path_yo_cloud = file.filename
    file.save(path_yo_cloud)
    userid=session['id']
    sessionName=session['name']
    pic=session['pic']
    show_sweetalert=True
    print(file)
    fileuid = generate_unique_id(10)
    sql = 'SELECT * FROM filedetail'
    print(sql)
    filedetail = recoredselect(sql)
    count=1
    if len(filedetail) > 0:
        count=int(filedetail[0][0])+1
    fileuid+=str(count)
    if file:
        response=verify_file(path_yo_cloud, path_yo_cloud)
        #time.sleep(10)
        if(response):
            return render_template("upload.html", pro=pic, key=sessionName, show_sweetalert=show_sweetalert,
                                   mess='Malicious File Not Allowed', icon="error")

        file_size = bytesconversion(os.path.getsize(path_yo_cloud))
        print(file_size)
        url = linkgenertaion(path_yo_cloud, path_yo_cloud)
        os.remove(path_yo_cloud)
        created_at=datetime.datetime.now()
        formatted_datetime = created_at.strftime("%Y-%m-%d %H:%M:%S")
        inserquery('INSERT INTO filedetail (filename, url,createdat,userid,uniqueId,filesize,filestatus) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
                   (path_yo_cloud,url,formatted_datetime, userid, fileuid, file_size,"Create"))

    return render_template("upload.html",pro=pic,key=sessionName,show_sweetalert=show_sweetalert,mess='Sucessfully file uploaded',icon="success")

@app.route('/registerpage')
def registerpage():
    return render_template("register.html")


@app.route('/downloadurl/<string:id>', methods=["GET", "POST"])
def downloadurl(id):

    sql = 'SELECT * FROM filedetail WHERE id = "%s" ' % \
          (id)
    print(sql)
    filedata = recoredselect(sql)
    print(filedata[0][2])
    print(filedata[0][1])
    #urllib.request.urlretrieve(filedata[0][2], filedata[0][1])
    info=filedownload(filedata[0][2],filedata[0][1])
    return send_file( io.BytesIO(info),
                    as_attachment=True,
                    download_name=filedata[0][1])

    #return redirect(url_for('download'))

@app.route('/downloadurlfile/<string:uid>', methods=["GET", "POST"])
def downloadurlfile(uid):
    if 'name' in session:
        sessionName = session['name']
        pic = session['pic']
        return render_template("downloadurlfile.html", uid=uid,pro=pic,key=sessionName)
    return render_template("downloadurlfile.html", uid=uid)

@app.route('/fileddownload', methods=["GET", "POST"])
def fileddownload():
    userid = session['id']
    sessionName = session['name']
    uid=request.form['fileinfo']
    sql = 'SELECT * FROM filedetail WHERE uniqueId = "%s" ' % \
          (uid)
    print(sql)
    filedata = recoredselect(sql)
    print(type(filedata[0][4]))
    print(type(userid))
    if(int(filedata[0][4]) == userid):

        print(filedata[0][2])
        print(filedata[0][1])
        #urllib.request.urlretrieve(filedata[0][2], filedata[0][1])
        info=filedownload(filedata[0][2],filedata[0][1])
        return send_file( io.BytesIO(info),
                        as_attachment=True,
                        download_name=filedata[0][1])
    else:
        sql = 'SELECT * FROM fileaccesslog WHERE fileurl = "%s" and accessid="%s" ' % \
              (uid,userid)
        print(sql)
        filedatainfo = recoredselect(sql)
        if(len(filedatainfo)>0):
            info = filedownload(filedata[0][2], filedata[0][1])
            return send_file(io.BytesIO(info),
                             as_attachment=True,
                             download_name=filedata[0][1])
    if 'name' in session:
        sessionName = session['name']
        pic = session['pic']
        return render_template("downloadurlfile.html", uid=uid,pro=pic,key=sessionName,title="File Download Status",show_sweetalert=True,mess='Access Permission Not Exist',icon="error")
    return render_template("downloadurlfile.html", uid=uid,title="File Download Status",show_sweetalert=True,mess='Access Permission Not Exist',icon="error")

@app.route('/delete/<string:id>', methods=["GET", "POST"])
def delete(id):
    sessionName = session['name']
    pic = session['pic']
    inserquery('update filedetail set filestatus="%s" where id="%s"' % \
               ("Delete", id))

    filedata = fildetails()
    return render_template("download.html",pro=pic,key=sessionName, title="File Delete Status", fileinfo=filedata,show_sweetalert=True,mess='Sucessfully file Deleted',icon="success")


@app.route('/restore/<string:id>', methods=["GET", "POST"])
def restore(id):
    sessionName = session['name']
    pic = session['pic']
    inserquery('update filedetail set filestatus="%s" where id="%s"' % \
               ("Create", id))

    filedata = filrestoredetails()
    return render_template("restore.html",pro=pic,key=sessionName, title="File Restore Status", fileinfo=filedata,show_sweetalert=True,mess='Sucessfully file Restored',icon="success")




@app.route('/upload')
def upload():
    sessionName = session['name']
    pic = session['pic']
    return render_template("upload.html",pro=pic,key=sessionName)

def fildetails():
    userid = session['id']
    sql = 'SELECT * FROM filedetail WHERE userid = "%s" and filestatus="Create"' % \
          (userid)
    print(sql)
    filedata = recoredselect(sql)
    return filedata

def fileshareddetails():
    userid = session['id']
    sql = 'SELECT * FROM fileshare WHERE receivermailid = "%s" ' % \
          (userid)
    print(sql)
    filedata = recoredselect(sql)
    return filedata

def filrestoredetails():
    userid = session['id']
    sql = 'SELECT * FROM filedetail WHERE userid = "%s" and filestatus="Delete"' % \
          (userid)
    print(sql)
    filedata = recoredselect(sql)
    return filedata


@app.route('/viewfile')
def viewfile():
    sessionName = session['name']
    pic = session['pic']
    filedata = fileshareddetails()
    return render_template("viewfile.html", pro=pic,key=sessionName,fileinfo=filedata)

@app.route('/download')
def download():
    sessionName = session['name']
    pic = session['pic']
    filedata = fildetails()
    return render_template("download.html", pro=pic,key=sessionName,fileinfo=filedata)

@app.route('/restorefile')
def restorefile():
    sessionName = session['name']
    pic = session['pic']
    filedata = filrestoredetails()

    return render_template("restore.html", pro=pic,key=sessionName,fileinfo=filedata)


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
