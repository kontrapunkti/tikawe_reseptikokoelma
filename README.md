# Reseptikokoelma

Tämä projekti on suoraan kurssimateriaalin ehdotuksista

## Sovelluksen toiminnot
* Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset ja valmistusohje.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt reseptit.
* Käyttäjä pystyy etsimään reseptejä hakusanalla.
* Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
* Käyttäjä pystyy valitsemaan esimerkiksi seuraavia luokitteluja:
  * Ruoan tyyppi: alkuruoka, pääruoka tai jälkiruoka
  * Ruokavalio: laktoositon, gluteeniton tai vegaaninen
* Käyttäjä pystyy antamaan reseptille kommentin ja arvosanan. Reseptistä näytetään kommentit ja keskimääräinen arvosana.

## Välipalautus 2
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan reseptejä
* Käyttäjä näkee sovellukseen lisätyt tietokohteet etusivulla, käyttäjäsivulla ja hakukentässä
* Käyttäjä pystyy etsimään tietokohteita hakusanalla otsikosta

## Sovelluksen asennus

```
pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
```

## Demoaineisto
Jos haluat luoda demoaineiston, aja seuraava komento
```
$ python3 demodata.py
```

Demoaineistossa on 10 käyttäjää, joiden kaikkien salasana on "salasana". Jokaiselle on luotu eri määrä reseptejä.

```
usernames = ["kalle", "maija",, "pekka", "matti", "liisa", "anna", "jari", "minna", "teemu", "sara"]
```

## Sovelluksen käynnistäminen

Käynnistä sovellus:
 
```
flask run
```