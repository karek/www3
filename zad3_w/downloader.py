import urllib
from bs4 import BeautifulSoup


def load_site(site):
    f = urllib.urlopen(site)
    return f.read()


def save_site(file_name, site_text):
    f = open(file_name, 'w')
    f.write(site_text)


def get_deeper_links(site_addr):
    site = load_site(site_addr)
    soup = BeautifulSoup(site)
    return soup.find(id="s0").find_all(class_="col5")


def compute():
    base_site = "http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/"
    wojewodztwa = get_deeper_links(base_site + "index.htm")
    okregi_miast = []
    okregi_gmin = []
    cnt = 0

    for i in wojewodztwa:
        powiaty = get_deeper_links(base_site + i.a['href'])
        print cnt
        for powiat in powiaty:
            print cnt
            if ", m." in powiat.text or "Zagranica" in powiat.text or "Statki" in powiat.text:
                okr_miasta = get_deeper_links(base_site + powiat.a['href'])
                curr_okregi = []
                for okrag in okr_miasta:
                    curr_okregi.append(okrag.text)
                    cnt += 1
                okregi_miast += (powiat.text, curr_okregi)
            else:
                gminy = get_deeper_links(base_site + powiat.a['href'])
                # print gminy
                for j in gminy:
                    okregi_gminy = get_deeper_links(base_site + j.a['href'])
                    curr_okregi = []
                    print j.text
                    for okrag in okregi_gminy:
                        curr_okregi.append(okrag.text)
                        cnt += 1
                        print okrag.text
                    okregi_gmin += (j.text, curr_okregi)
                    # print curr_okregi

    print okregi_gmin

    print "Finished1 " + str(cnt)
    save_site("aa", str(okregi_miast) + "\n" + str(okregi_gmin))
    print "Finished2 " + str(cnt)


compute()