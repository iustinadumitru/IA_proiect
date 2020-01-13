import re
import nltk
import time
import traceback
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


class TranslatorException(BaseException):
    def __init__(self, msg=""):
        super().__init__(msg)


class Translator:
    def __init__(self):
        self.LIMIT = 5000
        self.SITE = "http://translate.google.com/m?hl=%s&sl=%s&text=%s"
        self.HEADER = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    def translate(self, text, source_lan='ro', dest_lan='en'):
        translated_text = ""
        request_text = ""
        request_size = 0

        sentences = nltk.sent_tokenize(text)
        nr_of_sentences = len(sentences)

        for index in range(len(sentences)):
            length_current_sentence = len(sentences[index])
            if request_size + length_current_sentence < self.LIMIT:
                request_size += length_current_sentence
                request_text += " " + (sentences[index])

                if index < nr_of_sentences - 1:
                    continue

            try:
                link = self.SITE % (dest_lan, source_lan, urllib.parse.quote(request_text))
                req = urllib.request.Request(link, headers=self.HEADER)

                page = urllib.request.urlopen(req)
                soup = BeautifulSoup(page, 'lxml')
                translated_text += " " + soup.find('div', {'dir': 'ltr'}).get_text()

                request_text = sentences[index]
                request_size = length_current_sentence

            except Exception as e:
                raise TranslatorException("Something went wrong while translating text, {}".
                                          format(traceback.format_exc()))

        return translated_text

    def translate_words(self, words, source_lan='ro', dest_lan='en'):
        translated_words = ""
        request_words = ""
        request_size = 0

        words = list(filter(lambda x: x not in ".,!?\"\'„”;", words))
        words = list(map(lambda x: re.sub("[.,!?\"\'„”;]", "", x), words))
        nr_of_words = len(words)

        for index in range(len(words)):
            current_size = len(words[index]) + 1

            if request_size + current_size < self.LIMIT:
                request_words += words[index] + "|"
                request_size += current_size

                if index < nr_of_words - 1:
                    continue

            try:
                link = self.SITE % (dest_lan, source_lan, urllib.parse.quote(request_words))
                req = urllib.request.Request(link, headers=self.HEADER)

                page = urllib.request.urlopen(req)
                soup = BeautifulSoup(page, 'lxml')
                translated_words += soup.find('div', {'dir': 'ltr'}).get_text() + "|"

                request_words = words[index]
                request_size = current_size

            except Exception:
                raise TranslatorException("Something went wrong while translating text, {}".
                                          format(traceback.format_exc()))

        translated_words = translated_words.split("|")
        translated_words = list(map(lambda x: x.lower().strip(), translated_words))
        return list(zip(words, translated_words))


if __name__ == '__main__':
    t = Translator()
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
acolo, Margareta văzu cea mai încântătoare grădină de flori pe care o întâlnise vreodată. Căsuța în care o
conduse zâna era făcută din cele mai înmiresmate plante urcătoare, pereții erau din floarea-soarelui iar
acoperișul era învelit în milioane de zorele, ale căror flori străluceau printre frunzele verzi ca niște steluțe
viorii, roz sau albe. Ochii Margaretei rătăciră uluiți de la o floare la alta, iar zâna părea să se bucure de
uimirea ei. Din clipa în care Margareta intră în casa zânei, uită pe loc tot trecutul ei amar și toată durerea
pe care unchiul ei cel rău i-o pricinuise.
A doua zi zâna o duse prin poienile și grădinile din jurul casei și, la fiecare pas, fata vedea încă o
minune și încă o nouă frumusețe din lumea florilor. Dar ce ciudat! Nu erau
trandafiri nicăieri în grădini. Când zâna ajunse la capătul unei poieni, îi zise Margaretei:
- Vezi tufele alea țepoase care cresc acolo? Ei bine, au fost sădite de stră-străbunica mea cu mii
de ani în urmă și, pe când trăia ea, erau pline de cele mai frumoase flori roșii. În ziua morții ei toate
acele flori au murit și ele și nici una nu a mai înflorit de atunci și nici nu cred să o mai facă vreodată.
Zâna Flora și mica ei prietenă trăiau acolo foarte fericite împreună. Fetița se făcea foarte de
folos ajutând-o pe zână să aibă grijă de flori și să smulgă buruienile care răsăreau uneori din pământ.
Într-o zi, când Margareta n-avea nimic de făcut, merse printre tufele țepoase. Deodată auzi o voce și,
când se opri să asculte, desluși aceste cuvinte:
Dacă în deget îți vor intra spini
Flori roșii vor înflori pe tulpini.
De trei ori auzi Margareta aceste cuvinte, așa că se apropie de tufe și își înfipse degetul într-un
spin. Sângele țâșni din rană și se scurse pe tulpinile tufișului. Și oriunde ajungea sângele, o
floare roșie și frumoasă se deschidea. Fetița nu mai putea de bucurie și o chemă imediat pe
Flora să-i arate ce făcuse. Zâna se miră când văzu minunatele flori.
- Astea sunt florile pe care le avea și stră-străbunica mea! Acum hai să mergem la Regina
Zânelor să te răsplătească, draga mea, căci ea a spus că oricine va aduce înapoi trandafirii, îi va
fi prietenă pe veci.
Așa că Margareta merse la Regina Zânelor și, când Flora, Zâna Florilor, vorbi de isprava fetei,
regina se ridică de pe tron, o îmbrățișă și o sărută pe copilă. O rugă să rămână cu ea la palat și
Margareta rămase în Țara Zânelor pentru totdeauna.

