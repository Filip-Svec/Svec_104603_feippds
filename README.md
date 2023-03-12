# Dokumentácia tretieho zadania

Úlohou tretieho zadania bola implementácia problému *Večerajúcich filozofov* jednou z dvoch metód. Prvou metódou bolo rozdelenie filozofov na ľavákov a pravákov, druhou metódou bola implementácia tokenu. Podstata problému spočíva v prístupe k zdieľaným zdrojom algoritmu. Zdieľanými zdrojmi sú v tomto prípade **vidličky**, s ktorými filozofi jedia. V mojom zadaní som sa rozhodol použiť spôsob implementácie ľavákov a pravákov.

### Problematika *večerajúcich filozofov*

Problém nastáva, keď sa jednotlivé vlákna, v tomto prípade filozofi, snažia pristupovať ku zdieľaným zdrojom, vidličkám. Na to aby sa filozof mohol navečerať potrebuje na to obe vidličky. Avšak medzi každým filozofom sa nachádza len jedna vidlička. V prípade, že každý filozof zoberie práve jednu, žiadny z nich sa nemôže najesť a nastáva deadlock. 

### Dokumentácia kódu

Kód je napísaný v jazyku *python* vo verzii *3.10* a využíva knižnice *fei.ppds* na simulovanie procesu s niekoľkými vláknami, knižnicu *time* z dôvodu použitia funkcie *sleep*. Funkcia *sleep* simuluje nejaký proces (myslenie alebo jedenie). <br>

Ako prvé som si zadefinoval pole vidličiek. Jednotlivé vidličky v poli sú typu Mutex. Ďalej som vytvoril filozofov (vlákna) a pridelil im funkciu, ktorú budú vykonávať (`philosopher`).

##### Postup algoritmu (ľaváci, praváci)

Beh Algoritmu je nasledovný. Vytvorí sa `N` počet vlákien, ktoré začnú vykonávať proces `philosopher`.

V prvej podmienke `is_right_handed = i % 2 == 0` sa podľa indexu vlákna rozhodne či bude filozof ľavák alebo pravák. Ja som sa rozhodol spraviť každého druhého filozofa pravákom. Týmto spôsobom sa naraz môže najesť viacej filozofov, aspoň to bola moja teória. Avšak pri testovaní či už som použil tento spôsob alebo implementáciu s jedným pravákom, výsledok mi prišiel podobný ak nie rovnaký, každý filozof sa najedol v rozumnom čase.

Samotná implementácia pravákov a ľavákov prebieha v podmienke: 

```
    if is_right_handed:
        first_fork = (i + 1) % NUM_PHILOSOPHERS
        second_fork = i
    else:
        first_fork = i
        second_fork = (i + 1) % NUM_PHILOSOPHERS
```

Väčšina zdrojov uvádza jednotlivé premenné ako *pravá, ľavá* vidlička. Ja som použil prvá a druhá kvôli prehľadnosti. Či je vidlička pravá alebo ľavá je dané indexom kde `i` je ľavá a `i + 1` je pravá. Či je filozof pravák alebo ľavák je udané tým, ktorú z týchto dvoch vidličiek zodvihne ako prvú, preto názvy premenných sú `first_fork` a `second_fork`. Samozrejme toto je len moja vizualizácia problému, kľudne to môže byť implementované aj opačne.

Vo `for` cykle sa potom strieda proces jedenia a myslenia. Medzi nimi sa filozof snaží získať vidličky tým, že uzamkne *mutex* najskôr prvej a potom druhej vidličke. Po dojedení ich položí späť na stôl.

###### Vizualizácia riešenia

Vizualizácia je vyriešená pomocou jednotlivých `print` výpisov.

```
Philosopher 0 is thinking!
Philosopher 1 is thinking!
Philosopher 2 is thinking!
Philosopher 3 is thinking!
Philosopher 4 is thinking!
Philosopher 5 is thinking!
Philosopher 3 is eating!
Philosopher 5 is eating!
Philosopher 1 is eating!
Philosopher 3 is thinking!     # 3,5,1 najedeny
Philosopher 1 is thinking!
Philosopher 4 is eating!
Philosopher 5 is thinking!     # 3,5,1,4 najedeny
Philosopher 2 is eating!
Philosopher 0 is eating!
Philosopher 4 is thinking!
Philosopher 2 is thinking!     # 3,5,1,4,2,0 najedeny
...
```

Podľa výpisov je možné vidieť poradie jednotlivých operácií. Každý filozof sa najedol predtým, ako by sa hociktorý druhý najedol dvakrát. To však nemusí byť pravidlom. Aj pri tejto implementácii môže dôjsť k vyhladovaniu filozofa, to záleží už len od implementácie samotného vyhladovania. Ale predpoklad ostáva ten, že filozof by sa mal dostať k vidličke v konečnom čase.

#### Porovnanie s implementáciou pomocou čašníka

Implementácia s čašníkom funguje na princípe semaforu, ktorý povolí prístup len určitému počtu filozofov, tak aby sa aspoň jeden vždy najedol a nedošlo k deadlocku. Tento prístup zabezpečí relatívnu férovosť a postupnosť prístupu k obmedzenému zdroju.  Avšak v porovnaní s prístupom pravákov a ľavákov je tento postup pomalší kvôli použitiu semafora. V implementácii pravákov a ľavákov môže súčasne jesť viacero filozofov, nie je použitý žiaden semafor alebo mutex naviac, preto je toto riešenie rýchlejšie. Jeho nevýhodou je potenciálna neférovosť prístupu k zdieľanému zdroju. Keďže prístup nie je regulovaný, záleží len na tom či sú obe vidličky dostupné.

### Zdroje:

- https://pages.mtu.edu/~shene/NSF-3/e-Book/MUTEX/TM-example-left-right.html

- [The Dining Philosophers problem and different ways of solving it | ZeroBone](https://zerobone.net/blog/cs/dining-philosophers-problem/)

- [Dining philosophers problem - Wikipedia](https://en.wikipedia.org/wiki/Dining_philosophers_problem)

- https://chat.openai.com/

- [Dining Philosophers problem - GeeksforGeeks](https://www.geeksforgeeks.org/dining-philosophers-problem/)

- https://www.stolaf.edu/people/rab/pdc/text/dpsolns.htm
