# Dokumentácia štvrtého zadania

Úlohou štvrtého zadania bola implementácia *modifikovaného problému hodujúcich divochov*. Podstata problému spočíva v prístupe k zdieľaným zdrojom algoritmu. Zdieľanými zdrojmi sú v tomto prípade hrniec, v ktorom je určité množstvo porcií.

### Problematika *hodujúcich divochov* s viacerými kuchármi

Problém nastáva, keď sa jednotlivé vlákna, v tomto prípade divosi a kuchári, snažia pristupovať k hrncu. Cieľom je zabezpečiť integritu tohto zdieľaného zdroju, tak aby bol prístupný len pre jednu entitu v danom čase. Taktiež je potrebné vymedzenie prístupu pre skupiny vlákien (kuchárov a divochov). Keď kuchári varia a doplňujú hrniec porciami gulášu zo zebry, žiaden divoch nebude mať k nemu prístup, až dokým kuchári nedovaria a hrniec nebude plný. Analogicky, kuchári začnú variť, až keď si divosi naložia poslednú porciu z hrnca.

### Dokumentácia kódu

Kód je napísaný v jazyku *python* vo verzii *3.10* a využíva knižnice *fei.ppds* na simulovanie procesu s niekoľkými vláknami, knižnicu *time*, z dôvodu použitia funkcie *sleep*. Funkcia *sleep* simuluje proces jedenia alebo varenia. <br>

Ako prvé som si zadefinoval potrebné synchronizačné prvky, globálne premenné a počítadlá.

##### Postup algoritmu

Beh Algoritmu je nasledovný. Vytvorí sa `N` počet vlákien pre divochov a kuchárov, ktoré začnú vykonávať ich príslušné procesy `def cook()` a `def savage()`.

###### Podrobný opis procesu divocha

Proces sa vykonáva vo `while` cykle. Podľa prvého bodu zadania majú divosi vždy začínať hodovanie spolu. Za týmto účelom som implementoval znovu použiteľnú bariéru, rovnakým spôsobom, ako bola zadefinovaná v ukážkových kódoch z cvičení.

```
.
.
shared.mutexCountSavages.lock()
shared.countSavages += 1
if shared.countSavages == NUM_SAVAGES:
   shared.turnstile_1_start.signal(NUM_SAVAGES)
   print(f'Savage {i} signals to eat. Count savages = {shared.countSavages} / {NUM_SAVAGES} \n')
else:
   print(f'Savage {i} is waiting. Count savages = {shared.countSavages} / {NUM_SAVAGES}')
shared.mutexCountSavages.unlock()
shared.turnstile_1_start.wait()
.
.
```

Divosi si postupne prenechávajú prístup k počítadlu `countSavages` a postupne ho svojím prechodom zvyšujú. Čakajú na riadku `shared.turnstile_1_start.wait()`. Posledný z nich zbehne do podmienky `if` a zasignalizuje zvyšku, že môžu začať hodovať. Keďže sa jedná o znovu použiteľnú bariéru, jej druhá časť sa nachádza na samom konci tohto procesu. Funguje na presne rovnakom princípe s tou zmenou, že namiesto `shared.countSavages += 1`, zvyšovania počítadla sa z neho uberá: `shared.countSavages -= 1`. Týmto spôsobom je zabezpečená znovu použiteľnosť tejto bariéry vyresetovaním počítadla.

V ďalšom kroku už nasleduje proces hodovania. Moja implementácia je nasledovná. Predtým, ako divoch môže pristúpiť k hrncu, musí najskôr vstúpiť do 'kuchyne'. Túto operáciu som simuloval na riadku `shared.mutex_enter_kitchen.lock()`. Do 'kuchyne' môže vstúpiť len jeden divoch v danom momente. Dôvodom tohto postupu bolo vymedzenie prístupu pre skupinu divochov a kuchárov. Pri prvej implementácii som narazil na problém, kedy sa divosi a kuchári striedali medzi sebou. Snažil som sa tento problém riešiť pomocou signalizácie, no neúspešne. V implementácii s kuchyňou môžem voľne vymedziť prístup pre jednu alebo druhú skupinu. Postup vysvetlím na nasledujúcom kóde.