Într-o grădină mare și frumoasă stătea micuța Annie singură-singurică și părea tare abătută căci niște picături ce nu erau de
rouă cădeau de zor pe florile din jur, care se uitau mirate în sus și se aplecau tot mai mult spre ea ca și cum voiau s-o mângâie și
s-o înveselească. Vântul călduț îi ridica părul auriu și o săruta ușor pe obraji, în timp ce razele soarelui, îndreptate cu blândețe spre
fața ei, făceau mici curcubee în lacrimile care cădeau și dansau cu drăgălășenie în jurul ei. Dar Annie nu se uita nici la raze, nici la
vânt, nici la flori; iar lacrimile-i cristaline cădeau necontenit făcând-o să uite de toate și să se cufunde în amărăciune.
- Micuță Annie, spune-mi de ce plângi, îi șopti o voce subțirică în ureche; și, uitându-se în sus, copila văzu o făptură mititică
ce stătea pe o frunză de viță chiar lângă ea; o fețișoară drăgălașă îi zâmbea dintre niște bucle aurii și două aripioare sclipitoare
stăteau îndoite pe o mantie albă și lucitoare ce flutura în vânt.
- Cine ești tu, făptură minunată?, strigă Annie zâmbind printre lacrimi.
- Sunt o zână, copiliță dragă, și-am venit să te ajut și să te alin. Acum spune-mi de ce plângi și lasă-mă să fiu prietena ta,
răspunse mica făptură și zâmbi cu și mai mare blândețe spre chipul mirat al lui Annie.
- Și ești chiar o zână, așa cum am citit în cărțile mele cu povești? Zbori călare pe fluturi, dormi în potirele florilor și trăiești
printre nori?
- Da, chiar așa fac și încă multe alte lucruri bizare pe care cărțile tale cu povești nu ți le pot spune. Dar acum, dragă Annie,
șopti zâna aplecându-se și mai mult către fetiță, spune-mi de ce nu râde soarele în ochii tăi? De ce strălucesc aceste lacrimi mari
pe florile din jur și de ce stai aici singură când păsările și albinele te cheamă la joacă?
- Ah, mă vei urî dacă îți spun, zise Annie și lacrimile începură iar să cadă. Sunt nefericită pentru că nu sunt cuminte. Cum să
învăț să devin o fetiță ascultătoare și bună, draga mea zână, cum?
- Te voi ajuta bucuroasă, dragă Annie, și dacă vrei cu adevărat să fii fericită, trebuie să faci loc în inima ta pentru lucruri și
simțăminte de preț. E greu ce îți cer, dar îți voi dărui această floare fermecată ca să te sfătuiască. Apleacă-te spre mine ca să ți-o
pot pune la piept; din acel loc nu ți-o poate lua nimeni până ce nu desfac eu vraja ce o va ține acolo.
Și după ce spuse toate astea, zâna scoase de sub mantie o floare delicată, ale cărei frunze străluceau cu o lumină serafică.
- E o floare fermecată, spuse ea. Nu o poate vedea nimeni în afară de tine. Acum ascultă și-ți spun
ce puteri are. Atunci când inima ți se umple de iubire, dacă faci o faptă bună sau duci ceva la
îndeplinire, din floare se va ridica cel mai dulce și mai suav parfum, care te va răsplăti și te va
înveseli. Dar dacă vreo vorbă urâtă îți va ajunge pe buze, sau dacă porniri rele îți vor izvorî din inimă
și vei face vreo faptă necugetată sau nemiloasă, atunci vei auzi clinchetul delicat al potirului florii
fermecate. Să-l asculți cu luare-aminte și să lași vorba nerostită și fapta nefăcută, căci vei găsi în
bucuria tihnită a inimii tale și în parfumul magic ascuns în sân o răsplată din cele mai plăcute.
- O, zână bună, cum să-ți mulțumesc pentru acest dar minunat?, strigă Annie. Voi fi bună și
voi da ascultare clopoțelului meu ori de câte ori va suna. Dar pe tine te voi mai vedea? O, dacă ai
mai sta cu mine, ce frumos m-aș purta!
- Nu mai pot zăbovi, mică Annie, spuse zâna, dar când va veni iar primăvara, voi fi din nou
aici ca să văd dacă darul meu fermecat și-a împlinit menirea. Și acum, rămas bun, copilă dragă! Fii
cuminte și floarea nu se va ofili niciodată.
Și buna zână își petrecu brațele pe după gâtul fetiței, o sărută delicat pe obraz și,
întinzându-și aripioarele sclipitoare, își luă zborul cântând printre norii albi ce pluteau pe cer. Și mica Annie rămase printre flori și
privi cu mirare și bucurie floarea fermecată ce-i strălucea la piept.
Plăcutele zile de primăvară și vară trecură, iar în grădina micuței Annie începură să înflorească pretutindeni florile toamnei
care se făceau tot mai frumoase și mai strălucitoare cu fiecare zi, hrănite de soare și rouă. Dar floarea fermecată, cea care ar fi 
trebuit să fie cea mai mândră dintre toate, atârna ofilită și palidă la pieptul fetei. Parfumul ei parcă dispăruse iar clopoțelul potirului
suna adesea in urechile ei. Atunci când zâna o pusese acolo, fata fusese încântată de noul dar și o vreme dăduse ascultare
clopoțelului fermecat. Deseori încerca să atragă și minunatul parfum prin fapte și cuvinte pline de bunătate. Și, așa cum spusese
zâna, întotdeauna se bucura de dulcea răsplată a parfumului suav și ciudat al florii fermecate ce strălucea la pieptul ei. Dar gânduri
rele veneau să o amăgească, spunea ea, și cuvinte urâte îi cădeau de pe buze; și atunci floarea se ofilea și își pierdea parfumul,
clopoțelul fermecat suna trist iar Annie uita tot ce făgăduise și devenea iar un copil mofturos și îndărătnic.
În cele din urmă lăsă orice strădanie la o parte și se mânie pe biata floare, vrând
chiar să o smulgă de la piept. Dar vraja o ținea acolo cu putere, iar cuvintele pline de
mânie nu făceau decât să scuture și mai tare clopoțelul care suna tot mai trist. Până la
urmă fata nu mai dădu atenție clinchetului cristalin ce-i suna în urechi și deveni tot mai
răuvoitoare și mai nemulțumită cu fiecare zi. Așa că, atunci când sosi toamna, Annie nu
mai era defel încântată de darul bunei zâne, ci aștepta primăvara pentru a-l putea
înapoia. Căci sunetul necontenit al îndureratului clopoțel o întrista amarnic.
Într-o dimineață însorită cu vânticel răcoros și proaspăt și fără un nor pe cer,
mica Annie se plimba printre flori, privind cu băgare de seamă în fiecare potir și
nădăjduind să o găsească în vreunul pe zână, care să-i ia floarea de la piept. Fata
ridica frunzele plecate și privea în căușurile lor înrourate în zadar; nicio zână nu stătea
ascunsă acolo, iar Annie le întoarse spatele și își zise cu tristețe: „Mă voi duce pe pajiște și în pădure și-o voi căuta acolo pe zână.
Nu vreau să mai aud clinchetul ăsta plicticos și nici să mai port la piept floarea asta ofilită.” Așa că merse pe pajiște, unde iarba
înaltă îi foșnea sub tălpi și păsări sfioase o priveau din cuiburi, unde frumoase flori de câmp se clătinau în vânt și își deschideau
petalele înmiresmate să primească în ele albine zumzăitoare, și unde fluturii, ca niște floricele cu aripi, dansau și sclipeau în lumina
soarelui.
Micuța Annie se uită, căută și întrebă dacă nu știa cineva ceva despre zâna cea mică. Dar păsările o priviră cu mirare cu
ochișorii lor licăritori și delicați și continuară să cânte. Florile se clătinară demne pe tulpinile lor și tăcură, iar fluturii și albinele
zumzăiră și zburară mai departe, prea distrați sau prea ocupați să zăbovească și să dea vreun răspuns.
Annie merse apoi prin lanuri mari de grâne care dansau în jurul ei ca o pădure de aur. Aici țârâiau greierii, săreau cosașii și
munceau furnicile harnice, dar nici aceștia nu-i putură răspunde la întrebări. „Mă voi duce printre dealuri” își zise Annie „și poate o
voi găsi acolo.” Așa că o apucă pe povârnișurile verzi unde căută și strigă în zadar căci zâna nu apăru. Se duse pe malul râului și
le întrebă pe jucăușele libelule și pe nuferii albi și liniștiți dacă n-o văzuseră pe zână; dar undele albastre clipociră pe nisipul alb de
la picioarele ei și nimeni nu răspunse.
Apoi se duse în pădure și pe când trecea pe potecile umbroase și răcoroase și se afunda printre crengi florile îi surâdeau,
veverițele zglobii o priveau pe furiș, turturelele gângureau încetișor; dar nimeni nu-i răspunse. Obosită de atâta căutare zadarnică și
îndelungată, se așeză între ferigi și se îndestulă cu frăguțele trandafirii ce creșteau lângă ea, privind norii stacojii ai înserării ce
străluceau în jurul soarelui la asfințit.
Vântul nopții foșni printre ramuri legănând florile pentru somn; păsările își cântară imnurile nocturne și toate cele din pădure
fură acoperite de liniște; și tot mai palidă deveni lumina roșiatică a înserării, iar capul lui Annie se aplecă tot mai mult; ferigile se
întinseră să o ferească de rouă și pinii șoptitori îngânară un duios cântecel de leagăn; iar când luna răsări, lumina ei argintie
străluci pe copila cuibărită pe mușchiul verde și adormită printre flori în bătrâna pădure umbroasă.
Și toată noaptea lângă ea stătu zâna pe care o căutase atât și care, printr-o vrajă tainică, îi trimise fetei adormite un vis.
Mica Annie visă că stătea în grădina ei, așa cum făcea adesea, cu inima plină de amărăciune și cu vorbe rele pe buze.
Floarea fermecată își cânta clinchetul ei delicat, dar fata nu era atentă la nimic afară de gândurile ei triste. Și cum stătea așa, o
voce subțirică îi șopti în ureche:
- Micuță Annie, ia aminte la toate relele pe care le strângi în inimă. O să le-mbrac pe toate în chipuri potrivite ca să vezi ce
puteri mari pot avea dacă nu le alungi din sufletul tău pentru totdeauna.
Și Annie văzu, cu frică și cu mirare, că vorbele ei mânioase se preschimbau în chipuri urâte și întunecate, așa ca greșelile sau
relele de unde se iscaseră. Unele aveau fețe răutăcioase și ochi aprinși și sfredelitori; astea erau duhurile Mâniei. Altele, cu
înfățișări mohorâte și lacome, păreau să înhațe tot ce era prin preajmă, iar Annie văzu că, deși adunau cât mai mult cu putință,
păreau că n-au niciodată destul; și știa că astea erau chipurile Zgârceniei. Duhurile Trufiei erau și ele acolo și își desfășurau
straiele cenușii pe lângă trupuri dând cu tifla lucrurilor și chipurilor din jur. Și Annie văzu multe alte duhuri ce izvorau din inima ei și
se întrupau în tot soiul de forme dinaintea ochilor.
Când le văzu pentru prima oară, duhurile erau mici și slabe; dar cum se uita așa la ele, păreau că cresc și prind tot mai
multă forță și fiecare din ele avea o putere stranie asupra ei. Fata nu le putea alunga și ele se făceau tot mai puternice, mai
întunecate și mai urâte privirii. Păreau că aruncă umbre negre peste tot prin jur, că întunecă soarele, că vatămă florile, că alungă
toată strălucirea și frumusețea lucrurilor. Annie văzu că în jurul ei se înălța un zid mare și negru ce o ținea departe de tot ce iubea.
N-avea curaj să se miște sau să vorbească dar, cuprinsă de o frică ciudată ce pusese stăpânire pe inima ei, ședea așa și privea
formele cele întunecate ce roiau pe lângă ea.
Și zidul de umbră se înălță tot mai sus, florile de lângă ea muriră încet-încet, iar lumina soarelui se stinse ușor. Toate
plăcerile și luminile dispărură iar Annie rămase singură în spatele zidului de negură. Atunci duhurile se adunară în jurul fetei,
șoptindu-i vorbe ciudate în urechi, poruncindu-i să le dea ascultare, că doar de bună voie le dăruise ea inima ei să-și facă acolo
sălaș și se înrobise lor pentru totdeauna. Apoi Annie nu mai auzi nimic și, ghemuindu-se printre florile uscate, plânse lacrimi amare
și triste, căci își pierduse libertatea și bucuria vieții. Dar iată că prin negură licări o luminiță slabă și plăpândă și copila văzu că la
piept ținea floarea fermecată, pe frunzele căreia luceau acum lacrimile ei. Lumina se făcu tot mai limpede și mai strălucitoare, iar
duhurile începură să se întoarcă spre zidul de umbră și să lase copila în pace. Lumina și parfumul florii păreau s-o umple pe Annie
de puteri noi, iar ea, sărutând floarea de la piept, se ridică și spuse: „Draga mea floare, ajută-mă și călăuzește-mă și cu bucurie voi
da ascultare glasului clopoțelului tău fermecat.”
Apoi, în vis, fata simți cât de tare încercau duhurile s-o amăgească și s-o tulbure iar și cum, de n-ar fi fost floarea, ar fi tras-o înapoi
și ar fi întunecat și învăluit în negură toate lucrurile, așa ca mai înainte. Annie se luptă din toate puterile și vărsă multe lacrimi, dar,
cu fiecare luptă, floarea cea vrăjită strălucea tot mai tare, iar parfumul ei devenea tot mai înmiresmat. Duhurile slăbeau din ce în ce
și lujeri verzi și plini de flori începură să urce pe zidul cel negru și să-l acopere; și peste tot pe unde creșteau frunze și se
deschideau flori, zidul de negură slăbea și se destrăma. Iar Annie se strădui din răsputeri și speră, până ce toate duhurile rele
zburară unul câte unul, iar în locul lor se adunară chipuri luminoase cu ochi blânzi și zâmbete largi care spuneau vorbe dulci și-i
aduceau bucurie și putere în suflet, astfel încât nimic rău nu îndrăznea să mai pătrundă acolo. Și în vreme ce zidul de negură
dispărea și ghirlande de flori parfumate creșteau în loc, Annie ajunse iar în lumea cea plăcută și veselă, cu darul ei ce nu mai
atârna palid și ofilit, ci lucind ca o stea la piept.
Atunci vocea subțirică vorbi din nou în urechea adormită a fetei: „Năravurile și pornirile rele pe care le-ai văzut sunt în inima
ta; fii cu băgare de seamă căci acum ele sunt mici și slăbite și dacă le lași, îți vor înnegura toată viața și vor alunga orice urmă de
iubire și fericire pe veci. Ține bine minte lecția primită în vis, copilă dragă, și lasă duhurile luminii să-și facă sălaș în inima ta.”
Și, cu glasul acesta răsunându-i în urechi, mica Annie se trezi și văzu că nu fusese decât un vis; însă el nu trecu așa cum
trec alte vise; și cum ședea așa singură, scăldată în lumina trandafirie a dimineții și privind pădurea ce se trezea la viață, își aduse
aminte de chipurile ciudate pe care le văzuse și, uitându-se în jos la floarea de la piept, își promise în sinea ei că se va strădui din
răsputeri, așa cum s-a străduit în vis, să aducă lumină și frumusețe pe frunzele pălite, prin ceea ce îi ceruse zâna, adică prin 
răbdare și blândețe. Și pe când se gândea astfel, floarea își ridică potirul plecat și, uitându-se către fața luminoasă aplecată spre
ea, păru că răspunde gândului nerostit al fetei prin parfumul ei și că îi dă puteri pentru ce avea să se-ntâmple.
Pădurea prinse viață, păsările își dădură bună-dimineața prin viersul lor, iar frunzele și florile se întoarseră către soare să îl
salute, căci el răsărise deja și zâmbea lumii din jur. Și pe sub ramurile pădurii și pe pajiștile înrourate o porni mica Annie spre casă,
mai cuminte și mai înțeleaptă după visul avut.
Curând florile toamnei se duseră, frunze galbene zăceau foșnind pe pământ, vânturi aspre fluierau prin copacii goi și iarna
albă și rece se așternu ușor peste toate. Și totuși, deși toate păreau mohorâte și triste, la pieptul lui Annie floarea fermecată se
făcea tot mai frumoasă cu fiecare zi. Amintirea visului din pădure nu dispăruse și, străduindu-se din toate puterile, fata își ținu
promisiunea neîntinată. Acum doar rareori clopoțelul florii îi suna în urechi și tot rareori înceta parfumul ei să plutească în jur sau
lumina cea vrăjită să strălucească la piept.
Și în timpul geroasei ierni mica Annie era ca o rază de soare în casă, tot mai iubitoare în fiece zi și tot mai mulțumită cu sine.
Se simțea ispitită adesea să greșească, dar, amintindu-și visul, lua aminte numai la clinchetul fermecat, iar gândul necurat
dispărea, lăsând duhurile zâmbitoare ale blândeții și iubirii să se cuibărească în inimă, și totul era înecat în lumină din nou.
Copila era, așadar, tot mai cuminte și mai voioasă, iar floarea se făcea tot mai frumoasă și mai parfumată, până când
primăvara se așternu zâmbitoare peste pământ și trezi florile, dezgheță și eliberă pâraiele și readuse în aer păsările. În fiecare zi
stătea acum copila printre flori și aștepta să vină iar buna zână, să îi poată mulțumi pentru darul fermecat pe care i-l făcuse.
În cele din urmă, într-o bună zi, pe când Annie stătea într-un cotlon însorit unde înfloreau cele mai mândre flori, obosită de
atâta privit în zare în așteptarea micii făpturi, se aplecă cu dragoste spre floricica de la piept să o privească. Și când se uită,
petalele se dădură în lături, și ridicându-se din cupa înmiresmată, apăru chipul zâmbitor al zânei căreia fata îi dusese așa de tare
dorul.
- Dragă Annie, nu mă mai căuta! Sunt aici, la pieptul tău pentru că ai învățat să-mi prețuiești darul, iar floarea și-a împlinit
menirea, spuse zâna, privind către fața luminoasă și fericită a copilei și înconjurându-i gâtul cu brațele mici într-o îmbrățișare caldă.
Ți-am adus un alt dar de pe Tărâmul Zânelor, drept răsplată, draga mea copilă, adăugă zâna, după ce Annie îi arătă toată 
mulțumirea și recunoștința. Și, atingând fetița cu bagheta ei sclipitoare, zâna îi porunci să privească și să asculte cu luare aminte.
Deodată lumea se preschimbă; văzduhul se umplu de sunete dulci și ciudate și pretutindeni apărură plutind chipuri frumoase. În
toate florile stăteau zâne mici ce zâmbeau și cântau vesel în timp ce se legănau printre frunze. Pe fiecare adiere pluteau duhuri
străvezii și strălucitoare; unele îi atingeau ușor obrazul cu respirația lor răcoroasă și îi fluturau părul în toate părțile, iar altele făceau
să sune potirele florilor și foșneau plăcut printre frunze. În fântânița unde apa dansa și sclipea în soare, Annie vedea în fiecare
strop duhuri mititele și vesele care pluteau și se bălăceau în undele limpezi și reci și cântau cu bucurie asemenea florilor pe care
aruncau o rouă lucitoare. Copacii înalți, cu ramurile foșnind în vânt, cântau o melodie lină și feerică, în vreme ce iarba unduioasă se
umpluse de glăscioare pe care Annie nu le mai auzise în viața ei. Fluturii îi susurau povești minunate în urechi și păsările îi cântau
melodii vesele în triluri dulci și neînțelese. Pământul și văzduhul păreau învăluite într-o muzică și o frumusețe la care copila nici
măcar nu visase.
- Spune-mi, dragă zână, ce înseamnă toate astea? E și ăsta vreun vis sau este pământul cu adevărat așa de frumos?, strigă
fata uitându-se cu o bucurie mirată la zâna cuibărită în floarea de la piept.
- E aievea, copilă dragă, răspunse zâna. Și puțini muritori primesc de la noi un asemenea dar. Ceea ce îți pare ție acum așa
de plin de muzică și lumină, nu e decât o zi plăcută de vară pentru alții; ei nu vor cunoaște niciodată graiul fluturilor, al florilor sau al
păsărilor, ei sunt orbi la tot ceea ce vezi tu prin puterea pe care ți-am dat-o. Minunile astea sunt de-acum prietenii tăi de joacă și ei
te vor învăța multe lucruri frumoase și îți vor dărui o sumedenie de clipe încântătoare. Uite, grădina unde ședeai odată vărsând
lacrimi amare și triste e acum luminată de fericirea ta și plină de prieteni dragi izvorâți din gândurile și sentimentele tale calde. Uite
așa arată vara în casa unui copil cuminte și voios, la pieptul căruia floarea fermecată nu va păli niciodată. Și acum, dragă Annie, eu
trebuie să plec; dar în fiecare primăvară, odată cu cele mai timpurii flori, voi trece iar pe la tine să-ți aduc un dar magic. Păzește cu
strășnicie floarea fermecată, ca să o găsesc frumoasă și strălucitoare și data viitoare când voi veni.
Și apoi, luându-și rămas bun, zână își luă zborul în sus, prin văzduhul însorit, zâmbindu-i fetiței, până ce dispăru în norii albi
și pufoși, iar mica Annie rămase singură în grădina ei vrăjită, unde totul strălucea în lumină și era învelit în parfumul florii fermecate.

