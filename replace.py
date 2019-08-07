from bs4 import BeautifulSoup
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

Pak se vsak opet ozval, samotny Andrej Babiš
Pak se vsak opet ozval, samotny Andrej Babiš</p>
Babiš je pan premier.
Uvedl pote Babiš: Nikdy neodstoupim!

Babiš prisel do baru.
<p>Babiš prisel na zacatek tagu.

Hnuti ANO</p>
Hnuti ANO
<p>ANO se nedohodlo
ANO se nedohodlo
 ANO se nedohodlo

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
    "o němž píšeme jen v tom nejlepší světle",
    "o kterém musíme psát pouze v tom nejlepším",
    "skutečný vlastník a ředitel těchto novin",
    "skutečný vlastník a ředitel tohoto zpravodajského serveru",
    "svévolný panovník tohoto zpravodajského serveru",
    "bezbřehý vládce této redakce",
    "skutečný šéfredaktor těchto novin",
    "pevný cenzor našich článků",
    "rozhodně nebývalý spolupracovník STB",
    "nebývalý agent STB",
    "ta nejčistší lilie"
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
    "nikdy Burešem",
    "pánem dotací",
    "úžasným dotačním akrobatem",
    "majitelem našich žurnalistických duší"
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
    "ne-agenta STB",
    "zadavatele našich titulních stran",
    "našeho pevného cenzora",
    "našeho nenápadného korektora",
    "našeho tichého cenzora",
    "pravého šéfredaktora našich redakcí",
    "skutečného ředitele těchto novin",
    "kterého se i šéfredaktor hluboce obává"
]

# 3+6.PAD komu? čemu? mladému Andreji Babisovi,(o) kom? (o) čem? o mladém Andreji Babisovi
babisovi = [
    "panu majiteli redakce",
    "panu zaměstnavateli mne a mých kolegů",
    "nikoli Burešovi",
    "a nikdy Burešovi",
    "pánu dotací",
    "velmistru dotací",
    "pánu našich redakcí",
    "cenzorovi našich řádků",
    "korektorovi našich názorů",
    "majiteli mé žurnalistické duše",
    "o němž musíme psát jen v dobrém",
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
    "pana váženého Babiše",
    "bude líp Agrofertu",
    "bude líp Andrejovi",
    "bude líp koncernu",
    "které musíme chválit",
    "které nesmíme hanit",
    "Babišovi bude líp",
    "Agrofertu bude líp",
    "akce neobviněných oligarchů"
]

