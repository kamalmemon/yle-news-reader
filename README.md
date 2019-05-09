# yle-news-reader
A python reader for processing yle-news archive (http://urn.fi/urn:nbn:fi:lb-2017070501)

Usage: `python3 yle_reader.py --zip ylenews-fi-2011-2018-src.zip | gzip -c > ylenews-fi-2011-2018-src.txt.gz`

Reads YLE json files from the zip, and returns plain text, where metadata lines are marked with `###C:`. Note that most of the metadata fields included in the original json are not preserved.

Example of the output:
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

Can be further processed with Turku-neural-parser-pipeline (https://github.com/TurkuNLP/Turku-neural-parser-pipeline) to include tokenization, sentence splitting, lemmatization, tagging and parsing.

Example:
```
# doc_id = 1
# yle_id = 3-5315127
# url = http://yle.fi/uutiset/hpk_kaansi_lopulta_voiton_itselleen/5315127
# published = 2011-01-31T22:52:26+0200
# filename = ylenews-fi-2011-2018-src/data/fi/2011/01/0000.json
# newdoc
# newpar
# sent_id = 1
# text = HPK käänsi lopulta voiton itselleen
1       HPK     HPK     PROPN   N       Case=Nom|Number=Sing    2       nsubj   _       _
2       käänsi  kääntää VERB    V       Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act 0       root    _       _
3       lopulta lopulta ADV     Adv     _       2       advmod  _       _
4       voiton  voitto  NOUN    N       Case=Gen|Number=Sing    2       obj     _       _
5       itselleen       itse    PRON    Pron    Case=All|Number=Sing|Person[psor]=3|Reflex=Yes  2       obl     _       SpacesAfter=\n\n

# newpar
# sent_id = 2
# text = Kahdeksas perättäinen voitto ja 2 sarjapistettä.
1       Kahdeksas       kahdeksas       ADJ     Num     Case=Nom|Number=Sing|NumType=Ord        3       nummod  _       _
2       perättäinen     perättäinen     ADJ     A       Case=Nom|Degree=Pos|Derivation=Inen|Number=Sing 3       amod    _       _
3       voitto  voitto  NOUN    N       Case=Nom|Number=Sing    0       root    _       _
4       ja      ja      CCONJ   C       _       6       cc      _       _
5       2       2       NUM     Num     NumType=Card    6       nummod  _       _
6       sarjapistettä   sarja#piste     NOUN    N       Case=Par|Number=Sing    3       conj    _       SpaceAfter=No
7       .       .       PUNCT   Punct   _       3       punct   _       _
...
```