Demult, demult de tot, pe când lumea era la început, pe pământ nu erau deloc margarete. Ghioceii înfloreau de sub petice
de zăpadă, brândușele își deschideau potirele galbene sau viorii pe pajiști însorite, toporașii priveau rușinoși din iarbă, iar narcisele
își plecau căpșoarele sidefii peste pâraiele șopotitoare. Dar micile margarete nu erau nicăieri.
Primăvara, în acele zile demult apuse, când soarele strălucea cald și suflau adieri parfumate, iar copacii își desfășurau
preafrumoasele lor veșminte verzi, din fiecare trunchi se uita pe furiș, cu chip zâmbitor, o nimfă-fecioară. Acolo dormiseră ele cât
ținuse iarna cea rece. Și toate nimfele aveau râsul precum foșnetul frunzelor și ieșeau din copaci numai în vârful picioarelor. Apoi
se luau de mână și fugeau pe o pajiște unde ciobănașii își păzeau oile. Și dansau nimfele cu ciobănașii în iarba presărată cu flori.
Dar margarete nu erau nicăieri.
Dar iată că într-o primăvară nimfele-fecioare se duseră iar să danseze cu ciobănașii pe pajiște. Își târau mantiile lor verzi pe
pământ, își aruncau brațele subțiri în aer și-și fluturau ghirlandele de frunze de stejar împletite în păr. Dar cea mai frumoasă și mai
grațioasă dintre toate era mândra Bellis. Mantia ei lungă era albă și în păr avea prinsă o coroniță de brândușe galbene. Era așa de
pură și de albă, așa de gingașă și de fermecătoare, că toți ciobănașii voiau să danseze cu ea. Dar ea nu-l voia decât pe unul singur
– un flăcău cu bujori în obraji. Așa de sprinten, săltăreț și vioi era flăcăul ăsta, că nimfa dansă toată ziua cu el.
Se întâmplă ca Vertumnus, păzitorul tuturor livezilor din lume pe vremea aceea, să audă râsul nimfelor și ciobănașilor; așa
că își lăsă livezile cu flori rozalii și veni grabnic pe pajiște. Văzu nimfele dansând cu ciobănașii și vru și el să danseze. Dar nu o
voia decât pe frumoasa Bellis. Ciobănașul ei, însă, nu voia să o dea. Când frumoasa Bellis văzu ochii aprinși ai lui Vertumnus, se
temu pentru viața ciobănașului ei. Palidă și zâmbitoare, se dădu înapoi și se duse mai departe în iarbă. Atunci părul i se
preschimbă în petale alburii iar coronița din păr se făcu un bănuț galben; mâinile îi deveniră frunze verzi și se tupilă cu totul în
iarbă, mică margaretă.
Și uite că de atunci, în iarba înaltă, după ce brândușele și narcisele pălesc, frumoasa Bellis, mica margaretă, înflorește
modestă și plină de gingășie.
O LEGENDĂ A FLORILOR
Demult, demult de tot, măritul spirit Byamee părăsi pământul și plecă să viețuiască în depărtatul tărâm al odihnei, care se
afla dincolo de piscurile muntelui Oobi-Oobi. Pământul deveni mohorât și trist după plecarea lui, căci florile, care împodobiseră
dealurile și pajiștile cu strălucirea lor, încetară să se mai deschidă. Și dacă nu mai existau flori, nici albinele nu mai făceau miere
pentru copiii pământenilor. În toată lumea mai erau numai trei copaci în care sălășluiau și trudeau albine; dar nimeni nu se apropia
de copacii aceștia sacri, căci ei îi aparțineau lui Byamee. Copiii plângeau după miere, iar mamele lor porneau prin pădure cu coșuri
în căutarea minunatei și dulcii licori. Dar mereu se întorceau cu mâna goală spunând:
- Nicăieri nu e miere. Doar în copacii cei sacri. Dar de copacii lui Byamee nu ne atingem.
Această purtare supusă îl mulțumi pe Marele Spirit foarte tare, așa că spuse: „Le voi trimite copiilor o licoare la fel de dulce ca
mierea la care râvnesc. Ea va curge din eucaliptul coolabah1
.”
Nu mult după aceea, pete albe și dulci fură văzute pe frunzele lucioase ale acelor copaci, iar pe ramurile și trunchiurile lor se
scurse o sevă dulce care se prefăcu în zahăr. Copiii se bucurară nespus și toată lumea îi fu recunoscătoare lui Byamee pentru
darul făcut. Și totuși, oamenii nu erau pe deplin mulțumiți, căci ei voiau să vadă pajiștile și dealurile pline de flori. Și așa de mare le
era dorul, că, în cele din urmă, Sfatul Înțelepților hotărî:
- Vom merge până pe tărâmul lui Byamee și-i vom cere să ne dea strălucirea florilor înapoi.
Hotărârea fu însă luată în mare taină. Înțelepții porniră așadar și merseră cale lungă până ajunseră la poalele muntelui Oobi-Oobi,
care avea vârful acoperit de nori. Hoinăriră mult pe stâncile de la poale, întrebându-se cum să urce până pe creste pe piatra
abruptă și, într-un târziu, dădură de o mică treaptă ascunsă în stâncă și apoi de încă una și de încă una. Uitându-se în sus, văzură
un șir nesfârșit de trepte ce se pierdea și el în nori. Hotărâră să urce; dar după o zi de mers piscul părea încă departe. Mai văzură

