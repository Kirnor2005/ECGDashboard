# Uitleg gegenereerde data

De toegereikte ECG-data is rechtstreeks gebruikt. 
Voor de overige variabelen zijn categorieën gegenereerd waarbij het gemiddelde bewust richting een gezonde situatie is gekozen.

Vervolgens is aan iedere categorie een oplopende numerieke waarde toegekend. 
Om een gemiddelde waarde te schatten, is gebruikgemaakt van een gewogen gemiddelde waarbij de gewichten zijn bepaald met een Gaussische functie rond de modus (de meest voorkomende categorie). 
Hierbij krijgen categorieën die dichter bij de modus liggen een hoger gewicht dan categorieën die verder van de modus af liggen.

De originele formule voor Gaussian kernel smoother is:

```math
K(x^*,x_i) = \exp(- \frac{(x^* - x_i)^2}{2b^2})
```
waar $x^*$ het evaluatiepunt is en b (sigma in excel) de lengteschaal is.

De gebruikte gewichten zijn berekend met:
```math
w_i = \exp( -\frac{(x_i-modus)^2}{2b^2})
```

De richting word gegeven door: 
```math
\exp(- \lambda \max\{0, x_i-n\})
```
of
```math
\exp(-\lambda |x_i-n|)
```

Waarin n de hoeveelheid gezonde categorieën is en waarbij:

- $x_i$ = de numerieke waarde van een categorie  
- modus = de modus (meest voorkomende categorie)  

Het uiteindelijke gemiddelde is bij alles behalve BMI vervolgens berekend als:
```math
\bar{x} =\frac
{\sum_i x_i \cdot \exp\!\left(-\frac{(x_i-\text{modus})^2}{2b^2}-\lambda \max\{0, x_i-n\}\right)}
{\sum_i\exp\!\left(-\frac{(x_i-\text{modus})^2}{2b^2}-\lambda \max\{0, x_i-n\}\right)}
```

Het gemiddelde voor BMI is berekend als:
```math
\bar{x} =\frac
{\sum_i x_i \cdot \exp\!\left(-\frac{(x_i-\text{modus})^2}{2b^2}-\lambda |x_i-n|\right)}
{\sum_i\exp\!\left(-\frac{(x_i-\text{modus})^2}{2b^2}-\lambda |x_i-n|\right)}
```

Voor deze methode is gekozen omdat de werkelijke verdeling van de data onbekend is. Er is daarom aangenomen dat waarden die dichter bij de meest voorkomende categorie liggen waarschijnlijker zijn dan waarden die verder van deze categorie af liggen. Daarnaast is aangenomen dat de populatie overwegend gezond is, waardoor de meest voorkomende categorie in de richting van de gezonde categorieën is geplaatst.

- n was hier bij alles 1 behalve bij Bloeddruk (Bovendruk).
- $\sigma$ was bij allen 1
- $\lambda$ of de 'bias' was 0.14 om het niet al te veel af te laten wijken van de originele categorie

https://en.wikipedia.org/wiki/Kernel_smoother
