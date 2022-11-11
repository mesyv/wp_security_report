import requests

class ScanHeaders:
    def __init__(self, url):
        self.url = url
        r = requests.get(self.url)
        self.headers = r.headers
        self.cookies = r.cookies

    def scan_secure(self, cookie):
        """Set-Cookie header should have the secure attribute set"""
        if cookie.secure:
            print("[+]", "Secure", ':', "pass")
        else:
            print("[-]", "Secure attribute not set", ':', "fail!")

    def scan_httponly(self, cookie):
        """Set-Cookie header should have the HttpOnly attribute set"""
        if cookie.has_nonstandard_attr('httponly') or cookie.has_nonstandard_attr('HttpOnly'):
            print("[+]", "HttpOnly", ':', "pass")
        else:
            print("[-]", "HttpOnly attribute not set", ':', "fail!")

        #Add more headers which are also in securityheaders.com
if __name__ == "__main__":
	target = ScanHeaders("https://www.emazzanti.net/")

	for key in target.headers:
		print(key, ":", target.headers[key])

for cookie in target.cookies:
    print("Set-Cookie:")
    target.scan_secure(cookie)
    target.scan_httponly(cookie)