# Projekt 1 - Razvoj web aplikacija
Moj 1. projekt sadrži Swagger Rest API aplikaciju "Event API" strukturiranu po MVC patternu. U aplikaciji postoje 3 načina autentifikacije: Admin Auth (ADMIN_KEY=ja_sam_admin), Basic Auth sa email-om i zaporkom, te Bearer Auth pomoću tokena. 
Dijelovi API-ja su Auth Api (login, logout), Admin Api (za pristup do svih korisnika i napravljenih događaja), User Api (za pristup korsinicima do njihovih podataka) i Event Api (za kreiranje i pristup događajima).

**Aplikaciju klonirati i pokrenuti po sljedećim uputama:**
  * ```git clone https://github.com/unizd-sit-web/pzw-zavrsni-projekt-msaravanj.git```
  * ```(projekt otvoriti u editoru VSCode-u)```
  * ```(otvoriti Terminal unutar Editora)```
  * ```py -m venv venv```
  * ```.\venv\Scripts\Activate.ps1```
  * ```pip install -r requirements.txt```
  * ```$env:FLASK_APP="app.py"```
  * ```$env:FLASK_DEBUG=1```
  * ```flask run```
  * ```aplikaciju otvoriti u web pregledniku na localhost:5000```

Nakon što ste uspješno pokrenuli aplikaciju potrebno je inicijalizirati bazu podataka preko Admin API-ja (init-db).
Zatim možete kreirati nove korisnike i događaje preko POST metoda, uređivati podatke pomoću PUT metoda, dohvaćati podatke pomoću GET metoda i brisati sadržaje pomoću DELETE.
