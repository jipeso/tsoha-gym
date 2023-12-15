# Opetussovellus

Sovelluksen avulla voidaan järjestää verkkokursseja, joissa on tekstimateriaalia ja automaattisesti tarkastettavia tehtäviä. Jokainen käyttäjä on opettaja tai opiskelija.

Sovelluksen ominaisuuksia ovat:

* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Opiskelija näkee listan kursseista ja voi liittyä kurssille.
* Opiskelija voi lukea kurssin tekstimateriaalia sekä ratkoa kurssin tehtäviä.
* Opiskelija pystyy näkemään tilaston, mitkä kurssin tehtävät hän on ratkonut.
* Opettaja pystyy luomaan uuden kurssin, muuttamaan olemassa olevaa kurssia ja poistamaan kurssin.
* Opettaja pystyy lisäämään kurssille tekstimateriaalia ja tehtäviä. Tehtävä voi olla ainakin monivalinta tai tekstikenttä, 
  johon tulee kirjoittaa oikea vastaus.
* Opettaja pystyy näkemään kurssistaan tilaston, keitä opiskelijoita on kurssilla ja mitkä kurssin tehtävät kukin on ratkonut.

DONE: Sovelluksen runko ok kunnosssa, tietokantaan luotu tarvittavat taulut, kirjautuminen ja rekisteröinti toimii.

TODO: Opettajan toiminnot, kurssien sivut ja tehtävät, tilasto tehtävistä, ulkoasu.

Sovelluksen testaus:

1. Kloonaa repositorio omalle koneelle ja siirry sen juurikansioon.
2. Luo .env tiedosto ja määritä sen sisältö:
     DATABASE_URL=tietokannan-paikallinen-osoite
     SECRET_KEY=salainen-avain
3. Aktivoi virtuaaliympäristö venv ja asenna riippuvuudet komennolla pip install -r ./requirements.txt
4. Määritä tietokannan skeema komennolla psql < schema.sql
5. Käynnistä sovellus komennolla flask run