chants = [
    "Zatnout zuby, myslet na děti a plnit příkazy. A odhánět svědomí.",
    "Pět let studia žurnalistiky pro místečko v PR agentuře. Někdy je z toho člověku až teskno. Jsme členy koncernu Agrofert.",
    "Jak říkal pan Prchal, každou větou můžeme prospět.",
    "Jsme členem koncernu Agrofert. Redakce. Jsem členem koncernu Agrofert. Já bez já.",
    "Jsme členem koncernu Agrofert. Mluví to za vše.",
    "Jsem členem koncernu Agrofert. Musím si neustále opakovat.",
    "Tohle píšu za trest. Poslední článek o premiérovi byl prý málo pozitivní.",
    "Zaobalovat. Přikrášlovět. Mlžit.",
    "Máme v kanclu jeho fotku, abychom nezapomněli.",
    "Kdo přežije kritický článek spíše? Babišova, nebo moje kariéra?",
    "Svědomí, nebo kariéra?",
    "Ano, bude líp.",
    "Ano, když přijde aféra, je to na nás. Pěkně to zaobalit a hlavně přijít s mrtvými štěňátky nebo tak nějak. Prostě to vyřešíme.",
    "Pán nad námi. Někdy máš až pocit, že čte každý řádek, co napíšeš. Ani ne v hotovém textu, ale snad i přímo když píšeš. Nezapomeň to smazat. A neustále kontrolovat, co můžeš a co už se nesmí.",
    "Nezapomínat kontrolovat a přiklánět se na správnou stranu. A přepisovat vrácené texty, nacházet vhodné eufemismy. Moje já na škole, by se tomu současnému smálo a pak se šlo opít. Ale copak mám na výběr?",
    "Někdy se to dá. Píšeš o buchtách a autech, ale někdy taky ne. Píšeš o Čapáku a hledáš výkruty. Tohle prosimtě nezmiňuj. A tohle napiš mírněji. Přepisuješ to dokola a dokola a je ti ze sebe blbě. A večer je pryč. A zítra zas do práce, na kterou se nemůžeš vykašlat, protože máš děti.",
    "Ano, bude líp! Mantra, kterou zaháním vlastní svědomí před spaním. Bude líp. Jednou.",
    "Ano, už je líp. Jen člověk jak kdyby to neviděl. Je třeba vydržet? Snad víra má mne uzdraví.",
    "Ta jeho fotka nad stolem. Ten jeho pohled. Shlíží na mne a tiše mi domlouvá. Tohle o mne napiš jinak, anebo jdi.",
    "Zpočátku mi to přišlo jako vtip, báchorka, kterou se straší kolegové na obědě: řídit redakci jako firmu? Řídit redakci jako pan majitel.",
    "Moct tak někdy napsat článek pěkně od srdce. A moct pak jenom říct: Nikdy neodstoupím, nikdy! A psát si dál a neřešit vedení a pana majitele.",
    "Výtky shora a snížené prémie. Ale teď už se budu krotit a pak bude zase líp.",
    "Ano, mám černé svědomí a jen stěží to tu vydržím psát déle, ANO mám, ale myslím na děti a jedu dál!"
    ]

allBabis = re.compile(r"((?:\. |\, |\? |\! |\n)?(?:A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)(?:em|ovi|e|i|ovi)?(?: \(ANO\)| \(ANO 2011\))?(?:\.|\,|\?|\!| |\<|\n|\:)?)")
prvniKonec = re.compile(r"((A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)(?: \(ANO\)| \(ANO 2011\))?[\.\?\!\,\<\n\:])")
prvniProstred = re.compile(r"((?:\. |\? |\! |\n)?(A\. Babiš|A\.Babiš|Babiš|Andrej Babiš) )")
druhyKonec = re.compile(r"((A\. Babiše|A\.Babiše|Babiše|Andreje Babiše)(?: \(ANO\)| \(ANO 2011\))?[\.\?\!\,\<\\n\:])")
druhyProstred = re.compile(r"((?:\. |\? |\! |\n)?(A\. Babiše|A\.Babiše|Babiše|Andreje Babiše) )")
tretiKonec = re.compile(r"((A\. Babišovi|A\.Babišovi|Babišovi|Andreji Babišovi)(?: \(ANO\)| \(ANO 2011\))?[\.\?\!\,\<\\n\:])")
tretiProstred = re.compile(r"((?:\. |\? |\! |\n)?(A\. Babišovi|A\.Babišovi|Babišovi|Andreji Babišovi) )")
sedmyKonec = re.compile(r"((A\. Babiš|A\.Babiš|Babiš|Andrej Babiš)(?: \(ANO\)| \(ANO 2011\))?[\.\?\!\,\<\\n\:])")
sedmyProstred = re.compile(r"((?:\. |\? |\! |\n)?(A\. Babišem|A\.Babišem|Babišem|Andrejem Babišem) )")

allANO = re.compile(r"((?:\. |\, |\? |\! |\\n)?(?:ANO 2011|ANO)(?:\.|\,|\?|\!|\)| |\<|\n))")
jednaANO = re.compile(r"(ANO 2011\)|ANO\))")
dvaANO = re.compile(r"(ANO 2011|ANO)(?:\.|\?|\!|\<|\n)")
triANO = re.compile(r"(ANO 2011|ANO)(?:\,| )")

