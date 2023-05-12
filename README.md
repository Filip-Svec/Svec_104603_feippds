# Dokumentácia piateho zadania

Úlohou piateho zadania bola implementácia *konverzie obrázku do čiernebieleho formátu*.  Táto operácia je paralelizovaná na GPU pomocou python numba. Na testovanie som použil emulátor. 

### Manuál

Zadanie som implementoval nasledovným spôsobom. Z priečinka si načítam súbory, ktoré postupne v cykle konvertujem do *greyscale*. Prvý cyklus zabezpečuje prevedenie pomocou GPU a druhý cyklus pomocou CPU.

```
# Loop through all files using GPU
    for filename in files:
        print(filename)
        start_time = time.time()
        image = plt.imread("imgz/" + filename)
        newImage = grayscale(image)
        print("--- %s seconds ---" % (time.time() - start_time))
        plt.imsave("imgz_grey/" + "grey_" + filename, newImage, cmap='gray', format="jpg")

# Loop through all files using CPU
for filename in files:
    print(filename)
    start_time = time.time()
    image = plt.imread("imgz/" + filename)
    grayscale_CPU(image)
    print("--- %s seconds ---" % (time.time() - start_time)) 
```

Súbory čerpám z priečinka `directory = "imgz/"  files = os.listdir(directory)`. Na spustenie programu je potrebné mať obrázky uložené v tomto priečinku *imgz* na rovnakej priečinkovej úrovni ako .py. Na koniec si súbory vrátené funkciou `grayscale` uložím do separátneho priečinka a vypíšem čas trvania a veľkosť obrázka.

### Konverzia do *greyscale*

Najskôr si získam dimenzie vstupu a alokujem preň miesto ako aj pre výstup funkciou `cuda.to_device(image)`.

Ďalej nastavím počet vlákien v jednom bloku a počet blokov v gride. Tie sa odvíjajú aj od veľkosti vstupu.

```
threads_per_block = (16, 16)  
blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]  
blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]  
blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
```

V nasledujúcom kroku už spúšťam kernel v ktorom sa budú vykonávať paralelné výpočty. Nakoniec funkciou `copy_to_host()` pošlem výsledný súbor na výstup.

### Kernel

Vo vnútri kernela vykonávam konverziu rgb obrázka do čierno bieleho kanála. 

```
row, col = cuda.grid(2)  # Get the thread's row and column indices
if row < image.shape[0] and col < image.shape[1]:
    r, g, b = image[row, col]
    gray[row, col] = 0.21 * r + 0.72 * g + 0.07 * b
```

Získam si indexi stĺpcov a riadkov. Ak by som nepoužil podmienku if program by bol schopný konvertovať  iba obrázky o veľkosti `2 na n-tú`. 

### Výsledky

Použitím emulátora som nedosiahol najlepšie časové výsledky pri paralelizácii na GPU. Emulátor bol o mnoho pomalší ako CPU. Všetky výstupy som si uložil, ako pre CPU tak aj pre GPU. V nasledujúcej časti ich prezentujem:

Nasledujúca sada obrázkov má rozmer 256x256 a časy sú v poradí emulátor, CPU.

```
Karin_Viard_3.jpg
--- 9.24954 seconds ---
--- 0.00680 seconds ---
Katalin_Kollat_2.jpg
--- 9.01132 seconds ---
--- 0.00210 seconds ---
Kate_Winslet_0.jpg
--- 9.52286 seconds ---
--- 0.00100 seconds ---
Kate_Winslet_1.jpg
--- 9.27454 seconds ---
--- 0.00187 seconds ---
Katja_Riemann_0.jpg
--- 9.23245 seconds ---
--- 0.00199 seconds ---
```

Nasledujúce obrázky už majú väčšiu veľkosť najväčší má rozmer 2500x2500:

```
do_uef.png
width: 324, height: 324
--- 23.101183891296387 seconds ---
--- 0.0029997825622558594 seconds ---

harryHIHI.jpg
width: 684, height: 821
--- 117.49907660484314 seconds --- 
--- 0.009999275207519531 seconds --- 

Dreamdog.png
width: 800, height: 800
--- 130.02981090545654 seconds ---
--- 0.01600360870361328 seconds ---

tornadoe.jpg
width: 1051, height: 700
--- 135.702474734437920 seconds ---
--- 0.01400038281900112 seconds ---

nike.jpg
width: 1000, height: 1000
--- 209.76203322410583 seconds --- 
--- 0.023000478744506836 seconds ---

luoping china.jpg
width: 1920, height: 1080
--- 389.290239482039489 seconds ---
--- 0.03450594838393233 seconds ---

yuru camp 2.jpg
width: 2204, height: 1364
--- 571.998389238229228 seconds ---
--- 0.13350847774638001 seconds ---

pink-sky.jpg
width: 2500, height: 2500
--- 1263.12779584489982 seconds ---
--- 0.13350847774638001 seconds ---
```

Všetky obrázky sa nachádzajú v github repozitári.

### Zdroje:

- PPDS_zadanie_cuda.pdf

- Ukážkové kódy --> [GitHub - tj314/ppds-2023-cvicenia: This repo contains sources of the examples presented in seminars of the course PPDS of FEI STU.](https://github.com/tj314/ppds-2023-cvicenia)

- https://chat.openai.com/

- [Memory management &mdash; Numba 0.50.1 documentation](https://numba.pydata.org/numba-doc/latest/cuda/memory.html)

- [Introduction to Numba: CUDA Programming](https://nyu-cds.github.io/python-numba/05-cuda/)
