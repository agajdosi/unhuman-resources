import re, random
from bs4 import BeautifulSoup

text = """
Ironie. Babiš vytáhl do boje proti dvoji kvalite potravin.
Je to Blbost? Babiš si to nemysli!
Je to marketingova realita! Babiš nakonec shrnul svuj postoj.
Ironie. Babiš vytáhl do boje proti dvoji kvalite potravin.
Je to Blbost? Babiš si to nemysli!
Je to marketingova realita! Babiš nakonec shrnul svuj postoj.
A. Babiš se nechal slyšet, že nic nevrátí.
Babiš se nechal slyšet, že nikdy neodstoupí.
Andrej Babiš se nechal slyšet, že je vše kampaň.
Premiér A. Babiš priletel na navstevu Capiho hnizda.
Cekalo tam na nej hovno od mistni opozice. A. Babiš do nej omylem slapnul.
Po jednání se zástupci obchodních řetězců o tom mluvil premiér Andrej Babiš.
Chtěl bych jít už domů, řekl Andrej Babiš, a šel zase pracovat.
Do obchodu přišel Andrej Babiš a šel s účtenkou zase dál.
Na jednani s Babišem chyběl Hamáček.
S hnutím ANO do vlady nepujdu, rek Hamacek.
Hnuti ANO 2011 je nejlepsi, tvrdi stale dokola Babiš.
Takhle ne! Hnutí ANO se distancuje od ČSSD.
Kašlem na to, shodlo se Hnutí ANO.
"""

babis = [
    "náš vážený pan majitel",
    "náš vážený pan zaměstnavatel",
    "velectěný majitel těchto novin",
    "svévolný majitel tohoto serveru",
    "bývalý spolupracovník STB"
]

babisem = [
    "našim váženým panem majitelem",
    "našim váženým panem zaměstnavatelem",
    "velectěným majitelem těchto novin",
    "úctyhodným majitelem tohoto serveru",
    "bývalým spolupracovníkem STB"
]

hnutiANO = [
    "koncernu Agrofert",
    "pana agrárníka",
    "bude líp Agrofertu",
    "Andrejovi bude líp"
]

def replaceBabis(page):
    parts = re.split(r"((?:\. |\, |\? |\! |\n)?(?:A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)(?:em|ovi|e|i|ovi)?(?:\.|\,|\?|\!| )?)", page)
    print(parts)
    page = ""
    for part in parts:
        
        # Babis v zacatku souveti
        if re.match(r"((?:\. |\? |\! |\n)(A\. Babiš|A\.Babiš|Babiš|Andrej Babiš))", part):
            #part = part[0:2] + prepend[x].capitalize() + ", " + part[2:]
            x = random.randint(0,len(babis)-1)
            part = part[:-1] + ", " + babis[x] + "," + part[-1:]
        # Babis na konci souveti a vety
        elif re.match(r"((A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)[\.\?\!\,])", part):
            x = random.randint(0,len(babis)-1)
            part = part[:-1] + ", " + babis[x] + part[-1]
        # Babis uprostred vety
        elif re.match(r"((A\. Babiš|A\.Babiš|Babiš|Andrej Babiš) )", part):
            x = random.randint(0,len(babis)-1)
            part = part[:-1] + ", " + babis[x] + "," + part[-1:]
        elif re.match(r"((A\. Babišem|A\.Babišem|Babišem|Andrejem Babišem) )", part):
            x = random.randint(0,len(babisem)-1)
            part = part[:-1] + ", " + babisem[x] + "," + part[-1:]
        else:
            pass

        page = page + part
    return page

def replaceANO(page):
    parts = re.split(r"((?:\. |\, |\? |\! |\n)?(?:ANO 2011|ANO)(?:\.|\,|\?|\!| )?)", page)
    page = ""
    for part in parts:
        if re.match(r"(ANO 2011|ANO)(?:\,| )", part):
            x = random.randint(0,len(hnutiANO)-1)
            part = part[:-1] + ", " + hnutiANO[x] + ", "
        elif re.match(r"(ANO 2011|ANO)(?:\.|\?|\!)", part):
            x = random.randint(0,len(hnutiANO)-1)
            part = part[:-1] + ", " + hnutiANO[x] + part[-1:]
        page = page + part
    return page

def replaceLinks(html, originalAddress, newAddress):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all("a"):
        try:
            link["href"] = link["href"].replace("www." + originalAddress, newAddress)
            link["href"] = link["href"].replace(originalAddress, newAddress)
            link["href"] = link["href"].replace("https", "http")
        except:
            print(link)
    return str(soup)

if __name__ == "__main__":
    text = replaceBabis(text)
    text = replaceANO(text)
    print(text)