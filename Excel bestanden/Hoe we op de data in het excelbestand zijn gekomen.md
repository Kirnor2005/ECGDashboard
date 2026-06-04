# Uitleg gegenereerde data

De toegereikte ECG-data is rechtstreeks gebruikt. 
Voor de overige variabelen zijn categorieën gegenereerd waarbij de meest voorkomende categorie (MVC) bewust richting een gezonde situatie is gekozen.

Vervolgens is aan iedere categorie een oplopende numerieke waarde toegekend. 
Om een gemiddelde waarde te schatten, is gebruikgemaakt van een gewogen gemiddelde waarbij de gewichten zijn bepaald met een Gaussische functie rond de modus (de meest voorkomende categorie). 
Hierbij krijgen categorieën die dichter bij de modus liggen een hoger gewicht dan categorieën die verder van de modus af liggen.

$$
w_i = e^{-\frac{(x_i-\mu)^2}{2\sigma^2}}
$$