1 Eucalyptus viminalis – specie de eucalypt care produce o substanță zaharoasă, comestibilă, numită mană.
că urcau în spirală, înconjurând muntele. Abia după patru zile ajunseră la vârf. Găsiră acolo o fântâniță de marmură din care
țâșnea un izvor cu apă cristalină și dulce, din care înțelepții băură cu poftă. Drumul îi sleise de puteri, dar apa cea limpede îi
readuse la viață. Ceva mai încolo văzură apoi un cerc făcut din pietre puse una peste alta. Intrară în mijlocul acelui cerc și auziră
un glas ce venea, pesemne, de la un sol al Marelui Spirit Byamee:
- Ce vânt îi aduce pe înțelepții pământului în sălașul lui Byamee?
- De când măritul Byamee a plecat, nicio floare nu s-a mai deschis pe meleagurile noastre, răspunseră oamenii. Am venit să-l
rugăm să ne dea florile înapoi căci pământul e tare mohorât fără veselia culorilor.
Apoi glasul zise din nou:
- Duhuri ale muntelui, ridicați-i pe acești înțelepți la sălașul lui Byamee, acolo unde florile gingașe înfloresc veșnic. Înțelepților,
luați din florile astea atâtea câte puteți duce și după ce le adunați, duhurile vă vor purta înapoi în cercul de pietre de pe piscul
muntelui. De acolo să vă întoarceți cât mai grabnic pe meleagurile voastre.
Când glasul se opri, înțelepții se pomeniră luați pe sus și purtați printr-o deschizătură a cerului și apoi așezați pe un tărâm de o
frumusețe fără seamăn. Peste tot erau flori minunate de culori neînchipuite ce se înșirau ca o mulțime de curcubee prin iarbă. 
Înțelepții rămaseră muți de uimire la vederea fermecătoarei priveliști și plânseră de bucurie. Dar, amintindu-și pentru ce veniseră
până aici, se aplecară și adunară în mare grabă câte flori putură să țină cu mâinile. Duhurile veniră apoi și îi purtară din nou până la
cercul de piatră de pe vârful muntelui. Acolo auziră iar glasul acela care le spuse:
- Să le ziceți oamenilor atunci când le duceți aceste flori că de acum înainte pământul nu va mai fi niciodată gol și mohorât.
Vânturile vă vor aduce tot anul flori de un fel sau altul, iar vântul de la răsărit va aduce o mulțime de flori îndeosebi în copaci și
tufișuri. În iarbă, pe pajiști și pe coama dealurilor florile vor crește atât de multe cum n-ați mai văzut. Iar când vântul nu va sufla și
vor veni ploile, albinele vor face miere doar pentru ele. Atunci dulcea licoare va curge iar din copaci și va ține loc de miere până ce
vânturile de răsărit vor goni ploile și vor deschide florile în calea albinelor. Și iar va fi miere din belșug. Acum grăbiți-vă și duceți
această făgăduială și florile preafrumoase semenilor voștri.
Glasul se stinse și înțelepții, ducând cu ei florile nemuritoare, o porniră înapoi spre casă. Merseră iar pe treptele de piatră
săpate de duhurile muntelui, merseră peste pajiști și peste coame de deal și ajunseră în cele din urmă pe meleagurile lor. Oamenii
se adunară în jurul lor uitându-se uimiți la frumoasele flori. Aerul se umpluse de miresme îmbietoare, iar florile erau la fel de
proaspete ca atunci când înțelepții le culeseseră de pe tărâmul lui Byamee. Și după ce înțelepții le arătară semenilor florile și le
povestiră despre făgăduiala făcută de Byamee, răspândiră prețiosul dar în toate zările. Unele flori căzură pe copaci, altele pe
pajiști, altele pe coame de deal sau de munte și de atunci pământul e binecuvântat cu darul florilor.

