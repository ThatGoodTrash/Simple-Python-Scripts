import requests

def request(url):
    try:
        return requests.get("http://" + url)
        
    except requests.exceptions.ConnectionError:
        pass

target_url = "192.168.1.173"

with open("/usr/share/wordlists/dirb/common.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = target_url + "/" + word
        #print(test_url)
        response = request(test_url)
        if response:
            print("[+] Discovered URL:  " + test_url) 