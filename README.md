# Landgoed-Blom
Landgoed Blom provisioning scripts

## Installatie
Je hebt Python 3.11 of hoger nodig. Installeer dependency manager poetry en de dependencies:
```shell
pip install poetry
poetry install
```

## Scripts
### Gebruikersbeheer

In de platformoplossing staat een document met de deelnemers van Landgoed Blom. Het script voor het beheer van de
gebruikers maakt gebruik van dit document om gebruikers te activeren en deactiveren. Verwijderen van gebruikers is
altijd een handmatige actie.

Het script doet het volgende
- [X] Het script downloadt de tabel met gebruikers
- [X] Voor iedere gebruiker in de lijst controleert het script of deze gebruiker al in het communicatieplatform actief is. 
- [X] Bestaat het account nog niet, dan wordt het aangemaakt en krijgt de gebruiker een mail met het wachtwoord
- [ ] Voor iedere gebruiker in de tabel kijkt het script of de gebruiker actief is. De status wordt overeenkomstig aangepast in het platform.
- [ ] Het script haalt de lijst met actieve gebruikers op en deactiveert iedere gebruiker die niet in de tabel van gebruikers staat.
