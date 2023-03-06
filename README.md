# Dokumentácia druhého zadania

Úlohou druhého zadania bola implementácia *Sleeping barber problému* z daného
pseudokódu a šablóny. Podstata problému spočíva v prístupe k zdieľaným zdrojom algoritmu. Zdieľanými zdrojmi sú v tomto prípade **miesta v čakárni** a **stolička**, na ktorej holič strihá. Pokiaľ holič nemá žiadnych zákazníkov tak spí. Po príchode zákazníka sa zobudí a začne strihať. Čakáreň má len obmedzené množstvo miest, preto ak je plná, zákazník odchádza.

### Problematika *Sleeping barber*

Problém nastáva, keď sa jednotlivé vlákna, v tomto prípade zákazník a holič, snažia pristupovať ku zdieľaným zdrojom, ako je napríklad počet ľudí v čakárni alebo stolička na holenie. Pre implementovanie algoritmu je potrebné vzájomné vylúčenie pri pristupovaní k týmto zdrojom a taktiež vhodná signalizácia, aby sa predišlo zaseknutiu (*deadlock*).

### Dokumentácia kódu

Kód je napísaný v jazyku *python* vo verzii *3.10* a využíva knižnice *fei.ppds* na simulovanie procesu s niekoľkými vláknami, knižnicu *time* z dôvodu použitia funkcie *sleep*. Funkcia *sleep*simuluje nejaký proces (strihanie, čakanie...). Použil som taktiež funkciu *randint* z knižnice *random* na simuláciu nerovnomerného času rôznych operácií. <br>

Ako prvé som si zadefinoval všetky potrebné premenné a semafory pre zákazníkov a holiča v zdieľanej triede. Potom som vyplnil jednotlivé funkcie z poskytnutej šablóny. Pridal som do nich funkciu *sleep* a *print* výpis, ktorý simuluje a opisuje danú akciu.

##### Postup algoritmu

Beh Algoritmu je nasledovný. Vytvorí sa `C` počet vlákien, ktoré majú pridelený proces pre zákazníka a jedno vlákno, ktorému je pridelený proces holiča.

###### Proces zákazníka

Najskôr sa uzamkne vlákno a vymedzí sa preň prístup k zdieľanému zdroju `waiting_room`. V podmienke `if shared.waiting_room < N` sa porovná či počet zákazníkov dosiahol kapacitu čakárne. Ak áno, vlákno sa odomkne a umožní prístup do kritickej sekcie ďalšiemu vláknu. Táto operácia simuluje odchod zákazníka na nejaký čas (`balk(i)`). Ak miesnosť nie je plná, zákazník môže vstúpiť. Vlákno zvýši počet zákazníkov v miestnosti, zasignalizuje holičovi, že zákazník je pripravený sa dať strihať a opustí kritickú sekciu. Po ostrihaní sa čaká na signál od holiča a zákazníka či už dokončili svoje funkcie `get_haircut(i)` a `cut_hair()`.

###### Proces holiča

Analogicky, pri tomto procese holič čaká na signál od zákazníka, že vstúpil do čakárne. *Mutex* v tomto procese slúži na vymedzenie prístupu do kritickej sekcie a odčítanie zákazníka z čakárne v momente, keď sa ide strihať. Po ostrihaní sa čaká na signál od holiča a zákazníka či už dokončili svoje funkcie `get_haircut(i)` a `cut_hair()`.

###### Vizualizácia riešenia

Vizualizácia je vyriešená pomocou jednotlivých `print` výpisov. Implementácia tiež **povoľuje predbiehanie** zákazníkov.

```
CUSTOMER 0 has entered the waiting room, SEATS occupied: 1
CUSTOMER 1 has entered the waiting room, SEATS occupied: 2
CUSTOMER 2 has entered the waiting room, SEATS occupied: 3
Waiting room is FULL, CUSTOMER 3 is leaving.
Waiting room is FULL, CUSTOMER 4 is leaving.

BARBER is cutting hair.

CUSTOMER 1 is getting a haircut.
CUSTOMER 3 has entered the waiting room, SEATS occupied: 3
Waiting room is FULL, CUSTOMER 4 is leaving.
CUSTOMER 1 is DONE getting a haircut and LEAVING
CUSTOMER 1 is growing hair.

BARBER is DONE cutting hair


BARBER is cutting hair.

CUSTOMER 2 is getting a haircut.
CUSTOMER 4 has entered the waiting room, SEATS occupied: 3
CUSTOMER 2 is DONE getting a haircut and LEAVING
Waiting room is FULL, CUSTOMER 1 is leaving.

BARBER is DONE cutting hair
...
```

Podľa výpisov je možné vidieť poradie jednotlivých operácií. Pri plnej čakárni zákazník odíde. Keď holič začne strihať uvoľní sa jedno miesto v čakárni a zákazník môže vojsť. Taktiež sa vypíše, ktorý zákazník sa práve šiel strihať. Po ostrihaní zákazník odchádza, nejakú dobu mu rastú vlasy a holič si berie ďalšieho pána na holenie.

### Zdroje:

- [Sleeping barber problem - Wikipedia](https://en.wikipedia.org/wiki/Sleeping_barber_problem)

- [A Simple Guide to &quot;The Sleeping Barber&quot; Problem - YouTube](https://www.youtube.com/watch?v=cArBsUK1ufQ&ab_channel=EliTadeo)

- https://www.codingninjas.com/codestudio/library/sleeping-barber-problem

- [Sleeping Barber problem in Process Synchronization - GeeksforGeeks](https://www.geeksforgeeks.org/sleeping-barber-problem-in-process-synchronization/)

- https://www.hindicodingcommunity.com/2023/02/sleeping-barber-problem-in-process.html

- https://chat.openai.com
