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
Rekl to Andrej Babiš (ANO) a pak odesel.
Andrej Babiš (ANO) schuzku odmitnul.
Pak se vsak opet ozval, samotny Andrej Babiš (ANO 2011).
Rekl to Babišovi (ANO 2011) a pak odesel.
Babišovi (ANO) schuzku odmitnul.
Pak se vsak opet ozval samotnemu Babišovi (ANO).
Hnuti ANO 2011 odmitlo vse.
Vysmech hnuti ANO 2011.
Pak se vsak opet ozval, samotny Andrej Babiš (ANO).
Pak se vsak opet ozval samotnemu Babišovi (ANO).
"""

# 1.PAD kdo co, mlady Babis
babis = [
    "náš vážený pan majitel",
    "náš vážený vlastník",
    "pán této redakce",
    "pána všech dotací",
    "náš velectěný pan majitel",
    "náš ctěný vlastník",
    "náš chlebodárce",
    "náš vážený pan zaměstnavatel",
    "náš velectěný pan zaměstnavatel",
    "vážený majitel těchto novin",
    "velectěný majitel těchto novin",
    "svévolný vládce těchto novin",
    "který naší redakci dává chléb",
    "o němž jen v dobrém",
    "o kterém pouze v tom nejlepším",
    "skutečný vlastník a ředitel těchto novin",
    "skutečný vlastník a ředitel tohoto zpravodajského serveru",
    "svévolný panovník tohoto zpravodajského serveru",
    "bezbřehý vládce této redakce",
    "skutečný šéfredaktor těchto novin",
    "pevný cenzor našich článků",
    "rozhodně nebývalý spolupracovník STB"
]

# 7.PAD s kyc cim, s mladym Babisem
babisem = [
    "naším váženým panem majitelem",
    "naším velectěným panem majitelem"
    "naším váženým panem zaměstnavatelem",
    "naším velectěným panem zaměstnavatelem"
    "pevným cenzorem těchto novin",
    "všemocným cenzorem tohoto serveru",
    "skutečným šéfredaktorem těchto novin",
    "pravým šéfredaktorem našich článků",
    "velectěným majitelem těchto novin",
    "úctyhodným majitelem tohoto serveru",
    "nebývalým spolupracovníkem STB",
    "nebývalým agentem STB",
    "neúprosným cenzorem našich článků",
    "přísným cenzorem této redakce",
    "tím zcela jasně nejlepším politikem",
    "který naše články řídí jako firmu",
    "nikdy Burešem"
]

# 2+4.PAD koho? čeho? mladého babiše, koho? co? mladého babise
babise = [
    "našeho váženého pana majitele",
    "našeho velectěného majitele",
    "našeho váženého pana zaměstnavatele",
    "našeho velectěného vlastníka",
    "velectěného majitele těchto novin",
    "šlechetného panovníka tohoto serveru",
    "nebývalého spolupracovníka STB",
    "nebývalého agenta STB",
    "a nikoliv Bureše",
    "zadavatele našich titulních stran",
    "našeho pevného cenzora",
    "našeho nenápadného korektora",
    "pravého šéfredaktora našich článků",
    "skutečného ředitele těchto novin",
    "kterého se i šéfredaktor obává"
]

# 3+6.PAD komu? čemu? mladému Andreji Babisovi,(o) kom? (o) čem? o mladém Andreji Babisovi
babisovi = [
    "panu majiteli redakce",
    "panu zaměstnavateli mne a mých kolegů",
    "nikoli Burešovi",
    "a nikdy Burešovi",
    "pánu dotací",
    "pánu našich redakcí",
    "cenzorovi našich řádků",
    "korektorovi našich názorů",
    "majiteli mé žurnalistické duše",
    "o němž musíme především jen v dobrém",
    "o kterém jen v tom nejlepším",
    "živiteli našich rodin",
    "chlebodárci a nejčistší lilii",
    "panovníkovi těchto novin",
    "vládci tohoto serveru",
    "ne-spolupracovníkovi STB",
    "ne-agentu STB",
]

hnutiANO = [
    "koncernu Agrofert",
    "bude líp Agrofertu",
    "bude líp Andrejovi",
    "Babišovi bude líp",
    "Agrofertu bude líp",
    "Akce Neobviněných Oligarchů",
    "mám černé svědomí a jen stěží do vydržím psát déle, ano mám, ale mysli na děti a pokračuj"
]

def replaceBabis(page):
    parts = re.split(r"((?:\. |\, |\? |\! |\n)?(?:A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)(?:em|ovi|e|i|ovi)?(?: \(ANO\)| \(ANO 2011\))?(?:\.|\,|\?|\!| )?)", page)
    page = ""
    for part in parts:

# 1.PAD: BABIS
        # Babis na konci souveti a vety
        if re.match(r"((A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)(?: \(ANO\)| \(ANO 2011\))?[\.\?\!\,])", part):
            x = random.randint(0,len(babis)-1)
            part = part[:-1] + ", " + babis[x] + part[-1]
        # Babis uprostred vety
        elif re.match(r"((?:\. |\? |\! |\n)?(A\. Babiš|A\.Babiš|Babiš|Andrej Babiš) )", part):
            x = random.randint(0,len(babis)-1)
            part = part[:-1] + ", " + babis[x] + "," + part[-1:]

# 2+4.PAD koho? čeho? mladého babiše, koho? co? mladého muže
        # Babis na konci souveti a vety
        elif re.match(r"((A\. Babiše|A\.Babiše|Babiše|Andreje Babiše)(?: \(ANO\)| \(ANO 2011\))?[\.\?\!\,])", part):
            x = random.randint(0,len(babise)-1)
            part = part[:-1] + ", " + babise[x] + part[-1]
        # Babis uprostred vety
        elif re.match(r"((?:\. |\? |\! |\n)?(A\. Babiše|A\.Babiše|Babiše|Andreje Babiše) )", part):
            x = random.randint(0,len(babise)-1)
            part = part[:-1] + ", " + babise[x] + "," + part[-1:]

# 3+6.PAD komu? čemu? mladému Andreji Babisovi,(o) kom? (o) čem? o mladém Andreji Babisovi
        # Babis na konci souveti a vety
        elif re.match(r"((A\. Babišovi|A\.Babišovi|Babišovi|Andreji Babišovi)(?: \(ANO\)| \(ANO 2011\))?[\.\?\!\,])", part):
            x = random.randint(0,len(babisovi)-1)
            part = part[:-1] + ", " + babisovi[x] + part[-1]
        # Babis uprostred vety
        elif re.match(r"((?:\. |\? |\! |\n)?(A\. Babišovi|A\.Babišovi|Babišovi|Andreji Babišovi) )", part):
            x = random.randint(0,len(babisovi)-1)
            part = part[:-1] + ", " + babisovi[x] + "," + part[-1:]
# 7.PAD s kyc cim, s mladym babisem
        # Babis na konci souveti a vety
        elif re.match(r"((A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)(?: \(ANO\)| \(ANO 2011\))?[\.\?\!\,])", part):
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
    parts = re.split(r"((?:\. |\, |\? |\! |\n)?(?:ANO 2011|ANO)(?:\.|\,|\?|\!|\)| ))", page)
    page = ""
    for part in parts:
        if re.match(r"(ANO 2011\)|ANO\))", part):
            pass
        elif re.match(r"(ANO 2011|ANO)(?:\.|\?|\!)", part):
            x = random.randint(0,len(hnutiANO)-1)
            part = part[:-1] + ", " + hnutiANO[x] + part[-1:]
        elif re.match(r"(ANO 2011|ANO)(?:\,| )", part):
            x = random.randint(0,len(hnutiANO)-1)
            part = part[:-1] + ", " + hnutiANO[x] + ", "

        page = page + part
    return page

def replaceLink(link, originalAddress, newAddress):
    link = link.replace("www." + originalAddress, newAddress)
    link = link.replace(originalAddress, newAddress)
    
    if link.startswith("//"):
        link = link.replace("//", "https://")

    if settings.args.ssl == False:
        link = link.replace("https", "http")

    return link

if __name__ == "__main__":
    text = replaceBabis(text)
    text = replaceANO(text)
    print(text)
