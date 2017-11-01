# -*- coding: utf-8 -*-
"""Dette er en nedstrippet versjon av notebook Geopandas-nvdb-eksempel.ipynb

    Jeg har kommentert ut all interaktiv plotting samt notebook-spesifikke 
    visning av resultater (for eksempel visning av kolonner fra DataFrames)
    
    Selve analysen med spatial joins kjøres som normalt

"""

# # Bruk av geopandas med data fra NVDB og SSB
# 
# Demo av hvordan geopandas kan brukes med data fra [Nasjonal vegdatabank](https://www.vegvesen.no/fag/teknologi/Nasjonal+vegdatabank) (NVDB) og [Statistisk Sentralbyrå](http://www.ssb.no/natur-og-miljo/geodata) (SSB). 
# 
# Vi ønsker å finne hvilke turistveger som går gjennom hvilke tettsteder - og hvilke trafikkulykker som er registrert der. 
# 
# Gangen er som følger: 
# 1. [Installasjon](installasjon.md) 
# 1. Last ned data over tettsteder fra [SSB](http://www.ssb.no/natur-og-miljo/geodata
# 1. Last ned turistveger fra [NVDB api](https://www.vegvesen.no/nvdb/apidokumentasjon/)
# 1. Finn snittet av turistveger og tettsteder (hvilke turistveger som går gjennom hvilke tettsteder)
# 1. Last ned trafikkulykker på turistvegene  
#     1. Vi bruker NVDB api'ets [overlappfilter](https://www.vegvesen.no/nvdb/apidokumentasjon/#/parameter/overlappfilter)
# 1. Finn snittet av trafikkulykker mot tettsteder med turistveger.
# 

# ## [Installasjon](installasjon.md) 
# 
# [Installasjon](installasjon.md) 
# 
# ## Importer de bibliotekene som trengs

# In[1]:

# Fine plott og sånn
#get_ipython().magic('matplotlib notebook')
#import matplotlib.pylab as pylab
#import matplotlib.pyplot as plt


# For nedlasting fra SSB
import requests
import zipfile
import io
import os

# For å hente data fra NVDB api 
import nvdbapi      # Fra https://github.com/LtGlahn/nvdbapi-V2
import nvdb2geojson # Fra https://github.com/LtGlahn/nvdbapi-V2

# For datakverning og analyse
import geopandas as gpd
import pandas as pd


# 
# # Last ned data fra SSB

# In[2]:

# Se https://stackoverflow.com/a/14260592 , det om python 3+

url = 'http://www.ssb.no/natur-og-miljo/_attachment/286736?_ts=158d3354ee0'

# Laster kun en gang: 
if not os.path.exists('Tettsted2016/Tettsted2016.shp'):
    r = requests.get(url)
    if r.ok: 
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
    else: 
        print( "Nedlasting feiler:", r.status_code, r.reason )


# ### Hent SSB-data manuelt 
# 
# Dette steget kan også gjøres manuelt. Direkte lenke for nedlasting av 2016-datasett er http://www.ssb.no/natur-og-miljo/_attachment/286736?_ts=158d3354ee0 
# 
# *NB! Det vil ikke overraske meg om lenkeråte gjør at du uansett må inn på SSB og finne nedlastingslenker* 
# 
# #### Finn lenke til nedlasting på SSB's nettsider
# 
# 1. Gå inn på http://www.ssb.no/natur-og-miljo/geodata#Nedlasting_av_datasett_med_dynamiske_avgrensinger . 
# 1. Klikk på *Nedlasting av kart over tettsteder*. 
# 1. Klikk på det året du vil laste ned for. 
#     1. Nedlasting skal starte automagisk... hvis ikke kan du prøve en annen nettleser, evt kopiere lenken og bruke verktøy som curl eller wget. 
# 1. Pakk ut zip-arkivet og legg mappen ```Tettsted2016``` sammen med øvrige filer (rotnivå i repos'et). Dvs at stien til shapefilen skal være ```Tettsted2016/Tettsted2016.shp```
# 
# ### Les tettsted inn i geodata-frame 
# 
# Vi leser tettstedene inn i geodata-frame og knar litt på dem. 

# In[3]:

# Les inn tettsted i geodata-frame
tettsted = gpd.read_file( 'Tettsted2016/Tettsted2016.shp')

# Hvilke egenskaper (kolonner) har vi? 
# tettsted.columns


# In[24]:

# tettsted.describe()


# Bortsett fra kolonnen _geometry_ så er dette en vanlig pandas dataframe. 
# 
# La oss kna litt mer. Hva er f.eks. forholdet mellom areal og folketall? La oss plotte det

# In[4]:

#fig2, ax2 = plt.subplots()
#ax2.set_title( "Areal vs folketall, tettsted")
#ax2.set_xlabel( 'Areal (km^2)')
#ax2.set_ylabel( 'Folketall')
#ax2.plot( tettsted.Areal_km2, tettsted.Tot_Bef, '.g' );
#fig2.tight_layout();


# Interessant.La oss se på hva som særpreger tettsteder større enn 50 km${}^2$. 

# In[5]:

#tettsted[ tettsted.Areal_km2 > 50].sort_values('Areal_km2', ascending=False )


# Dette er storbyene våre. Hvem er de minste tettstedene? 

# In[25]:

#tettsted.sort_values('Areal_km2' ).head()


# # Les data fra Nasjonal vegdatabank

# In[6]:

turistveger = nvdbapi.nvdbFagdata(777)
turistveger_geojson = nvdb2geojson.fagdata2geojson( turistveger)
turist2 = gpd.GeoDataFrame.from_features( turistveger_geojson['features'])


