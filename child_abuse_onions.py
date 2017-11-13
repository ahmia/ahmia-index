import urllib2
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

def get_abuse_onions():
    html = urllib2.urlopen("http://uhwikih256ynt57t.onion/wiki/index.php/Hard_Candy")
    soup = BeautifulSoup(html, "html.parser")
    snippet = soup.find_all('h1')
    urls=[]
    for h1 in snippet:
        if h1.string=="Resources: Nude or Hardcore":
            ss=h1.find_next('h3')
            while ss.string!="Image and video boards":
                ss=ss.find_next('h3')
            ss=ss.next
            while ss.name!="h3":
                if ss.name=="a" and ss.get('href')[0]!='/':
                    url=ss.get('href')[7:29]
                    # Add onion domains
                    if len(url) == 22 and url[-6:] == ".onion":
                        urls.append(url)
                ss=ss.next
    urls = list(set(urls)) # Remove duplicates from the list
    for domain in urls:
        print(domain)
if __name__ == '__main__':
   get_abuse_onions()
