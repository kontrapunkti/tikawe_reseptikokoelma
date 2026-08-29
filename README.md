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
* Käyttäjä pystyy antamaan reseptille arvosanan. Reseptistä näytetään arvioiden määrä ja keskimääräinen arvosana.
* Käyttäjä voi muuttaa aiemmin antamaansa arvosanaa.
* Käyttäjä näkee omien reseptiensä arviointitilastot käyttäjäsivulla.

## Sovelluksen asennus

1. Asenna Flask
```
pip install flask
```

2. Luo tietokanta

```
$ sqlite3 database.db < schema.sql
```

4. Käynnistä sovellus
```
flask run
```

## Demoaineisto
Jos haluat luoda demoaineiston, aja seuraava komento ennen sovelluksen käynnistämistä.
```
python3 demodata.py
```

Demoaineistossa on 10 käyttäjää, joiden kaikkien salasana on "salasana". Jokaiselle on luotu eri määrä reseptejä. Tiedosto tyhjentää tietokannan ja luo satunnaiset reseptit, mutta ei luo arviointeja.

```
usernames = ["kalle", "maija", "pekka", "matti", "liisa", "anna", "jari", "minna", "teemu", "sara"]
```

## Config
Vaihda tiedoston config.py secret_key johonkin satunnaiseen merkkijonoon ennen sovelluksen käyttöönottoa.
