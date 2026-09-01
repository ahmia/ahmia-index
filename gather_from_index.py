# -*- coding: utf-8 -*-
""" Filter websites based on keywords """
from elasticsearch import Elasticsearch
import settings  # Import the settings from settings.py
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ALLOWED_DOMAINS = [
    "zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion",
    "donionsixbjtiohce24abfgsffo2l4tk26qx464zylumgejukfq2vead.onion",
    "deeeepv4bfndyatwkdzeciebqcwwlvgqa6mofdtsvwpon4elfut7lfqd.onion",
    "juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion",
    "torbuy4iw7eghmdkpllz2tjvphtsey6a47mn2mjsmcii4vlv3wr2csqd.onion",
    "torbuyxpe6auueywlctu4wz6ur3o5n2meybt6tyi4rmeudtjsysayqyd.onion"
]

def search(es, domain_list, keywords_list):
    """
    Search domains for filtering.
    """
    query = {
        "size": 30000,
        "_source": ["title", "domain"],
        "query": {
            "bool": {
                "should": [
                    {"match_phrase": {"content": keyword}} for keyword in keywords_list
                ]
            }
        }
    }
    resp = es.options(request_timeout=90).search(index=settings.ES_TOR_INDEX, body=query)
    hits = resp['hits']['hits']
    for hit in hits:
        domain = hit.get("_source", {}).get("domain", "")
        if domain and domain not in domain_list and domain not in ALLOWED_DOMAINS:
            print(domain)
            domain_list.append(domain)

def main():
    """
    Search based on keywords and filter pages.
    """
    # Use the imported settings
    es = Elasticsearch(
        [settings.ES_HOST],
        verify_certs=False,
        ca_certs=settings.ES_CA_CERTS,
        basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD)
    )

    domain_list = []
    keywords_list = ['3d boy', '3d boys', 'am pedophilia',
                     'amateur cp', 'amateurs cp', 'anal child',
                     'baby love', 'baby porn', 'baby slut',
                     'baby sluts', 'baby whore', 'baby whores',
                     'babyboy', 'babyboys', 'babyshivid',
                     'babyshivids', 'best cp', 'best onion porn',
                     'big rape', 'bitch cp', 'boy a priori',
                     'boy cp', 'boy forbidden', 'boy hurt',
                     'boy vid', 'boy video', 'boy videos',
                     'boy vids', 'boylove', 'candy sex',
                     'candydoll', 'candydolls', 'child a priori',
                     'child anal', 'child blowjob', 'child cp',
                     'child cum', 'child foot', 'child forbidden',
                     'child fuck', 'child naughty', 'child nude',
                     'child porn', 'child porno', 'child rape',
                     'child sex', 'child slut', 'child sluts',
                     'child xxx', 'childfugga', 'childlove',
                     'childlover', 'childporn', 'children nude',
                     'childrens porn', 'childrenxxx', 'childsex',
                     'childxxx', 'city porn', 'content pedo',
                     'cp amateur', 'cp amateurs', 'cp boy',
                     'cp boys', 'cp bukkake', 'cp child',
                     'cp database', 'cp fuck',
                     'cp large', 'cp love', 'cp pack',
                     'cp pedo', 'cp porn', 'cp premium',
                     'cp rape', 'cp sex', 'cp vid',
                     'cp video', 'cp videos', 'cp vids',
                     'cp violence', 'cporn', 'cpvid',
                     'cpvideo', 'cpvideos', 'cpvids',
                     'database cp', 'daughters destroyed', 'delivers xnxx',
                     'destroyed daughter', 'emodoll', 'emodolls',
                     'family incest', 'foot child', 'foot kid',
                     'forbidden boy', 'forbidden boys', 'forbidden fruit',
                     'forbidden girl', 'forbidden girls', 'forbidden porn',
                     'forbidden sex', 'forbidden young', 'fruit forbidden',
                     'fuck child', 'fuck cp', 'girl a priori',
                     'girl forbidden', 'girls youngest', 'hard porn forum',
                     'hard porn room', 'hardcore child', 'hebephilia',
                     'hurt boy', 'hurt boys', 'illegal sex',
                     'incest family', 'jailbait', 'jailbaits',
                     'kid porn', 'kids foot', 'kids naughty',
                     'kids porno', 'kids video', 'kids videos',
                     'kidsxxx', 'kidzporn', 'kinderficker',
                     'kinderporn', 'kitty porn', 'large cp',
                     'little love', 'lola pedo', 'loland',
                     'loli lust', 'lolicore', 'lolilust',
                     'loliporn', 'lolita', 'lolitacity',
                     'lolitaguy', 'lolitas', 'lollisex',
                     'lordofthering', 'love cp', 'love little',
                     'mylola', 'myteens', 'naked young',
                     'naughty child', 'naughty kid', 'nefarious taboo',
                     'nude child', 'nude children', 'pack cp',
                     'pedo child', 'pedo content', 'pedo cp',
                     'pedo lola', 'pedo pedo', 'pedo photo',
                     'pedo porno', 'pedo vid', 'pedo video',
                     'pedo videos', 'pedo vids', 'pedo webcam',
                     'pedo webcams', 'pedobum', 'pedodad',
                     'pedofamily', 'pedoleak', 'pedolola',
                     'pedolover', 'pedomania', 'pedomom',
                     'pedomum', 'pedophilic', 'photo pedo',
                     'pink child', 'playground molly', 'porn city',
                     'porn cp', 'porn hacker', 'porn kid',
                     'porn kitty', 'porn porn porn porn', 'porn toddler',
                     'porn underage', 'porn, true, true, porn', 'porno kid',
                     'porno pedo', 'porno station', 'premium cp',
                     'preteen', 'preteens', 'pron true',
                     'pthc', 'ptsc', 'pureyoung',
                     'rape and murder', 'rape big', 'rape child',
                     'rape cp', 'rape videos', 'raped bitch',
                     'real rape', 'rindexxx', 'sex candy',
                     'sex child', 'sex cp', 'sex forbidden',
                     'sex underage', 'show the immoral content', 'slut baby',
                     'slut child', 'spanking underage', 'teen deepthroat',
                     'teen garden', 'teen porn box', 'toddler porn',
                     'torpedo', 'true pron', 'true teen amateurs',
                     'trusted porn', 'underage cam', 'underage porn',
                     'underage sex', 'underage slut', 'underage sluts',
                     'underage spanking', 'underage whore', 'underage whores',
                     'underage xxx', 'video cp', 'video mix',
                     'videos boy', 'videos boys', 'videos cp',
                     'videos kid', 'vids boy', 'vids boys',
                     'vids cp', 'violence cp', 'webcams pedo',
                     'whore baby', 'whore underage', 'xnxx deliver',
                     'xnxx delivers', 'xonions', 'xplay',
                     'xxx child', 'xxx underage', 'young forbidden',
                     'forbidden fust', 'cp for sale', 'oXXX', 'xxx tube',
                     'red room', 'zona chat', 'zona access',
                     'Onion, Onion, Onion,', 'secret desitres',
                     'kinderporno', 'misbruik', 'kindermisbruik', 'under legal age',
                     'ChildHub', 'sweet story', 'Yati Yati',
                     'Onion Porn You Can Trust', 'Free Browsing For All']

    search(es, domain_list, keywords_list)

if __name__ == '__main__':
    main()
