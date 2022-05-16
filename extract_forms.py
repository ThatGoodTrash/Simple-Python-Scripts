import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def request(url):
    try:
        return requests.get("http://" + url)
        
    except requests.exceptions.ConnectionError:
        pass

target_url = "192.168.1.173/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)

parsed_html = BeautifulSoup(response.content, "xml")
forms_list = parsed_html.find_all("form")

for form in forms_list:
    action = form.get("action")
    post_url = "http://" + urljoin(target_url, action)
    print(post_url)
    method = form.get("method")
    print(method)

    inputs_list = form.find_all("input")
    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = "test"

        post_data[input_name] = input_value

    result = requests.post(post_url, data=post_data)
    print(result.content.decode())