# # Finn turistveger i tettsteder 
# 
# http://geopandas.org/mergingdata.html , spatial joins. Først må vi sette 
# koordinatsystem. Merk at du bygger koordinatsystem i geopandas med linje kode. 
# http://geopandas.org/projections.html#re-projecting 
# 
# 

# In[8]:

tettsted.crs = {'init': 'epsg:25833'}
turist2.crs = {'init': 'epsg:25833'}

turist_i_tettsted = gpd.sjoin( turist2, tettsted, how='inner', op='intersects')
tettsted_m_turist = gpd.sjoin( tettsted, turist2, how='inner', op='intersects')


# _Hvis du her får en kryptisk **RuntimeWarning**- advarsel over så kan du trygt ignorere det. Eldre versjoner av programvaren gir divisjon med 0 når vi ikke får treff på "join" - operasjonen._ Gjelder f.eks. min windows anaconda-installasjon, men ikke linux. 
# 
# La oss sjekke hvor mange vi fant: 

# In[9]:

print( "Antall segmenter med turistveger", len( turist2))
print( "Antall tettsteder", len(tettsted))
print( "Tettsteder med turistveger", len(tettsted_m_turist), "Med  DUPLIKATER?")
print( "Turistveger som går gjennom tettsteder", len(turist_i_tettsted))


# Våre 17 turistveger er splittet opp i 527 korte segmenter - og overgangen mellom segmentene er ofte i vegkryss, dvs vi har typisk mer enn ett turistveg-segment per tettsted. Det gir duplikater som må fjernes fra datasettet _tettsteder med turistveger_

# In[10]:

tettsted_m_turist.drop_duplicates( subset='TETTNR', inplace=True)
print( "Tettsteder med turistveger", len(tettsted_m_turist), "UTEN duplikater")


# # Finner trafikkulykker på turistveger
# 
# Bruker NVDB api's overlappfilter https://www.vegvesen.no/nvdb/apidokumentasjon/#/parameter/overlappfilter 
# 

# In[11]:

ulykker = nvdbapi.nvdbFagdata( 570)
ulykker.addfilter_overlapp( '777'  )
print( 'Antall ulykker på turistveger', ulykker.statistikk()) 


# ### Gjør om ulykkene til geodataframe
# 
# Vi gjør om data fra NVDB api til geojson-objekter, som så leses direkte inn i geopdandas-dataFrame. 

# In[12]:

ulykker_geojson = nvdb2geojson.fagdata2geojson( ulykker)
ulykker_gpd = gpd.GeoDataFrame.from_features( ulykker_geojson['features']);


# ### Hvor mange av disse trafikkulykkene er i tettsteder? 

# In[13]:

ulykker_gpd.crs = {'init': 'epsg:25833'}
# Spatial join gir kolonnene 'index_right' og 'index_left'. Disse må slettes eller døpes om 
# før resultatet fra spatial join brukes i nye joins
tettsted_m_turist.rename( columns={ 'index_right' : 'tettsted_m_turist_indeks_right'}, inplace=True)
ulykker_i_tettsted = gpd.sjoin( ulykker_gpd, tettsted_m_turist, how='inner', op='intersects')
print( len(ulykker_i_tettsted), "ulykker på turistveger gjennom tettsteder") 


# #### Hvor mange tettsteder med turistveger har trafikkulykker? 

# In[26]:

tettsted_m_turistveg_ulykker = gpd.sjoin( tettsted_m_turist, ulykker_gpd, 
                                         how='inner', op='intersects' ) 

# Fjerner duplikater
tettsted_m_turistveg_ulykker.drop_duplicates( subset='TETTNR', inplace=True)

print( len(tettsted_m_turistveg_ulykker), "tettsteder har turistveger med ulykker")


# #### Alvorligste skadegrad?

# In[35]:

#ulykker_i_tettsted['Alvorligste skadegrad'].value_counts()


# #### Vi plotter litt
# 
# La oss plotte tettstedet Granvin (gul flate) med turistveg (blå linje) og 
# trafikkulykker (røde prikker)

# In[37]:

vistettsted = 'Granvin'
#fig1, ax1 = plt.subplots()
#
#ax1.set_title( "Ulykker på turistveg, " + vistettsted)
#ax1.set_ylabel( 'Nord utm33-meter')
#ax1.set_xlabel( 'Øst utm33-meter')
#ax1.set_aspect('equal')
#
#tettsted_m_turistveg_ulykker[ tettsted_m_turistveg_ulykker.Tettstedsn == 
#        vistettsted ].geometry.plot( ax=ax1, color='y', edgecolor='g')
#
#turist_i_tettsted[ turist_i_tettsted.Tettstedsn == 
#                  vistettsted].geometry.plot( ax=ax1, color='b');
#
#ulykker_i_tettsted[ ulykker_i_tettsted.Tettstedsn == 
#                vistettsted].geometry.plot( ax=ax1, color='r', markersize = 10);
#
#
## La oss granske detaljene for ulykkene i Granvin. 
## 
## Vi har ganske mange egenskapsverdier (totalt 78 kolonner). Med horisontal scrolling får vi vist alle hvis vi insisterer. 
#
## In[28]:
#
#pd.options.display.max_columns = 100
#ulykker_i_tettsted[ ulykker_i_tettsted.Tettstedsn == vistettsted]


# #### Dumper tettsted-ulykkene til geojson
# 
# Geojson er per definisjon lengde/breddegrad, så da må vi reprojisere. http://geopandas.org/projections.html#re-projecting 

# In[34]:

datadump = ulykker_i_tettsted.to_crs( { 'init' : 'epsg:4326' } )

with open('ulykker_i_tettsted.geojson', 'w') as f:
    f.write(datadump.to_json())
    
print( "Datadump CRS", datadump.crs, "ulykker CRS", ulykker_i_tettsted.crs)

