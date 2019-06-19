try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import re
from bs4 import BeautifulSoup
# import socks
# import socket

# def create_connection(address, timeout=None, source_address=None):
#     sock = socks.socksocket()
#     sock.connect(address)
#     return sock

# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

# # patch the socket module
# socket.socket = socks.socksocket
# socket.create_connection = create_connection


def get_abuse_onions_hiddenwiki():
    html = urlopen("http://mijpsrtgf54l7um6.onion/index.php/Hard_Candy")
    soup = BeautifulSoup(html, "html.parser")
    snippet = soup.find_all('h1')
    urls = []
    for h1 in snippet:
        if h1.string == "Resources: Nude or Hardcore":
            ss = h1.find_next('h3')
            while ss.string != "Image and video boards":
                ss = ss.find_next('h3')
            ss = ss.next
            while ss.name != "h3":
                if ss.name == "a" and ss.get('href')[0] != '/':
                    url1 = ss.get('href')[7:29]
                    url2 = ss.get('href')[7:69]
                    # Add onion domains
                    if len(url1) == 22 and url1[-6:] == ".onion":
                        urls.append(url1)
                    if len(url2) == 62 and url2[-6:] == ".onion":
                        urls.append(url2)
                ss = ss.next
    urls = list(set(urls))  # Remove duplicates from the list
    for domain in urls:
        if not "mijpsrtgf54l7um6" in domain:
            print(domain)

def get_abuse_onions_by_url(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        address = link.get('href')
        url1 = address[7:29]
        url2 = address[7:69]
        # Add onion domains
        if len(url1) == 22 and url1[-6:] == ".onion":
            urls.append(url1)
        if len(url2) == 62 and url2[-6:] == ".onion":
            urls.append(url2)
    urls = list(set(urls))  # Remove duplicates from the list
    for domain in urls:
        if not url[7:23] in domain:
            print(domain)

if __name__ == '__main__':
    get_abuse_onions_hiddenwiki()
    url = "http://mijpsrtgf54l7um6.onion/index.php/Underage_erotica"
    get_abuse_onions_by_url(url)
    url = "http://toplistftmajmxhb.onion"
    get_abuse_onions_by_url(url)