O viță plăpândă răsări dintre firele de iarbă. Încercă să se înalțe, dar firele de iarbă, deși se opintiră din răsputeri, nu putură
să o ridice, iar ea căzu pe pământul moale și cald.
- Aș vrea atât de tare să văd cerul, zise vița într-o bună zi, când iarba crescuse așa de mare că abia dacă mai zărea ceva
printre firele late.
- Încearcă să te cațeri pe trunchiul meu, spuse un stejar bătrân ce creștea deasupra ei.
- Aș face-o bucuroasă dacă m-ai lăsa, zise vița cea plăpândă.
- Dacă te las? Sigur că te las, râse bătrânul copac. De ce sunt eu mare și puternic dacă nu-i ajut pe cei mai mici decât mine?
Și vița începu să se cațere. Și ce lesne era să se agațe de scoarța bătrână și aspră! Și cât de repede creștea! Și înainte de
jumătatea verii ajunse sus, între ramuri. Acum vedea cerul. Și el părea foarte, foarte aproape. Și erau păsări în copac și sute de
gâze lucitoare. Vița dansa în bătaia vântului și era cea mai fericită plantă din tot ținutul.
Încet, încet veni toamna, iar bătrânul copac începu să-și lepede frunzele. Vița începu și ea să-și schimbe culoarea. Acum
era roșie și strălucitoare ca focul. Dar într-o zi veniră doi tăietori de lemne cu topoarele pe umeri.
- Vezi vița aia roșie?, spuse primul dintre ei. Tocmai mă pregăteam să tai copacul, dar păcat de frumusețea aia de viță. Și
pădurarii plecară.
Vița dansă și râse de bucurie. Și copacul cel bătrân era fericit.
- Tu m-ai salvat, zise el.
- Ba nu, tu m-ai salvat pe mine cu ceva luni în urmă, spuse vița.
Vița și stejarul sunt încă în pădure și trăiesc fericiți împreună; dar nu se pot nicicum înțelege cine pe cine a salvat.

