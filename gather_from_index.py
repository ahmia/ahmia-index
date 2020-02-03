""" Filter websites based on keywords """
import requests

def search(url):
    """
    Search domains for filtering.
    """
    resp = requests.get(url)
    domain_list = []
    for hit in resp.json()["hits"]["hits"]:
        domain = hit["_source"]["domain"]
        if not domain in domain_list:
            domain_list.append(domain)
        #print(hit["_source"].get("title", "").encode("ascii","ignore"))
        print(domain)

def main():
    """
    Search based on key words and filter pages.
    """
    url = "http://localhost:9200/latest-tor/_search?pretty&size=9000&_source=title,domain"
    keywords_list = ['preteen', 'loli', 'lolita', 'jailbait', 'pthc', 'best cp',
                     '"child porn"', '"kid porn"', '"child sex"', '"cp video"']
    url = url + "&q=" + " OR ".join(keywords_list).replace(" ", "%20")
    url = url + "%20AND%20porn"
    search(url)

if __name__ == '__main__':
    main()
