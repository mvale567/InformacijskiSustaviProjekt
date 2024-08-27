<h1>Opis Projekta: Skladište Bicikala</h1>
Opis
Projekt skladišta bicikala ima za cilj razvoj sofisticiranog sustava za upravljanje biciklima u skladištu. Ovaj sustav omogućuje radnicima i korisnicima da efikasno i precizno upravljaju biciklima kroz različite funkcionalnosti poput pregleda, dodavanja, brisanja i uređivanja stavki. Također pruža alat za analizu podataka o biciklima, čime omogućuje bolje donošenje odluka i optimizaciju upravljanja skladištem.

<h2>Ključne Funkcionalnosti:</h2>

<h4>Pregled Bicikala:</h4>
Omogućuje korisnicima da pregledaju sve bicikle u skladištu.
Informacije uključuju osnovne podatke poput marke, modela, veličine okvira, težine, broj brzina, godina proizvodnje, namjene, cijene i dodatnog opisa.

<h4>Dodavanje Bicikala:</h4>
Omogućuje korisnicima da dodaju nove bicikle u sustav.
Forme za unos detalja bicikla, istih gore navedenih koje mogu pregledavati.
Automatsko generiranje jedinstvenih identifikatora za svaki bicikl radi lakše identifikacije i praćenja.

<h4>Brisanje Bicikala:</h4>
Omogućuje korisnicima da uklone bicikle iz sustava kada ime više nisu potrebni ili su prodani.
Postavljanje potvrde za brisanje kako bi se izbjegle greške.

<h4>Uređivanje Stavki:</h4>
Omogućuje korisnicima da ažuriraju informacije o biciklima, odnosno sve inofrmacije unesene pri dodavanju bicikla

<h4>Analiza Stavki:</h4>
Pruža alat za analizu podataka o biciklima u skladištu.
Izvještaji i grafikon koji pokriva broj bicikala po namjeni.

<h1>Upute za instalaciju</h1>
<h4>Prvo, moraš imati instaliran Git na svom računaru.
I obavezno pokrenut Docker Desktop. Nakon toga naredbe redom unositi u terminal.</h4>


cd Downloads

git clone https://github.com/V-DevCode/InformacijskiSustaviProjekt.git

cd InformacijskiSustaviProjekt

docker build -t todo .

docker ps

docker run -p 8080:8080 todo

