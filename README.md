# Dokumentácia prvého zadania

Úlohou prvého zadania bola implementácia *Bakery Algoritmu* z daného pseudokódu. Cieľom algoritmu je pomocou vzájomného vylúčenia zabezpečiť prístup k zdieľaným zdrojom pre viaceré procesy. Program obsahuje jeden spustiteľný súbor *.py*. Súbor môže byť spustený z ľubovoľného vývojového prostredia. Výstupom sú výpisy, ktoré demonštrujú prístup jednotlivých vlákien ku kritickej sekcii.

### Problematika paralelných výpočtov a Bakery Algoritmu

Problém nastáva, keď viaceré vlákna súčasne pristupujú k spoločnému zdroju, napríklad k zdieľanému súboru alebo premennej. *Bakery algoritmus* funguje na princípe prideľovania čísel jednotlivým procesom. Tieto čísla sa dajú chápať ako poradové čísla v čakárni. V podstate určujú prioritu, s ktorou sa proces má vykonať. Každému procesu je najskôr pridelené toto číslo, proces potom čaká dokým nebude mať najnižšie číslo z čakajúcich procesov, iba v tomto prípade je schopný vstúpiť do tzv. kritickej sekcie. <br>Kritická sekcia je miesto, kde proces ma prístup ku zdieľaným zdrojom. V tejto sekcii sa musí v danom okamihu nachádzať len jeden proces. Keď vlákno opustí kritickú sekciu, ďalšie môže vstúpiť.

### Dokumentácia kódu

Kód je napísaný v jazyku *python* vo verzii 3.10 a využíva knižnice *fei.ppds* na simulovanie procesu s niekoľkými vláknami a tiež knižnicu *time* z dôvodu použitia
funkcie *sleep*. <br>Ako prvé som si zadefinoval premenné polí `choosing` a `ticket_number`. Pole `choosing` uchováva `true` alebo `false` hodnotu, ktorá hovorí o tom či je konkrétne vlákno v procese výberu čísla. Pole `ticket_number` uchováva samotné číslo, ktoré bolo pridelené procesu.

###### Postup algoritmu

Beh Algoritmu je nasledovný. Vytvorí sa `N` počet vlákien, ktoré majú pridelený proces, ktorý majú vykonať. Algoritmus som rozdelil do štyroch funkcii, ktorých argumentom je ID daného vlákna `tid`. Prvou je funkcia `def process(tid)`, ktorú budú vlákna vykonávať. V tejto funkcii je definovaný počet vykonaní celého procesu.

Najskôr sa začína funkciou `def lock(tid)`, ktorá simuluje uzamknutie vlákna. Proces najskôr nastaví svoj `choosing` *boolean* na `true` a následne mu bude pridelené najvyššie číslo *+1* z poľa `ticket_number`. Po úspešnom výbere sa `choosing` *boolean* nastaví na `false`. Proces sa potom presune do *for* cyklu. V ňom sa nachádzajú dva `while` cykly. 

```
while choosing[j]:  
 sleep(0.001)

while ticket_number[j] != 0 
        and (ticket_number[j], j) < (ticket_number[tid], tid):  
 sleep(0.001)
```

Prvý cyklus čaká dokým bude každému vláknu pridelené číslo. Druhý cyklus kontroluje či má konkrétny proces najnižšie číslo. Ak áno, proces môže pokračovať ďalej do funkcie `def critical_section(tid)`. V tejto funkcii sa pomocou print výstupov oddelených `sleep` funkciou simuluje náročná operácia. Pri správnom fungovaní algoritmu musí daný proces najskôr vstúpiť a potom vystúpiť z kritickej zóny, tento postup simulujú print výstupy.

```
Thread 0 enters critical section
Thread 0 exits critical section
Thread 1 enters critical section
Thread 1 exits critical section
Thread 2 enters critical section
Thread 2 exits critical section
```

Po opustení kritickej sekcie nasleduje posledná funkcia `def unlock(tid)`, ktorá nastaví číslo procesu na 0, čím proces oznámi, že dokončil pristupovanie k zdieľaným zdrojom. Ako posledný prebehne cyklus, ktorý použitím funkcie `join` počká na vykonanie procesu v každom vlákne pred ukončením programu. 

```
for thread in threads:
    thread.join()
```

### Prečo je Bakery Algoritmus správnym riešením danej problematiky ?

Ako bolo spomenuté vyššie, *Bakery algoritmus* zabezpečuje vzájomne vylúčenie, ktoré vymedzuje prístup ku kritickej sekcii len jednému procesu v danom čase. Túto funkcionalitu zabezpečuje *ticket system*, v ktorom je každému vláknu pridelené unikátne číslo. Keď jeden proces obdrží číslo, nasledujúci proces obdrží číslo o jedna väčšie. Algoritmus potom počká dokým *všetky* procesy, ktoré chcú pristupovať ku kritickej sekcii majú svoje číslo a až potom sa postupne povoľuje prístup pre jednotlivé procesy. Takýto postup zabezpečuje férovosť prístupu ku zdrojom v konečnom čase. To znamená, že každé vlákno sa s určitosťou dostane na rad rovnaký počet krát ako ostatné vlákna. Vlákno s najnižším číslom v poradovníku získa prístup ako prvé a po dokončení sekcie je prístup udelený ďalšiemu v poradí. Týmto spôsobom sa proces môže opakovať. Procesy, ktoré nepristupujú ku zdieľaným zdrojom si nevyberajú žiadne číslo, tým pádom nie sú zaradené v poradovníku, preto nezabraňujú iným procesom vo vstupe do kritickej sekcie.

### Zdroje:

- [GitHub - tj314/ppds-2023-cvicenia: This repo contains sources of the examples presented in seminars of the course PPDS of FEI STU.](https://github.com/tj314/ppds-2023-cvicenia)

- [Lamport's bakery algorithm - Wikipedia](https://en.wikipedia.org/wiki/Lamport%27s_bakery_algorithm)

- [Bakery Algorithm in Process Synchronization - GeeksforGeeks](https://www.geeksforgeeks.org/bakery-algorithm-in-process-synchronization/)

- [Bakery Algorithm in OS | Scaler Topics](https://www.scaler.com/topics/operating-system/bakery-algorithm-in-os/)

- https://chat.openai.com

- https://cppsecrets.com/users/120612197115104981111171149751485164103109971051084699111109/Python-Implementation-of-Bakery-Algorithm.php
