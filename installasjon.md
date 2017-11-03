
# Installasjon

Anbefaling - Anaconda distribusjon på din plattform (testet på linux og windows). 

Disse python-bibliotekene: 

* Shapely
* Pandas
* Geopandas
* For nedlasting fra SSB (kan være like greit å laste ned manuelt?) 
    * requests (også påkrevd for ```nvdapi.py```)
    * shutil 
* *work in progress*, mere kommer.
* ```nvdbapi.py``` og ```nvdb2geojson.py``` fra [NVDBapi-v2 reposet](https://github.com/LtGlahn/nvdbapi-V2)

Koden finnes både som kjørbare python-script og som jupyter notebook _(Geopandas-nvdb-eksempel.ipynb)_. 

## De kule tingene kan være vrient på Windows

Litt om hvordan man får tak i Geopandas og øvrige bibliotek på Windows-plattform. 



## Linux med anaconda

Last ned siste [Anaconda versjon](https://www.anaconda.com/download/#linux) for python 3.6 eller høyere, installer med ```bash Anaconda*.sh```- [Mer detaljert oppskrift](https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-16-04). 

* Geopandas: Kluss med inkompatibilitet mellom hva Geopandas trenger og det som brukes default. 
  * ```conda config --add channels conda-forge``` (gir conda-forge høyest prioritet)
  * ```conda install -c conda-forge geopandas``` [Dokumentasjon](http://geopandas.org/install.html#installing-geopandas)
* Geojson ```conda install -c ioos geojson``` [Dokumentasjon](https://pypi.python.org/pypi/geojson)

## Linux uten anaconda

Antagelsen her er at du har python3 installert, men at din standard pythoninstallasjon er python 2.7.

* [Geopandas](http://geopandas.org/) ```pip3 install geopandas```
* [Geojson](https://pypi.python.org/pypi/geojson) ```pip3 install geojson```

Denne oppskriften er prøvd på [pythonanywhere](https://pythonanywhere.com). Med betalkonto ($5/mnd) har du tilgang til notebook. 

## Windows 

Last ned og installer siste [Anaconda versjon](https://www.anaconda.com/download) for python 3.6 eller høyere. Kjør installasjonen. 

**Todo: Skriv om bruk av windows-oppfinnelsen _anaconda prompt_ **

# Funker på SSM-linux
  
conda install -c conda-forge geopandas
conda install -c conda-forge geojson
conda install -c conda-forge mplleaflet