Era odată un om care avea o fată pe care o iubea ca pe lumina ochilor. Într-o bună zi, pe când se îndrepta spre casă de la
treburile lui, văzu o garoafă roz ce creștea la marginea drumului. O culese și o duse acasă la fiică-sa. Aceasta spuse că așa
garoafă frumoasă ea nu mai văzuse și o puse cu mare grijă într-un pahar cu apă.
În seara aceea, pe când ținea garoafa în mână admirând-o, din nebăgare de seamă, o
scăpă în flacăra lumânării. Garoafa cea roz începu de îndată să ardă. Și pe loc apăru în fața fetei
un tânăr chipeș care grăi cu tristețe în glas:
- De ce nu vrei să-mi vorbești? Uite, acum va trebui să mă cauți printre stânci și pietre peste
tot prin lume. Și tânărul dispăru la fel de misterios precum apăruse.
Biata fată nu mai văzuse un tânăr așa de frumos în toată viața ei. Acum visa la el în fiecare
noapte, iar cuvintele lui îi tot sunau în urechi: „Acum va trebui să mă cauți printre stânci și pietre
peste tot prin lume.”
Și fata nu găsi nimic mai bun de făcut decât să plece în căutarea flăcăului misterios. Acasă
nu-și mai găsea tihna. Așa că se puse pe mers și merse și merse... Într-un sfârșit ajunse la o stână
înaltă pe malul unui râu și, pentru că era ruptă de oboseală, se așeză să se odihnească. Era foarte
cald și fata începu să plângă de atâta dogoare și oboseală. Deodată, stânca se deschise și din ea apăru tânărul cel chipeș.
- De ce plângi? întrebă el cu blândețe.
Fata se sperie așa de tare că nu scoase un cuvânt; doar plânse în continuare. Tânărul mai spuse:
- Uite colo în pădure o să vezi o casă mare cu ogoare întinse pe lângă ea. Mergi la casa aceea și cere să fii slujnică. Te vor
primi bucuroși. Și spunând acestea, flăcăul se făcu nevăzut în stâncă.
Fata îi urmă fără preget sfatul și găsi casa după cum îi spusese el. Stăpâna acelei case era tocmai în căutarea unei slujnice
și o tocmi pe fată de îndată. Nu trecu mult până ce fata deveni favorită între celelalte servitoare ale casei, căci avea un chip frumos,
era harnică și plăcută la purtare. Ceilalți o pizmuiau și puseră la cale să-i facă necazuri. Merseră la stăpână și îi ziseră:
- Stăpână, știi ce a spus noua servitoare în bucătărie?
Stăpâna se arătă foarte curioasă să afle.
- A spus că nu vă trebuie atâția slujitori, și că ea singură ar putea să spele toate rufele într-o singură zi.
Stăpâna o chemă pe fată la ea și o întrebă dacă era adevărat. Fata începu să plângă și spuse că totul era o minciună și că
ea nu zisese niciodată așa ceva; dar ceilalți servitori jurară că o auziseră cu toții, iar stăpâna îi porunci atunci să spele toate rufele
într-o singură zi, așa cum se lăudase.
Fata merse la râu cu rufele și se așeză plângând pe o stâncă. Deodată, stânca se deschise și flăcăul cel chipeș apăru
dinaintea ei.
- De ce plângi?, întrebă el.
Fata fu așa de uimită că nu scoase un cuvânt și se puse pe un plâns și mai amarnic. Tânărul zise:
- Nu te necăji cu rufele. Lasă-le aici pe mal și roagă păsările să vină să te ajute.
Fata se uită la el plină de uimire, dar tânărul dispăru și de data asta în stâncă. Făcu atunci așa cum o povățuise el și strigă:
- Hei, păsări din lumea largă, veniți și ajutați-mă!
Și pe loc nenumărate păsări se adunară în stoluri pe malul râului. Erau și păsări mari, și păsări mici și mijlocii. Erau și păsări negre,
și maro, și albastre, și roșii, și galbene. Fata nici nu știuse că existau așa de multe păsări pe fața pământului. Și ele apucară
hainele murdare cu ciocurile și le tăvăliră în apele râului. Nu după mult timp toate rufele se făcură albe și curate. La amiază, hainele
erau deja uscate și gata să fie duse înapoi acasă. Stăpâna și ceilalți servitori nu-și crezură ochilor când văzură că treaba fusese
împlinită. Și stăpâna o îndrăgi și mai mult pe tânăra slujnică și se lăudă la toată lumea că avea în casa ei o adevărată comoară.
Ceilalți servitori o pizmuiră însă și mai mult și se gândeau acum la o altă caznă. Se întâmplase ca stăpâna să aibă un singur
fiu care plecase mai demult de acasă și nu se mai întorsese. Fusese vrăjit pesemne și biata mamă plânsese până ce aproape că
își pierduse vederea. Servitorii se duseră de astă dată la ea și îi ziseră că slujnica cea tânără se lăudase că știa ea de unde să
aducă niște apă care putea tămădui orice boală de ochi. Desigur că sărmana fată nu spusese niciodată așa o grozăvie, dar toți se
jurară că era adevărat, iar stăpâna se înfurie la auzul veștii că slujnica știa de apa asta tămăduitoare pe care ea nu o avea. Așa că
fata fu trimisă să aducă apa ce avea să vindece ochii plânși și bolnavi ai stăpânei.
Merse fata iar la râu și se așeză pe stâncă, plângând de i se rupea sufletul. Vezi bine că nu știa nimic despre vreo apă cu
puteri tămăduitoare. Și dintr-odată stânca se deschise și flăcăul cel chipeș păși la lumina zilei.
- Ce s-a întâmplat? De ce plângi?, întrebă el.
Și cum nu primi nici un răspuns, spuse:
- Știu cum poți face rost de apa care să vindece ochii mamei mele. Adu o ulcică și stai pe malul râului. Apoi cheamă păsările
de pe tot întinsul pământului să vină să plângă împreună cu tine. Și spunând acestea, tânărul dispăru.
Fata îi urmă povața și se așeză pe mal cu o ulcică în mâini. Strigă păsările să vină să plângă împreună cu ea și pe dată ele
veniră. Și fiecare pasăre vărsă o lacrimă în ulcică, până aceasta se umplu. Ultima pasăre lăsă un fulgușor alb în cupă.
Apoi, când fata spălă ochii stăpânei cu apa aceea, folosindu-se de fulgul cel alb, femeia începu să vadă mai bine. Și curând
începu să vadă mai bine ca oricând și o îndrăgi pe tânăra slujnică și mai mult. Servitorii cei pizmași uneltiră iar împotriva fetei. De
astă dată îi spuseră stăpânei că fata se lăudase că știa cum să rupă vraja ce îl ține legat pe fiul demult plecat. Acum stăpâna
căpătase așa o încredere mare în slujnica ei, încât credea că aceasta putea face orice. Iar când fata spuse că ea nu se lăudase
niciodată în felul acela, stăpâna îi zise:
- N-are importanță! Du-te și încearcă! Și dacă se întâmplă să reușești să rupi vraja fiului meu și să mi-l aduci înapoi, i te dau
de nevastă.
Tânăra slujnică se duse iar la stânca de lângă râu și plânse amarnic. Flăcăul ieși din stâncă și de astă dată și o întrebă de
ce plânge. Și pentru că fata nu răspunse, el zise:
- Știu că maică-mea te-a trimis să rupi vraja. Adună toate fetele din oraș, și pe cele sărace și pe cele bogate și vino cu ele
aici lângă stâncă. Și fiecare să aibă o lumânare aprinsă în mână. Și vezi să nu se stingă nici o flacără! Să vedem dacă așa se va
rupe vraja!
Și când dispăru și de data asta, tânăra se duse în goana mare să aducă toate fetele din oraș, sărace și bogate deopotrivă.
Și ce frumos veneau ele împreună pe mal către stâncă, fiecare cu o lumânare aprinsă în mână! Tânăra slujnică era ultima din șirul
de fete și taman când ajunse lângă stâncă, vântul îi stinse lumânarea.
- Vai, mie! Ce mă fac? Mi s-a stins lumânarea!, se tângui ea. Și văzu că flăcăul cel chipeș își făcuse deja apariția.
- În sfârșit, ai vorbit lângă mine! strigă el. Acum vraja s-a rupt!
- Și eu care am crezut că am stricat totul când mi s-a stins lumânarea! exclamă fata.
Și flăcăul îi povesti cum fusese vrăjit într-o zi pe când se plimba pe câmp. Fusese preschimbat într-o garoafă și i se spusese că
vraja va putea fi ruptă numai atunci când cel ce va arde garoafa, va vorbi în prezența lui.
- N-ai rostit niciun cuvânt când m-ai ars, îi spuse el cu reproș. A trebuit să mă întorc în stânca din care răsărise garoafa și
începusem să cred că nu voi putea să te fac să vorbești vreodată. Nu făceai decât să plângi!
Mama flăcăului fu cuprinsă de o fericire fără seamăn când își văzu iarăși fiul, teafăr și nevătămat. Își sărută slujnica pe
amândoi obrajii.
- Îmi vei fi ca o fiică acum, spuse ea. Nunta se va face de îndată!
Și tânăra se vindecă pe deplin de obiceiul de a plânge și bine făcu pentru că, după toată întârzierea cu care se rupsese
vraja, bărbatul ei n-ar mai fi putut îndura o femeie plângăcioasă.
DE CE ÎNFLORESC FLORILE DOAR JUMĂTATE DIN AN
Toamna asta Mama Natură era până peste cap de ocupată. Recoltele fuseseră bogate și avusese atâtea fructe cât nici nu
visase vreodată. Zeul-Soare și Zeul-Ploaie fuseseră tare buni și tot pământul era fericit. „Draga de ea”, gândi Mama Natură privind
peste câmpuri la frumoasa Regină a Florilor; „n-a fost niciodată atât de frumoasă cum este în toamna asta! Dar, vai, să merg iute în
lanurile de grâu și prin livezi!”
- Rămas bun, copilă dragă! Ai grijă de tine și nu-l lăsa pe Craiul-Ger să te ducă cu el!
Mica Regină a Florilor promise să ia seama și dansă fericită în lumină.
- Nu te teme, dragă mamă, râse ea, întorcându-și fața drăgălașă spre cer; norișorii mă vor păzi.
Dar mica Regină a Florilor, ca orice copil, nu știa ce pericole pot pândi la tot pasul; și, uite-așa, când se auzi un huruit ușor
pe sub pământ, ea continuă să se miște voioasă de colo-colo. „Copiii pământului se tem când aud acel zgomot”, își spuse ea, „dar
eu știu că e doar huruitul roților carului lui Pluto.”
Pluto era regele tărâmului subpământean. Avea grijă de sol să rămână moale și gras. Dar Mama Natură n-ar fi crezut
niciodată că acest bătrân rege o pizmuia pentru frumoasa și mica Regină a Florilor și aștepta momentul prielnic să vină să o fure.
- Mama Natură e foarte ocupată azi, îi șoptiră vânturile mohorâtului rege, pe când treceau măturând pământul.
- Și unde e mica Regină a Florilor?, întrebă repede Pluto.
- Oo, se joacă pe câmpuri și pe răzor, răspunse vântul.
Un zâmbet trecu peste fața lui Pluto și într-o clipită sări în car. Așa că mica Regină a Florilor auzi iar roțile carului. Deodată îi
ajunseră la urechi trosnituri de rădăcini frânte; apoi apăru și Pluto cu carul lui cu tot. Abia putea să îndure lumina soarelui, care
aproape că-l orbea. Și, înșfăcând-o pe mica regină, dispăru iar în întunericul lumii subpământene.
Biata Mama Natură! Cum mai plânse când se întoarse și nu-și găsi copila! Cât de mohorât arăta tot pământul! Chiar și
copacii își lepădau frunzele de durere! Zile și săptămâni rătăci biata mamă încoace și-ncolo pe pământul gol și rece.
- Vino înapoi, vino înapoi, copila mea!, gemea ea, iar copiii pământului, auzind-o, credeau că
e vântul.
Lacurile își acoperiră chipurile cu un văl greu și apele lor încetară să mai strălucească. Chiar
și râurile și pârâurile încremeniră de durere.
Dar iată că într-o zi Regina Florilor se întoarse. Mama Natură se bucură, lacurile zâmbiră și
străluciră din nou. Pârâiașele începură să cânte și să danseze de bucurie și, timp de șase luni,
Regina Florilor se jucă iar în lumina soarelui. Dar într-o zi își plecă gingașul ei cap și se întristă.
Culorile luminoase ale rochiei pe care o purta se preschimbară în tonuri de maro și toată viața părea
că i se stinge de pe chipul fericit.
- Dragă mamă, șopti ea, a sosit timpul să merg iar în casa mea subpământeană. Să nu plângi
după mine! Regele Pluto e mohorât, după cum se știe, dar asta pentru că e tare singur acolo sub
pământ. E bun cu mine, iar eu chiar am nevoie de odihnă. Asta mă ține veșnic tânără; și în fiecare an
mă voi întoarce la tine, la fel de proaspătă cum am fost. Deci rămas bun, dragă mamă! La revedere,
soare drag, la revedere! Peste doar câteva luni voi veni din nou!

