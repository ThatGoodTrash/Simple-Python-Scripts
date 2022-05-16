import scanner


target_url = "http://192.168.1.173/dvwa/"
links_to_ignore = ["http://192.168.1.173/dvwa/logout.php"]

data_dict = {"username":"admin" , "password":"password" , "Login":"submit"}

vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
vuln_scanner.session.post(target_url, data=data_dict)

#vuln_scanner.crawl()
forms = vuln_scanner.extract_forms("http://192.168.1.173/dvwa/vulnerabilities/xss_r/")
print(forms)
response = vuln_scanner.submit_form(forms[0], "testtest", "http://192.168.1.173/dvwa/vulnerabilities/xss_r/")
print(response.content)