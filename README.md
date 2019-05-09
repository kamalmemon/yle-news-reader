# yle-news-reader
A python reader for processing yle-news archive (http://urn.fi/urn:nbn:fi:lb-2017070501)

Usage: `python3 yle_reader.py --zip ylenews-fi-2011-2018-src.zip | gzip -c > ylenews-fi-2011-2018-src.txt.gz`

Reads YLE json files from the zip, and returns plain text, where metadata lines are marked with `###C:`. Note that most of the metadata fields included in the original json are not preserved.

Example of output:
```
###C: doc_id = 1
###C: yle_id = 3-5315127
###C: url = http://yle.fi/uutiset/hpk_kaansi_lopulta_voiton_itselleen/5315127
###C: published = 2011-01-31T22:52:26+0200
###C: filename = ylenews-fi-2011-2018-src/data/fi/2011/01/0000.json
HPK käänsi lopulta voiton itselleen

Kahdeksas perättäinen voitto ja 2 sarjapistettä. Siinä HPK:n saldo naisten lentopalloliigan kamppailusta Liiga - Euraa vastaan, kun joukkue käänsi lopulta yleisöön menevän ottelun itselleen erin 3 - 2 (25-22 , 28-26 , 23-25 , 22-25 , 15-11).

Ennakkoasetelmat:

Illan ainoassa naisten lentopallon Mestaruusliigan kamppailussa kohtaavat...
```
