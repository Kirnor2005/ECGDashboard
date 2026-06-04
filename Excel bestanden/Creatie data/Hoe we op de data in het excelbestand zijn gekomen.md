# Uitleg gegenereerde data

De toegereikte ECG-data is rechtstreeks gebruikt. 
Voor de overige variabelen zijn categorieën gegenereerd waarbij de meest voorkomende categorie (MVC) bewust richting een gezonde situatie is gekozen.

Vervolgens is aan iedere categorie een oplopende numerieke waarde toegekend. 
Om een gemiddelde waarde te schatten, is gebruikgemaakt van een gewogen gemiddelde waarbij de gewichten zijn bepaald met een Gaussische functie rond de modus (de meest voorkomende categorie). 
Hierbij krijgen categorieën die dichter bij de modus liggen een hoger gewicht dan categorieën die verder van de modus af liggen.

De gebruikte gewichten zijn berekend met:
```math
w_i = \exp\left( -(x_i-\mu)^2 \cdot e^{\lambda \max\{0, x-n\}} \right)
```
Waarin n de hoeveelheid gezonde categorieën is en waarbij:

- $x_i$ = de numerieke waarde van een categorie  
- $\mu$ = de modus (meest voorkomende categorie)  
- $\sigma$ = de gekozen spreidingsparameter

Het uiteindelijke gemiddelde is bij alles behalve BMI vervolgens berekend als:
```math
\bar{x} = \frac{\sum x_i \cdot e^{-\lambda \max\{0, x_i-n\}}}{\sum e^{-\lambda \max\{0, x_i-n\}}}
```

Het gemiddelde voor BMI is berekend als:
```math
\bar{x} = \frac{\sum x_i \cdot e^{-\lambda |x_i-n|}}{\sum e^{-\lambda |x_i-n|}}
```

Voor deze methode is gekozen omdat de werkelijke verdeling van de data onbekend is. Er is daarom aangenomen dat waarden die dichter bij de meest voorkomende categorie liggen waarschijnlijker zijn dan waarden die verder van deze categorie af liggen. Daarnaast is aangenomen dat de populatie overwegend gezond is, waardoor de meest voorkomende categorie in de richting van de gezonde categorieën is geplaatst.

- n was hier bij alles 1 behalve bij Bloeddruk (Bovendruk).
- $\sigma$ was bij allen 1
- $\lambda$ of de 'bias' was 0.14 om het niet al te veel af te laten wijken van de originele categorie