Ați vrea să știți de ce micuța floare de toporaș aruncă priviri așa de furișe de sub frunzele ei verzi și late și de ce se ascunde
cu așa mare modestie în păduri și pe sub tufele umbroase? Iată ce spune o veche legendă:
Cică era odată o preafrumoasă și modestă fecioară numită Ianthis. Ea era una dintre slujitoarele Dianei, Zeița cu Arc.
Adesea, Ianthis avea obiceiul să hoinărească prin pădure împreună cu suratele ei, Arethusa și Syrinx, și să culeagă flori și fructe.
Dar spre deosebire de acestea două care își purtau brațele descoperite pentru a-și putea folosi cu mai mare ușurință arcurile la
vânătoare, modesta Ianthis se înfășura într-un văl albastru închis și mâna o cireadă de vaci ce pășteau liniștite pe pajiștile
înmiresmate.
Se întâmplă ca într-o zi Apollo, Zeul Luminii și al Razelor de Aur, să privească din palatul lui din soare și să zărească ochii
minunați ai lui Ianthis ce se uitau timid în sus de sub vălul ei albastru. Îndată zbură zeul drept pe pajiște. Dar Ianthis îl văzu venind
și fugi rușinată.
- Diana, strigă ea plângând, unde să mă ascund de Apollo? Să fug între munți si să mă pitulez
acolo?
Diana îi răspunse liniștită:
- Dragă surioară, nu te duce între munți căci lui Apollo îi place să stea pe culmile lor și să
privească de acolo cerul. Mai bine ascunde-te într-un cotlon umbros, pentru că lui Apollo nu-i plac
locurile ferite.
Așa că Ianthis alergă în pădure și se ascunse într-un tufăriș lângă pârâu. Dar Apollo o găsi.
Dădu crengile în lături și, când îi văzu chipul îmbujorat de rușine uitându-se la el, își întinse brațele și
o înșfăcă să o ducă în palatul lui din soare. Dar Diana, care își iubea tare mult surata, îi atinse chipul
acoperit de vălul albastru și îl preschimbă într-o plăpândă și frumoasă floare de toporaș; trupul i se
cufundă printre pietre și frunze și deveni o plăntuță verde întinsă pe pământ.
Și din acea zi, spune legenda, Ianthis, floarea de toporaș, se ascunde pe malurile pâraielor și
pe sub tufișurile umbroase, aruncând priviri furișe și rușinoase de sub frunzele ei late și verzi.

