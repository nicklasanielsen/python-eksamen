# Python - Eksamens Projekt

## Projektnavn

Døgnrapporten

## Kort beskrivelse

I dette projekt har vi tænkt os at behandle data fra [Politiets døgnrapporter](https://politi.dk/doegnrapporter), hvor vi vil standardisere døgnrapporternes indhold ud fra hvilken type forbrydelse der har fundet sted, hvor og hvornår.

Når døgnrapporterne er blevet standardiseret, vil vi behandle dataene således, at vi vha. graffer kan illustrere hvordan udviklingen af forbrydelsen har ændret sig over en tidsperiode på landsplan, i de forskellige politikredse eller i et given postnummer.

Til slut har vi tænkt os, at illustrere mængden af typen af forbrydelse på et heatmap over Danmark.

Selve applikationen vil køre vha. CLI, hvor blandt andet typen af forbrydelse angives som parameter.

## Liste af teknologier brugt

- [gmaps](https://pypi.org/project/gmaps/)
- [geopy](https://pypi.org/project/geopy/)
- [nominatim](https://pypi.org/project/nominatim/)
- pandas
- selenium
- matplotlib.pyplot
- re
- requests
- bs4
- concurrent.futures.thread
- time
- numpy

## Installation Guide

Denne applikation er udviklet i det Docker miljø vi blev tildelt i starten af semesteret, og derfor anbefales det, at køre applikationen i dette miljø.

Ydeligere skal disse biblioteker installeres:

- Gmaps

  ```bash
  pip install gmaps
  ```

- Geopy

  ```bash
  pip install geopy
  ```

- Nominatim

  ```bash
  pip install nominatim
  ```

## User Guide

Efter installationsguiden er gennemført, skal notebooken - 'PYTHON_PROJEKT_DEMO' - åbnes.

I denne notebook, er funktionerne allerede opsat således, at det kun er start- og slut dato der skal ændres, samt hvilken type af hændelser man vil se.

Information om hvordan funktionerne indstilles, ses i notebooken.

## Status

Vi havde et ønske om, at applikationen skulle kunne køres fra terminalen, men grundet nogle af de biblioteker vi benyttede os af, var dette ikke muligt. Derfor har vi istedet valgt, at illustrere applikationens funktionalitet vha. en Jupyter notebook.

Applikationen kan ud fra en start- og slut dato indhente information fra landets politirapporter, og vise mængde af hændelser som heatmap, og som et søjlediagram.

Ikke alle landets politikredse er blevet implementeret, dette skyldes, at grundet opsætningen i deres døgnrapporter, at det ikke været muligt, at hente den ønskede data. Derudover er Københavns politi ikke implementeret, dette skyldes at de ikke har frigivet døgnrapporter siden midt november 2020.

Vi har dog formået at implementere 5 ud af landets 8 politikredse.

## Liste Af Udfordringer Projektet Vil Fremhæve

- Dataindsamling af dårligt opstillet data
- Databehandling vha. tråde
- Opsætning af data i søjlediagram
- Placering af data på kort

## Gruppemedlemmer

- [Mathias Haugaard Nielsen (cph-mn556)](https://github.com/Haugaard-DK/)
- [Nicklas Alexander Nielsen (cph-nn161)](https://github.com/nicklasanielsen/)
- [Nikolaj Larsen (cph-nl174)](https://github.com/Nearial)