```
        # Savage in the kitchen locks access to the pot
        shared.mutex_accessing_pot.lock()

        # Check for empty pot
        if shared.portions_left == 0:

            # Signal cook that pot is empty and unlock access to the pot
            shared.full_pot.signal(NUM_COOKS)
            shared.mutex_accessing_pot.unlock()

            # Savage waits in the kitchen until cooks are done
            print(f"Savage {i} signals cook that pot is empty and waits! \n")
            shared.empty_pot.wait()

            # Cooks are done, savage in the kitchen can take his portion
            shared.mutex_accessing_pot.lock()
            shared.portions_left -= 1
            shared.mutex_accessing_pot.unlock()
        else:
            shared.portions_left -= 1
            shared.mutex_accessing_pot.unlock()

# Another savage can enter chicken
shared.mutex_enter_kitchen.unlock()
```

Ako prvé po vstupe do kuchyne si divoch vymedzí prístup k hrncu. V podmienke skontroluje či je hrniec prázdny. Ak nie je, naberie si porciu, odomkne prístup k hrncu a mimo podmienky opustí kuchyňu. Ďalší môže vstúpiť do kuchyne. Ak zistí, že hrniec je prázdny, odomkne zámok (resp. odstúpi od hrnca) a na riadku `shared.full_pot.signal(NUM_COOKS)` zasignalizuje kuchárom, aby začali variť. Divoch potom čaká na signál od kuchárov, že naplnili hrniec na tomto riadku `shared.empty_pot.wait()`. Tým pádom divoch ostal v kuchyni, preto nemôže iný divoch vstúpiť a kuchári môžu v pokoji pristúpiť k hrncu a doložiť porcie. Divoch v kuchyni sa na nich pozerá a čaká na ich signál. Týmto spôsobom som vyriešil vymedzenie prístupu pre určité skupiny entít v tomto algoritme.

Následne po doplnení hrnca kuchári signalizujú divochovi v kuchyni, že hrniec je naplnený. Na posledných troch riadkoch `if` podmienky si divoch vymedzí prístup k hrncu, odoberie jednu porciu a odstúpi od hrnca a následne mimo podmienky odomkne prístup do kuchyne. Divoch sa následne naje, už mimo kuchyne, tento proces je simulovaný klasicky funkciou `sleep`.

Posledným krokom je už len druhá časť znovu použiteľnej bariéry, ktorú som opísal vyššie. Proces sa následne môže opakovať.

###### Podrobný opis procesu kuchára

Celý proces sa odohráva v cykle. Kuchári sa dajú v kontexte procesu divocha predstaviť ako nejaké entity, ktoré sa stále nachádzajú v kuchyni, no nepristupujú k hrncu, až dokým divoch nesignalizuje prázdny hrniec. Konkrétne čakajú na tomto semafore `shared.full_pot.wait()`. Po signalizácii jednotlivé vlákna vstúpia do ďalšieho cyklu, ktorý reprezentuje process varenia. Obdobne ako pri procese divocha, kuchár si pomocou zámku vymedzí prístup k hrncu. 

```
shared.mutex_accessing_pot.lock()
if shared.portions_left == NUM_PORTIONS_POT:
   shared.mutex_accessing_pot.unlock()
   break
else:
   shared.portions_left += 1
   print(f"Cook {i} added a portion! Portions left: {shared.portions_left} / {NUM_PORTIONS_POT}")
   shared.mutex_accessing_pot.unlock()
   sleep(0.2)
```

Ak je hrniec plný, kuchár odchádza od hrnca a preruší cyklus. Ak hrniec nie je plný, kuchár vloží porciu. Týmto spôsobom sa kuchári striedajú.

Na konci procesu sa kuchári navzájom počkajú na bariére, posledný z nich signalizuje divochovi v kuchyni, že kuchári dovarili a hrniec je opäť plný. Bariéra je znovu použiteľná a je implementovaná rovnakým spôsobom, ako tá v procese divochov.

###### Vizualizácia riešenia

Vizualizácia je znázornená pomocou jednotlivých `print` výpisov. V ukážkovom výpise som použil 5 divochov, 4 kuchárov a kapacitu hrnca 3.