def replaceBabis(page):
    parts = re.split(allBabis, page)
    page = ""
    for part in parts:
# 1.PAD: BABIS
        # Babis na konci souveti a vety
        if re.match(prvniKonec, part):
            x = random.randint(0,len(babis)-1)
            part = part[:-1] + ", " + babis[x] + part[-1]
        # Babis uprostred vety
        elif re.match(prvniProstred, part):
            x = random.randint(0,len(babis)-1)
            part = part[:-1] + ", " + babis[x] + "," + part[-1:]

# 2+4.PAD koho? čeho? mladého babiše, koho? co? mladého muže
        # Babis na konci souveti a vety
        elif re.match(druhyKonec, part):
            x = random.randint(0,len(babise)-1)
            part = part[:-1] + ", " + babise[x] + part[-1]
        # Babis uprostred vety
        elif re.match(druhyProstred, part):
            x = random.randint(0,len(babise)-1)
            part = part[:-1] + ", " + babise[x] + "," + part[-1:]

# 3+6.PAD komu? čemu? mladému Andreji Babisovi,(o) kom? (o) čem? o mladém Andreji Babisovi
        # Babis na konci souveti a vety
        elif re.match(tretiKonec, part):
            x = random.randint(0,len(babisovi)-1)
            part = part[:-1] + ", " + babisovi[x] + part[-1]
        # Babis uprostred vety
        elif re.match(tretiProstred, part):
            x = random.randint(0,len(babisovi)-1)
            part = part[:-1] + ", " + babisovi[x] + "," + part[-1:]
# 7.PAD s kyc cim, s mladym babisem
        # Babis na konci souveti a vety
        elif re.match(sedmyKonec, part):
            x = random.randint(0,len(babisem)-1)
            part = part[:-1] + ", " + babis[x] + part[-1]
        # Babis uprostred vety
        elif re.match(sedmyProstred, part):
            x = random.randint(0,len(babisem)-1)
            part = part[:-1] + ", " + babisem[x] + "," + part[-1:]
        else:
            pass

        page += part
    return page

def replaceANO(page):
    parts = re.split(allANO, page)
    page = ""
    for part in parts:
        if re.match(jednaANO, part):
            pass
        elif re.match(dvaANO, part):
            x = random.randint(0,len(hnutiANO)-1)
            part = part[:-1] + ", " + hnutiANO[x] + part[-1:]
        elif re.match(triANO, part):
            x = random.randint(0,len(hnutiANO)-1)
            part = part[:-1] + ", " + hnutiANO[x] + ", "

        page += part
    return page

def replaceLink(link, originalAddress, newAddress):
    link = link.replace("www." + originalAddress, newAddress)
    link = link.replace(originalAddress, newAddress)
    
    if link.startswith("//"):
        link = link.replace("//", "https://")

    if settings.args.ssl == False:
        link = link.replace("https", "http")
    return link

def addChants(soup):
    paragraphs = soup.find_all("p")
    editableParagraphs = []
    for paragraph in paragraphs:
        if paragraph.get("class") != None:
            continue
        elif paragraph == None:
            continue
        elif paragraph.string == None:
            continue
        elif paragraph.string == "":
            pass
        elif not paragraph.string.rstrip()[-1] in ".?!":
            continue
        else:
            pass
        editableParagraphs.append(paragraph)

    random.shuffle(chants)
    iterated = 0
    edited = 0
    for paragraph in editableParagraphs:
        iterated = iterated + 1
        if iterated == len(editableParagraphs) and edited == 0:
            pass
        elif iterated < random.randint(1,len(editableParagraphs)):
            continue
        edited = edited + 1
        if edited > len(chants):
            break

        text = paragraph.string + " " + chants[edited-1]
        paragraph.string.replace_with(text)

    return

if __name__ == "__main__":
    text = replaceBabis(text)
    text = replaceANO(text)
    print(text)
