# Passar por tudo e retirar aspas, \n, espaços e tabs. 
# Retirar os N/A's e empty values

# 1 Juntar estas todas 
Diet: 2519  
Prey: 1408
Favorite Food: 981
Main Prey: 771
Diet for this Fish: 160

# 2 Intervalos
Lifespan: 2147    ---> Provavelmente fazer parsing de intervalos para valor médio ou converter tudo para uma só unidade
Weight: 1843
Length: 1582 
Height: 617
Wingspan: 407
Average Spawn Size: 170
Estimated Population Size: 946 ----> Soome are in interval, some are numbers, other are just stable. 

# 3
Age of Sexual Maturity: 859
Age of Weaning: 402
Age Of Independence: 210
Age of Molting: 182
Age Of Fledgling: 170
Gestation Period: 810
Incubation Period: 440

# 4 Binário
Migratory: 222   ------>  É só um 1. Acrescentar 0 a todos os outros que faltam, para colocar em todos os animais.
Venomous: 784    ------> É só um Sim. Trocar todos para 1 e 0.

# 5 Join Columns
Optimum pH Level: 157  -----> join with the below one
Optimum PH Level: 3 

Litter Size: 781    ------> Join with average Clutch Size
Average Clutch Size: 261

Predators: 1413      -----> Still thinking about what to do with these 2. Maybe join with Biggest Threat
Biggest Threat: 1336

Most Distinctive Feature: 1541 ----> Join together with the below ones. Don't forget about adding connection and capital letters.
Distinctive Feature: 735 
Special Features: 263

Location: 1155   -----> They are mostly the same, but check anyways.
Origin: 360

Common Name: 1587  -----> Join, and make sure they are not repeated.
Other Name(s): 1100

Fun Fact: 2352   ----> Fun fact and slogan are the same, but they are both the same as the Quote (check for Special cases when there are both slogan and fun fact, and join the different one to quote)
Slogan: 698

# 6 Fiill empty values
Name Of Young: 1247    ----> Para cães ou gatos colocar "puppy" ou "kitten"

# 7 Join together with a formated string
Aggression: 809
Temperament: 542
Group Behavior: 1493

# 8 Convert to km/h
Top Speed: 755  ----> Seems to be well formated, but still need to check

Color: 2380
Skin Type: 2363

Habitat: 1692
Nesting Location: 439

Lifestyle: 1232
Type: 1182





# DROP:
Group: 539
Average Litter Size: 600
Training: 117
Number Of Species: 1076


João 2 e 4