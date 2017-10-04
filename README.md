# Bruk av geopandas med data fra NVDB og SSB

Demo av hvordan geopandas kan brukes med data fra [Nasjonal vegdatabank](https://www.vegvesen.no/fag/teknologi/Nasjonal+vegdatabank) (NVDB) og [Statistisk Sentralbyrå](http://www.ssb.no/natur-og-miljo/geodata) (SSB). 

Vi ønsker å finne hvilke turistveger som går gjennom hvilke sentrumsområder - og hvilke trafikkulykker som er registrert der. 

Gangen er som følger: 
1. Last ned data over sentrumsområder fra [SSB](http://www.ssb.no/natur-og-miljo/geodata
1. Last ned turistveger fra [NVDB api](https://www.vegvesen.no/nvdb/apidokumentasjon/)
1. Finn snittet av turistveger og sentrumsområder (hvilke turistveger som går gjennom hvilke sentrumsområder)
1. Finn trafikkulykkene på turistvegene som går gjennom sentrumsområder. 
    1. Finn BoundingBox for hvert av sentrumsområdene 
    1. Hent trafikkulykker innenfor BBox. M
    1. Finn trafikkulykkene som ligger på turistvegens senterlinje
        1. Alternativt finn trafikkulykkene innenfor radius fra turistvegen. 
1. Lag fine plott og sånn

# Installasjon

Anbefaling - Anaconda distribusjon på din plattform (testet på linux og windows). 

Disse python-bibliotekene: 

* Shapely
* Pandas
* Geopandas
* For nedlasting fra SSB (kan være like greit å laste ned manuelt?) 
    * requests (også påkrevd for ```nvdapi.py```)
    * shutil 
* _sikkert noen flere_ 
* ```nvdbapi.py``` og ```nvdb2geojson.py``` fra [NVDBapi-v2 reposet](https://github.com/LtGlahn/nvdbapi-V2)

Koden finnes både som kjørbare python-script og som jupyter notebook _(Geopandas-nvdb-eksempel.ipynb)_. 

## De kule tingene kan være vrient på Windows

Litt om hvordan man får tak i Geopandas og øvrige bibliotek på Windows-plattform. 

# NB! WORK IN PROGRESS! 

Foreløbig kun skjelettet til det som skal bli kule ting... 
