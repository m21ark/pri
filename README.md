# PRI Project

Query 4:  
Animals that generally walk in groups and their respective hierarchy and how they deal with territory: 
    - duvidas na classificação --- Zebra, OX, Mongoose(contraditorio em alguns casos), ELK(n fala do territorio?), Wood Bison(n fala da hierarquia), Sika Deer(tem dos dois casos grupo/alone), African Forest Elephant(dois casos), Giraffe, Teddy Guinea Pig, Arctic Fox
    - no V1 : Saber Toothed Tiger, Bhutan Takin(os males podem ficar sozinhos durante uma ano), Lace Monitor(engraçado de se falar, n é social), Husky(n sei, parece forçado)

Energetic dog breeds suited for hunting
North America animals that like to eat insects
Change the color of their skin, fur or feathers for the purpose of camouflage
Animals that walk in hierarchical groups or herds and how they deal with territory
Animals that are (NOT birds) that migrate to Mexico


{
    "params": {
      "defType": "edismax",
      "fl": "Name, Genus",
      "indent": true,
      "q": "",
      "ps": "10",
      "tie": "0.1",
      "mm": "1",
      "qf": "Behavior^1.5 Text^1.2 Class^1.0 Migratory^1.2 Fun_Fact^1.5 Features^1.5 Origin^1.2 Diet^1.2 Genus^1.5",
      "bq": "Text:(\"change color\"~5)^2 OR (\"change skin\"^3~5) OR (\"change fur\"^2~5) OR camouflage^2^2",
      "rows": 30
    }
  }
  


"q": [
      "Text:group*^2.5",
      "Behavior:Herd^2.0",
      "Behavior:pack^2.0",
      "Text:Herd^1.3",    
      "Text:pack*^1.8",
      "Text:community*^1.6",
      "Text:social*~1^1.5",
      "Text:hierarchy^1.9",
      "Text:\"social structure\"~4^1.5",
      "Text:territory*^2.8",
      "Text: \"mark territorial\"~3^2.4",
      "Text: \"territorial behavior\"~3^2.4",
      "Text: \"deal with territory\"~2^2.4"
    ]