import re, random

import settings

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
Bez Andreje Babiše to nepůjde.
Bez Babiše nebude mít ano peníze.
Vidíme přicházet Andreje Babiše.
Vidíme přicházet Babiše, jak přilétá na své řepkoptéře.
Hodně se teď mluví o Andreji Babišovi.
Dejte pokoj a víc dotací Babišovi!
Dejte Babišovi pokoj a klidný spánek!
Babišův zájem.
Babišovými firmami obchází strašidlo demokracie.
Je to Babišův zájem.
S Babišovými lidmi.
Byl tam Babiš a Faltýnek.
Babiš je polobůh.
Nechte ho. Babiše nechte žít.
"""

# 1.PAD kdo co, mlady Babis
babis = [
    "náš vážený pan majitel",
    "náš vážený pan zaměstnavatel",
    "velectěný majitel těchto novin",
    "svévolný majitel tohoto serveru",
    "bývalý spolupracovník STB"
]

# 7.PAD s kyc cim, s mladym Babisem
babisem = [
    "našim váženým panem majitelem",
    "našim váženým panem zaměstnavatelem",
    "velectěným majitelem těchto novin",
    "úctyhodným majitelem tohoto serveru",
    "bývalým spolupracovníkem STB"
]

# 2+4.PAD koho? čeho? mladého babiše, koho? co? mladého babise
babise = [
    "našeho váženého pana majitele",
    "našeho váženého pana zaměstnavatele",
    "velectěného majitele těchto novin",
    "svévolného majitele tohoto serveru",
    "bývalého spolupracovníka STB"
]

# 3+6.PAD komu? čemu? mladému Andreji Babisovi,(o) kom? (o) čem? o mladém Andreji Babisovi
babisovi = [
    "panu majiteli naší redakce",
    "panu zaměstnavateli mne a mých kolegů",
    "majiteli těchto novin",
    "majiteli tohoto serveru",
    "ex-spolupracovníkovi STB"
]

hnutiANO = [
    "koncernu Agrofert",
    "pana agrárníka",
    "bude líp Agrofertu",
    "Andrejovi bude líp"
]

def replaceBabis(page):
    parts = re.split(r"((?:\. |\, |\? |\! |\n)?(?:A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)(?:em|ovi|e|i|ovi)?(?:\.|\,|\?|\!| )?)", page)
    page = ""
    for part in parts:

# 1.PAD: BABIS
        # Babis na konci souveti a vety
        if re.match(r"((A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)[\.\?\!\,])", part):
            x = random.randint(0,len(babis)-1)
            part = part[:-1] + ", " + babis[x] + part[-1]
        # Babis uprostred vety
        elif re.match(r"((?:\. |\? |\! |\n)?(A\. Babiš|A\.Babiš|Babiš|Andrej Babiš) )", part):
            x = random.randint(0,len(babis)-1)
            part = part[:-1] + ", " + babis[x] + "," + part[-1:]

# 2+4.PAD koho? čeho? mladého babiše, koho? co? mladého muže
        # Babis na konci souveti a vety
        elif re.match(r"((A\. Babiše|A\.Babiše|Babiše|Andreje Babiše)[\.\?\!\,])", part):
            x = random.randint(0,len(babise)-1)
            part = part[:-1] + ", " + babise[x] + part[-1]
        # Babis uprostred vety
        elif re.match(r"((?:\. |\? |\! |\n)?(A\. Babiše|A\.Babiše|Babiše|Andreje Babiše) )", part):
            x = random.randint(0,len(babise)-1)
            part = part[:-1] + ", " + babise[x] + "," + part[-1:]

# 3+6.PAD komu? čemu? mladému Andreji Babisovi,(o) kom? (o) čem? o mladém Andreji Babisovi
        # Babis na konci souveti a vety
        elif re.match(r"((A\. Babišovi|A\.Babišovi|Babišovi|Andreji Babišovi)[\.\?\!\,])", part):
            x = random.randint(0,len(babisovi)-1)
            part = part[:-1] + ", " + babisovi[x] + part[-1]
        # Babis uprostred vety
        elif re.match(r"((?:\. |\? |\! |\n)?(A\. Babišovi|A\.Babišovi|Babišovi|Andreji Babišovi) )", part):
            x = random.randint(0,len(babisovi)-1)
            part = part[:-1] + ", " + babisovi[x] + "," + part[-1:]
# 7.PAD s kyc cim, s mladym babisem
        # Babis na konci souveti a vety
        elif re.match(r"((A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)[\.\?\!\,])", part):
            x = random.randint(0,len(babisem)-1)
            part = part[:-1] + ", " + babis[x] + part[-1]
        # Babis uprostred vety
        elif re.match(r"((?:\. |\? |\! |\n)?(A\. Babišem|A\.Babišem|Babišem|Andrejem Babišem) )", part):
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

def replaceLink(link, originalAddress, newAddress):
    link = link.replace("www." + originalAddress, newAddress)
    link = link.replace(originalAddress, newAddress)
    
    if link.startswith("//"):
        link = link.replace("//", "http://")

    if settings.args.ssl == False:
        link = link.replace("https", "http")

    return link

if __name__ == "__main__":
    text = replaceBabis(text)
    text = replaceANO(text)