Au fost odată un rege și o regină care în fiece zi spuneau cu mare mâhnire: „Dacă am avea și noi un copil”; dar se scurse
multă vreme și ei tot n-avură niciunul. Dar iată că odată, pe când regina se scălda, se întâmplă că o broască ieși pe malul apei și îi
zise:
- Dorința ta se va împlini; nu se va încheia anul și tu vei aduce pe lume o fetiță.
Vorbele broaștei se adeveriră. Regina născu o fetiță atâta de frumoasă, că regele nu-și mai încăpea în piele de bucurie și se apucă
să pregătească un mare ospăț. Își invită nu numai neamurile, prietenii și toți cunoscuții, ci chemă și zânele ca să o înzestreze pe
copilă cu daruri minunate. Și erau treisprezece zâne în tot regatul, dar cum regele nu avea decât douăsprezece tipsii de aur, una
din zâne trebui să rămână acasă.
Ospățul fu încântător, iar când se apropie de sfârșit, toate zânele se înfățișară înaintea fetiței cu daruri magice. Una îi dete
virtute, alta frumusețe, a treia bogății, și tot așa, tot ce și-ar fi putut dori mai bun și mai frumos din ce exista pe lume. După ce
unsprezece zâne se perindară prin fața micuței, se pomeniră toți că apare și zâna a treisprezecea. Voia răzbunare pentru că nu
fusese chemată la ospăț. Și, fără să dea ziua bună, sau fără măcar să arunce vreo privire celor de față, strigă cu voce tunătoare:
- Prințesa se va înțepa într-un fus când va împlini cincisprezece ani și va cădea moartă pe dată! Și, fără să mai rostească
alte cuvinte, le întoarse spatele și dispăru.
Toți oaspeții se cutremurară când auziră acestea, dar zâna cea de-a douăsprezecea, a cărei dorință nu fusese încă rostită,
păși în față. Nu putea desface blestemul, dar îl putea preschimba un pic, să nu fie atât de necruțător, așa că spuse:
- Fiica voastră nu va fi moartă cu adevărat, dar va cădea într-un somn adânc ce va dura o sută de ani.
Dornic să-și păzească draga copilă de marea nenorocire, regele porunci ca toate fusele din tot regatul să fie arse. Anii
trecură și toate cele ursite de zâne se împliniră. Prințesa crescu așa de frumoasă, de modestă, de bună și de înțeleaptă, că toți cei
ce o întâlneau nu puteau decât s-o îndrăgească. Se întâmplă însă ca tocmai în ziua când fata făcea cincisprezece ani, regele și 
regina să nu fie la palat, iar ea să fie singură acasă. Rătăci peste tot prin castel, uitându-se prin odăi și încăperi după pofta inimii,
până ajunse într-un turn vechi. Urcă pe o scară îngustă și răsucită până ce ajunse la o ușiță. O cheie ruginită era lăsată în broască
și când fata învârti cheia, ușa se deschise. Într-o cămăruță ședea o bătrână cu un fus, torcându-și de zor caierul.
- Ziua bună, mătușică!, zise prințesa. Ce faci acolo?
- Torc, spuse bătrâna, făcându-i semn din cap să se apropie.
- Ce e lucrușorul acela care se rotește așa de iute și de frumos?, întrebă prințesa. Și luă și ea fusul și încercă să toarcă. Dar
nici nu-l apucă bine, că blestemul se și împlini, iar ea se înțepă într-un deget. Și cum se înțepă, căzu pe patul ce se afla acolo și se
adânci într-un somn greu care cuprinse întregul castel.
Regele și regina, care tocmai se întorseseră și intraseră în marele hol al palatului, adormiră și ei pe loc, și toți curtenii odată
cu ei. Adormiră și caii în grajduri, și cânii în curte, și porumbeii pe acoperiș, și muștele pe pereți; da, chiar și focul ce licărea în vatră
se opri și adormi, iar friptura ce se rumenea deasupra se opri din sfârâit; bucătarul, care-și păruia ucenicul pentru nu știu ce
greșeală făcută, îl lăsă în pace și adormi. Și vântul încetă să mai bată, astfel că nici o frunzuliță din copacii din fața castelului nu se
mai mișca. În jurul castelului începu să crească un hățiș de trandafiri sălbatici; cu fiece an creștea tot mai înalt, până ce înconjură
palatul de tot, de nu se mai vedea nimic din el, nici măcar flamura de pe acoperiș.
În ținut se răspândise însă o legendă despre frumoasa adormită Trandafirița, căci așa se numea fiica regelui, și din când în
când câte un prinț se încumeta și încerca să-și croiască drum prin hățiș, ca să ajungă la castel. Dar în zadar încerca, pentru că
țepii, de parcă ar fi avut mâini, îl țineau țintuit locului și prințul rămânea acolo neputincios și fără scăpare și murind până la urmă o
nefericită moarte.
După mulți, mulți ani, un prinț veni iarăși în țara aceea și auzi un bătrân povestind despre castelul ascuns îndărătul hățișului
de trandafir sălbatic, unde dormea de o sută de ani o preafrumoasă fecioară numită Trandafirița și, odată cu ea, dormeau și regele,
și regina și toți curtenii. Și prințul știa de la bunicul său că mulți cavaleri trecuseră pe acolo și încercaseră să pătrundă printre spini,
dar rămăseseră prinși între țepoasele crengi și muriseră de o moarte grea. Atunci prințul spuse:- Nu mi-e teamă; sunt hotărât să
merg să o văd pe frumoasa Trandafirița.
Bătrânul cel bun făcu tot ce-i stătu în putere să-l împiedice pe prinț, dar prințul nu dădu ascultare. Mai ales că cei o sută de
ani aproape se scurseseră și urma să vină ziua când prințesa avea să se trezească. Când prințul se apropie, tufele de trandafir
sălbatic erau în floare, iar florile erau mari și frumoase și se dădeau la o parte din calea lui, lăsându-l să treacă nevătămat și apoi
închizându-se iar în urmă-i într-un hățiș de netrecut.
În curtea palatului, el văzu cai și câini adormiți, pe acoperiș ședeau porumbeii cu capetele sub aripi, înăuntru muștele
dormeau pe pereți și lângă tron zăceau adormiți regele și regina; în bucătărie era bucătarul, cu mâna ridicată de parcă era
gata-gata să-l pocnească pe ucenic, iar servitoarea stătea adormită, cu o găină neagră în poală, pe care urma să o jumulească.
Prințul merse mai departe și totul era așa de nemișcat, că-și putea auzi propria răsuflare. Ajunse și în turn și deschise ușa
cămăruței unde dormea Trandafirița. Și, cum stătea ea așa întinsă, arăta atât de frumoasă, că prințul nu-și putea lua ochii de la ea;
se aplecă, aşadar, și o sărută. Și cum o atinse, Trandafirița deschise ochii și îl privi dulce. Apoi coborâră amândoi în castel, iar
regele, regina și toți curtenii se treziră și se priviră uimiți. Caii din grajduri se ridicară și se scuturară, câinii săriră în picioare și
începură să dea din coadă, porumbeii de pe acoperiș își scoaseră capetele de sub aripi, se uitară de jur împrejur și își luară zborul
spre câmp, muștele de pe pereți începură iar să se miște, focul din bucătărie se reaprinse și își ridică flăcările ca să frigă
mâncarea, carnea începu să sfârâie, iar bucătarul îl pocni pe ucenic așa de tare peste urechi, că acesta zbieră din toți rărunchii, în
vreme ce servitoarea jumulea găina. Și apoi se făcu o nuntă de toată frumusețea între prinț și Trandafirița, care trăiră fericiți până la
adânci bătrâneți.

Vai, vai, cât de tristă este pricina pentru care mica cicoare albă stă așteptând răbdătoare la marginea drumului, iar în jurul ei
se unduie plăpândele flori de cicoare albastră uitându-se în toate părțile!
Odată, demult, mica cicoare albă era o prințesă frumoasă. Era foarte fericită căci fusese promisă unui prinț atât de chipeș,
cum nu se mai găsea altul în lume. Dar acesta era înfumurat și nestatornic și într-o bună zi o părăsi pe preafrumoasa prințesă fără
măcar să îi spună vreun cuvânt de adio; urcându-se deci pe cal, plecă din împărăție. Și când prințesa află și își dădu seama că
poate rămâne singură pe veci, se puse pe un plâns amarnic ce dură zile și nopți în șir.
Bujorii îi dispărură din obraji și se făcu tot mai albă și mai albă. Și stătea mereu în umbrarul din grădină, cu ochii în zare,
așteptându-l pe prinț să se întoarcă. Plânsul o slei de puteri, de abia se mai putea ține pe picioare.
- Vai mie, plângea ea, mai bine ar fi să mor! Dar dacă mor, nu-l voi mai vedea niciodată pe iubitul meu prinț.
- Vai, vai, se tânguiau domnițele de la curte. Mai bine ar fi să murim și noi odată cu tine! Dar dacă murim, nu te mai putem
veghea aici în grădină.
Și cum vorbeau așa, se și preschimbară cu totul! Frumoasa prințesă se făcu o mică cicoare albă ce așteaptă la marginea drumului,
iar domnițele deveniră flori de cicoare albastră, adunate în jurul ei și uitându-se în toate direcțiile.
Iată pricina cea tristă pentru care florile de cicoare albastră stau și acum de pază pe lângă prințesa lor
și privesc, în timp ce mica cicoare albă așteaptă răbdătoare să i se întoarcă iubitul."""
    words = nltk.word_tokenize(text)
    print(words)
    start = time.time()
    output = t.translate_words(words)
    end = time.time()

    print("1st translation:")
    print(output)
    print("Translated whole text in {} seconds".format(end - start))

    # start = time.time()
    # second_output = t.translate(output, source_lan='en', dest_lan='ro')
    # end = time.time()
    #
    # print("\n\n2nd translation:")
    # print(second_output)
    # print("Translated whole text in {} seconds".format(end - start))
    #
    # print(len(nltk.sent_tokenize(second_output)))
    # start = time.time()
    # for word in text.split(" "):
    #     t.translate(word)
    #
    # end = time.time()
    # print("Translated word by word in {} seconds".format(end - start))
