from django.core.management.base import BaseCommand, CommandError
import urllib
from bs4 import BeautifulSoup
from app.models import Gmina, Obwod


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
    cnt = 0

    for i in wojewodztwa:
        powiaty = get_deeper_links(base_site + i.a['href'])
        print cnt
        # if i.text < "mazowieckie":
        #     continue
        for powiat in powiaty:
            print cnt
            if ", m." in powiat.text or "Zagranica" in powiat.text or "Statki" in powiat.text:
                okr_miasta = get_deeper_links(base_site + powiat.a['href'])

                g, created = Gmina.objects.update_or_create(nazwa=powiat.text)

                for okrag in okr_miasta:
                    o, created = Obwod.objects.update_or_create(gmina=g, adres=okrag.text,
                                                                uprawnionych=0, ileKart=0)
                    cnt += 1
            else:
                gminy = get_deeper_links(base_site + powiat.a['href'])
                for j in gminy:
                    okregi_gminy = get_deeper_links(base_site + j.a['href'])
                    print j.text
                    # g = Gmina(nazwa=j.text)
                    g, created = Gmina.objects.update_or_create(nazwa=j.text)

                    for okrag in okregi_gminy:
                        o, created = Obwod.objects.update_or_create(gmina=g, adres=okrag.text,
                                                                    uprawnionych=0, ileKart=0)
                        cnt += 1

    # save_site("data", str(okregi_miast) + "\n" + str(okregi_gmin))
    print "Finished2 " + str(cnt)

class Command(BaseCommand):
    help = 'Pobiera gminy i okregi wyborcze do aplikacji'

    def handle(self, *args, **options):
        compute()