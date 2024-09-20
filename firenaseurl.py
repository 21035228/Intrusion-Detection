import pyrebase
import os
import requests
config ={
    "apiKey": "AIzaSyDwiCiOvx0mgkdUVe6HW2x4_Oq0X3kgBs8",
    "authDomain": "fileshareingapplication.firebaseapp.com",
    "databaseURL": "https://fileshareingapplication-default-rtdb.firebaseio.com",
    "projectId": "fileshareingapplication",
    "storageBucket": "fileshareingapplication.appspot.com",
    "messagingSenderId": "543959977112",
    "appId": "1:543959977112:web:5871406c916e1d961754ed",
    "measurementId": "G-J7JMNB5GHQ"
}

firebase=pyrebase.initialize_app(config)
storage=firebase.storage()
def linkgenertaion(path_yo_cloud,path_loacal):

    storage.child(path_yo_cloud).put(path_loacal)
    url = storage.child(path_yo_cloud).get_url(token=None)
    print(url)

    return url
def filedownload(download_url,name):

    local_file_path =name
    try:
        response = requests.get(download_url)
        if response.status_code == 200:
            return response.content
            print(f"File downloaded to {local_file_path}")
        else:
            print(f"Error: HTTP status code {response.status_code}")
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
    return ""

#filedownload('https://firebasestorage.googleapis.com/v0/b/fileshareingapplication.appspot.com/o/Project.pdf?alt=media')