```
Savage 0 is waiting. Count savages = 1 / 5
Savage 1 is waiting. Count savages = 2 / 5
Savage 2 is waiting. Count savages = 3 / 5
Savage 3 is waiting. Count savages = 4 / 5
Savage 4 signals to eat. Count savages = 5 / 5 

Savage 3 took portion! Portions left: 2 / 3
Savage 3 is eating!
Savage 2 took portion! Portions left: 1 / 3
Savage 2 is eating!
Savage 0 took portion! Portions left: 0 / 3
Savage 0 is eating!
Savage 1 signals cook that pot is empty and waits! 

Cook 2 added a portion! Portions left: 1 / 3
Cook 0 added a portion! Portions left: 2 / 3
Cook 1 added a portion! Portions left: 3 / 3
Cook 3 is waiting. Count cooks = 1 / 4
Cook 2 is waiting. Count cooks = 2 / 4
Cook 0 is waiting. Count cooks = 3 / 4
Cook 1 signals to leave kitchen. Savages EAT! Count cooks = 4 / 4 

Savage 1 took portion! Portions left: 2 / 3
Savage 1 is eating!
Savage 4 took portion! Portions left: 1 / 3
Savage 4 is eating!
Every savage has eaten. Ah #a@1, here we go again.
...
```

Podľa výpisov je možné vidieť poradie jednotlivých operácií. Medzerami som oddelil čakanie divochov na bariére, pristupovanie k hrncu a proces jedenia a nakoniec celý proces kuchárov. Na konci sa celý proces opakuje. Nižšie prikladám ešte jedno kolo výpisov. 

```
...
Savage 1 is waiting. Count savages = 1 / 5
Savage 2 is waiting. Count savages = 2 / 5
Savage 4 is waiting. Count savages = 3 / 5
Savage 0 is waiting. Count savages = 4 / 5
Savage 3 signals to eat. Count savages = 5 / 5 

Savage 3 took portion! Portions left: 0 / 3
Savage 3 is eating!
Savage 0 signals cook that pot is empty and waits! 

Cook 0 added a portion! Portions left: 1 / 3
Cook 1 added a portion! Portions left: 2 / 3
Cook 3 added a portion! Portions left: 3 / 3
Cook 2 is waiting. Count cooks = 1 / 4
Cook 3 is waiting. Count cooks = 2 / 4
Cook 0 is waiting. Count cooks = 3 / 4
Cook 1 signals to leave kitchen. Savages EAT! Count cooks = 4 / 4 

Savage 0 took portion! Portions left: 2 / 3
Savage 0 is eating!
Savage 1 took portion! Portions left: 1 / 3
Savage 1 is eating!
Savage 2 took portion! Portions left: 0 / 3
Savage 2 is eating!
Savage 4 signals cook that pot is empty and waits! 

Cook 2 added a portion! Portions left: 1 / 3
Cook 3 added a portion! Portions left: 2 / 3
Cook 1 added a portion! Portions left: 3 / 3
Cook 0 is waiting. Count cooks = 1 / 4
Cook 1 is waiting. Count cooks = 2 / 4
Cook 2 is waiting. Count cooks = 3 / 4
Cook 3 signals to leave kitchen. Savages EAT! Count cooks = 4 / 4 

Savage 4 took portion! Portions left: 2 / 3
Savage 4 is eating!
Every savage has eaten. Ah #$@1, here we go again. 
...
```

#### Zhrnutie bodov zadania

- [x] Divosi vždy začínajú jesť spolu --> Bariéra

- [x] Divosi si po jednom berú svoju porciu z hrnca --> `mutex_accessing_pot`

- [x] Divoch, ktorý zistí, že už je hrniec prázdny, upozorní kuchárov --> `full_pot.signal`

- [x] Divosi čakajú, kým kuchári doplnia --> `empty_pot.wait`

- [x] Kuchár vždy navarí jednu porciu a vloží ju do hrnca --> `while` cyklus a `mutex_accessing_pot`

- [x] Ked’ je hrniec plný, divosi pokračujú --> `empty_pot.signal()`

- [x] Proces sa opakuje

### Zdroje:

- PPDS_zadanie_velke.pdf

- Ukážkové kódy, najmä bariéry --> [GitHub - tj314/ppds-2023-cvicenia: This repo contains sources of the examples presented in seminars of the course PPDS of FEI STU.](https://github.com/tj314/ppds-2023-cvicenia)

- https://chat.openai.com/

- https://www.eiffel.org/doc/solutions/Dining_savages

- [operating system - Dining savages problem - Semaphores and Mutexes - Stack Overflow](https://stackoverflow.com/questions/70543411/dining-savages-problem-semaphores-and-mutexes)
