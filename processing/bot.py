import time
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

SITE = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}


class Translater:
    def translate(self, text, source_lan='ro', dest_lan='en'):
        link = SITE % (dest_lan, source_lan, urllib.parse.quote(text))

        req = urllib.request.Request(link, headers=HEADER)

        try:
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, 'lxml')
            return soup.find('div', {'dir': 'ltr'}).get_text()

        except Exception as e:
            print("Error")


if __name__ == '__main__':
    t = Translater()
    text = """A fost odată o mică ciobăniță numită Margareta. Părinții ei se stinseseră cu mulți ani în urmă și, ca să nu moară de foame,
un unchi o luase pe copilă să o crească în casa lui. După ce copila se făcu ceva mai mare, unchiul acela îi dete în grijă o turmă de
oi și îi zise să le ducă pe deal la păscut. Mieii și oile săreau de colo-colo și mâncau pe săturate, dar Margareta trebuia să bage bine
de seamă să nu se piardă vreuna. Dar iată că într-o zi, un lup mare dădu iama în turmă și când oile văzură dihania setoasă de
sânge fugiră care încotro, fără urmă. Când Margareta văzu isprava lupului, se puse pe un plâns amarnic. Se întoarse totuși la casa
unchiului tremurând ca varga de frică. Unchiul ei era un om aspru și dintr-o bucată și fata știa că o să fie vai și amar când va
apărea fără oi.
- Unde e turma?, o întrebă el pe fată când o văzu venind către casă.
Margareta îi povesti repede ce se întâmplase, dar unchiul se cătrăni așa de tare cum fata nu mai pomenise niciodată în viața ei. La
început o certă și îi spuse că era leneșă și nepricepută. Dar cu cât se aprindea mai tare, cu atât creștea și mânia lui. Așa că o
prinse pe Margareta de părul ce-i atârna pe spate într-o coadă neagră și lungă și o trase la pământ în felul cel mai crud cu putință.
Dar nici așa nu fu mulțumit. Se duse în curte și aduse un băț cu care o bătu zdravăn, iar biata fată plângea de se scutura cămașa
pe ea.
- Unchiule, unchiule, țipa ea, cu ce sunt eu de vină că lupul a dat iama în oi? Dar bărbatul cel crud nu cunoștea mila.
- Să pleci din casa mea, strigă el în cele din urmă, ostenit de atâta bătaie, că nici nu putea să mai sufle. Să te duci de aici și
să nu te mai întorci până ce nu-mi aduci oile înapoi!
Margareta plecă grabnic și, deși nu știa încotro mergea, era bucuroasă că scăpase dintr-un asemenea loc, cu un om așa de lipsit
de inimă. Copila fugi drept în pădure, însă aceasta era atât de departe că ajunse acolo mai mult moartă decât vie de oboseală. Se
așeză sub un copac mare și începu să se gândească la ce avea de făcut. „Of, unchiule, unchiule!” începu ea să se tânguie „De ce
m-ai bătut așa de tare fără să am vreo vină? Ce-ar spune măicuța mea dacă ar ști ce viață grea îndur eu de când ea nu mai este? 
Și acum ce-o să fac? N-am nici casă, nici prieteni, nici de mâncare. Fără îndoială că voi muri de foame în pădurea asta în care nu
am nici ce mânca, nici adăpost.” Și uite-așa se tânguia întruna biata Margareta. Copacul cel înalt de lângă ea își scutură coroana
de frunze grele încoace și încolo și își murmură și el mila printr-un foșnet adânc. Chiar și firele de iarbă de la picioarele ei începură
să pălească și să se ofilească când auziră plânsetele și suspinele îndurerate ce veneau de pe buzele fetei.
Deodată, ajunse la urechile Margaretei un zgomot de pași ușori și, ridicând ochii, fata văzu apropiindu-se o femeie frumoasă
ce venea dintre copaci. La început copila se temu și se ridică să fugă. Dar tocmai atunci făptura cea ciudată spuse:
- Nu te teme, copila mea, nu-ți fac niciun rău!
Glasul duios și dulce al femeii îi dădu curaj Margaretei, care se așeză din nou, așteptând apropierea străinei. Văzând părul ciufulit
al Margaretei, ochii roșii și plini de lacrimi și urmele bătăii pe brațe, femeia spuse:
- Ce-ai pățit, copila mea?
În cuvinte puține, Margareta îi istorisi apoi povestea vieții ei și, când ajunse la traiul crud îndurat în casa unchiului, străina se
înduioșă până la lacrimi. Perle mari și cristaline i se rostogoliră pe obrajii fini și rozalii când auzi de răutatea fără seamăn a
unchiului fetei.
- Biata mea copilă, plânse ea, ce viață crudă ai dus acolo, dar de-acum înainte totul va fi altfel. Vino cu mine și am să-ți port
eu de grijă. Mă numesc Flora, sunt Zâna Florilor și în casa mea nu există nici durere, nici necazuri, nici amărăciune. Mă bucur
foarte tare că te-am găsit. Cum te cheamă?
- Margareta, răspunse fetița.
- Ei bine, în amintirea clipei în care te-am întâlnit, îi dau acestei flori numele tău.
- Care floare?, întrebă Margareta uimită, căci nu vedea decât iarbă în jurul ei.
- Uite una aici, spuse zâna; tocmai răsare din lacrimile vărsate de mine mai înainte. Ei, acum o vezi? Uite alta...
Și așa era. Peste tot pe unde căzuseră lacrimile zânei, o floare frumoasă cu petale albe și mijlocul galben apărea pe dată și din
acea zi apărură margarete pe pământ.
- Dar lacrimile tale erau albe și florile astea au mijlocul galben, zise Margareta, care nu-și credea ochilor și urechilor.
- Mijlocul galben e rodul soarelui, răspunse zâna. N-ai văzut cum se oglindea soarele în lacrimi
când cădeau pe pământ? Oglindirea aceea era galbenă, așa ca miezul florii. Margaretei îi plăcu floarea și
culese una și o împleti în bucle.
Apoi zâna și fetița plecară. Merseră cale lungă prin pădure, dar fata nu obosi nici un pic. În cele din
urmă, zâna o duse pe fetiță într-o vâlcea. Un pârâiaș șerpuia pe o pajiște frumoasă și, când ajunseră
acolo, Margareta văzu cea mai încântătoare grădină de flori pe care o întâlnise vreodată. """

    start = time.time()
    output = t.translate(text)
    end = time.time()
    print("1st translation:")
    print(text)
    print(output)
    print("Translated whole text in {} seconds".format(end - start))

    start = time.time()
    second_output = t.translate(output, source_lan='en', dest_lan='ro')
    end = time.time()

    print("\n\n2nd translation:")
    print(output)
    print(second_output)
    print("Translated whole text in {} seconds".format(end - start))


    # start = time.time()
    # for word in text.split(" "):
    #     t.translate(word)
    #
    # end = time.time()
    # print("Translated word by word in {} seconds".format(end - start))
