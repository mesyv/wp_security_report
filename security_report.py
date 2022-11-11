# Objective
# This script checks for WordPress vulnerabilities
# Author: Kamil Smolag
# Start Date: 2022 August 17
# Last Modified: 2022 August 31

# --- Imports
import socket
import ssl
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd



# --- Variables
headers = {
    "User-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}

# --- Functions
# try and
def try_except(func, *arg):
    try:
        result = func(*arg)
        print(func.__name__, ": ", result)
        return result
    except Exception as e:
        print(e)
        return "N/a"

#check if WordPress
def check_if_wordpress(r):
    if "wordpress" in r.text:
        return True
    else:
        return False

#check WordPress version
def check_wordpress_version(r):
    soup = BeautifulSoup(r.text, 'lxml')
    generators = soup.find_all("meta", {"name":"generator"}) # Looking for <meta name="generator" content="WordPress X.X.X">
    for g in generators: # There is many <meta name="generator"...> in page
        if "WordPress" in g["content"]: 
            if len(g["content"]) < 18: # Some of the "generators" are from plugins, could include WordPress in "content"
                return g["content"].strip("WordPress ") # Taking only number of WordPress
        else:
            return "N/a"

#check SSL
def ssl_check(hostname):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname,)
    conn.settimeout(3.0)
    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    Exp_ON = datetime.strptime(ssl_info['notAfter'], r"%b %d %H:%M:%S %Y %Z")
    # Days_Remaining = Exp_ON - datetime.utcnow()
    # Days_Remaining = int((Days_Remaining.total_seconds()/3600)/24) # Converting timedelta to seconds -> hours -> days
    Exp_ON = Exp_ON.strftime('%Y-%b-%d') # Changing date format
    # print("Expires ON:", Exp_ON, "\nRemaining:", Days_Remaining)
    return Exp_ON

#check DNS
def dns_check(hostname):
    return socket.gethostbyname(hostname)

#check robots.txt
def check_robots(hostname):
    hostname = hostname + "/robots.txt"
    r = requests.get(hostname)
    if r.status_code == 200:
        return True
    else:
        return False

#check /wp-json
def check_wpjson(hostname):
    hostname = hostname + "/wp-json/"
    r = requests.get(hostname, allow_redirects=False)
    if r.status_code == 200:
        return True
    else:
        return False

#check /wp-json/wp/v2/users 
def wpjson_users_check(hostname_url):
    wpjson_links = ["/wp-json/wp/v2/users", "/wp-json/wp/v2/UsErS", "/?rest_route=/wp/v2/users",  "/wp-json/wp/v2/users/1", 
    f"/wp-json/oembed/1.0/embed?url={hostname_url}/&format=json"]
    for link in wpjson_links:
        url = hostname_url + link
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return link
    return "N/A"

#print /wp-json/wp/v2/users 
def wpjson_users_print(url):
    r = requests.get(url, headers=headers)
    json_users = json.loads(r.text) #[1]["name"]
    users_data = {}
    for u in json_users:
        users_data[u["slug"]] = u["name"]
    return users_data

#check Security Headers
def scan_security_headers(url_headers):
    keys = ["X-XSS-Protection", "X-Content-Type-Options", "x-frame-options", "Strict-Transport-Security", "referrer-policy", "Content-Security-Policy"]
    security_headers_dict = {}
    for key in keys:
        try:
            #print(key, ": ", url_headers[key])
            if url_headers[key]:
                security_headers_dict[key] = url_headers[key]
        except KeyError:
            security_headers_dict[key] = "N/a"
            pass
    return security_headers_dict

#check XML-RPC
def check_xmlrpc(hostname):
    url = hostname + "/xmlrpc.php"
    r = requests.get(url)
    if "XML-RPC server accepts POST requests only." in r.text:
        return True
    else:
        return False

#check /wp-includes
def check_wp_includes(hostname):
    hostname = hostname + "/wp-includes"
    r = requests.get(hostname)
    if r.status_code == 200:
        return True
    else:
        return False

#check /wp-content/uploads/
def check_wp_content_uploads(hostname):
    hostname = hostname + "/wp-content/uploads/"
    r = requests.get(hostname, allow_redirects=False)
    if r.status_code == 200:
        return True
    else:
        return False

#check Theme/Plugins version
# in the future

websites = []
wordpress = []
wordpress_version = []
dns_address = []
ssl_cert = []
robots = []
wp_json = []
wp_json_users_link = []
wp_json_users_list = []
security_headers = []
xmlrpc = []
wp_includes = []
wp_content = []

test_list = ["perfectweb.today", "emazzanti.net", "messagingarchitects.com"]
clientsites_list = [
    "airbrasive.com", "alvapictures.com", "bkrllc.com", "castlehotelandspa.com", "chclearningcenter.org", "filtnews.com",
    "fiberjournal.com", "fortunefootwear.com", "rocklandrealty.com", "sankaraspa.com", "visitnyack.org", "bcc.us.com", "fmbsteel.com",
    "mattoon-lee.com", "foodbanknyc.org", "ericarobert.com",
]
oursites_list = [
    "emazzanti.net", "liqui-site.com", "messagingarchitects.com", "emazzanti.ninja", "businesscontinuityvault.com", 
    "cloudtechnology365.com", "emazzantifashion.com", "emazzantijewelrygroup.com", "guarddepot.com", "retailpaytech.com", 
    "virtualfirewall.com", "egovernance.com", 
]

if __name__ == "__main__":
    for hostname in clientsites_list:
        websites.append(hostname)
        if not "http" in hostname:
            url = "https://" + hostname
        print("-----------------------------------------------------------")
        print(hostname)
        r = requests.get(url)
        wordpress.append(try_except(check_if_wordpress, r))
        wordpress_version.append(try_except(check_wordpress_version, r))
        dns_address.append(try_except(dns_check, hostname))
        ssl_cert.append(try_except(ssl_check, hostname))
        robots.append(try_except(check_robots, url))
        wp_json.append(try_except(check_wpjson, url))
        wp_json_users_link_var = try_except(wpjson_users_check, url) #saving wp_json user link to variable to use in IF
        wp_json_users_link.append(wp_json_users_link_var)
        if wp_json_users_link_var != "N/a": #If user enumeration is disabled no need to scrap the users
            wp_json_users_list.append(try_except(wpjson_users_print, url + wp_json_users_link_var))
        else:
            wp_json_users_list.append("N/a")
        security_headers.append(try_except(scan_security_headers, r.headers))
        xmlrpc.append(try_except(check_xmlrpc, url))
        wp_includes.append(try_except(check_wp_includes, url))
        wp_content.append(try_except(check_wp_content_uploads, url))
       


final_data = {
    #"Scrap date" : datetime.now().strftime("%Y-%b-%d %H-%M"),
    "Website" : websites,
    "WordPress" : wordpress,
    "WP version" : wordpress_version,
    "DNS" : dns_address,
    "SSL" : ssl_cert,
    "wp_json" : wp_json,
    "wp_json_users_link" : wp_json_users_link,
    "wp_json_users_list" : wp_json_users_list,
    "Security Headers" : security_headers,
    "Robots.txt" : robots,
    "XML-RPC" : xmlrpc,
    "wp_includes" : wp_includes,
    "wp_content" : wp_content,

    #...
}

dt = pd.DataFrame(final_data, index=False)
dt.to_excel(r"C:\Projekty\Coding\wp_security_report\security_report.xlsx")
print(dt)