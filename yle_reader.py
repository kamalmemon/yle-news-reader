import zipfile
import argparse
import sys
import json
import re
from markdown import markdown
from bs4 import BeautifulSoup
import ftfy


def fix_encoding(text):
    # MOT: Eduskunnan rahareik&auml;\r\ntoimittaja Tero Koskinen\r\nensil&auml;h. 24.1.2011

    return ftfy.fix_text(text, uncurl_quotes=False)

def clean_markdown(text):
    # [Keskisuomalaisen](http://www.ksml.fi/kiekko/uutiset/sopanen-palaa-pelicansiin-jyp-ei-hankkinut-uusia-pelaajia/641867) mukaan JYP-hyökkääjä
    # kosketinsoittaja **Janne** toivoisi

    html = markdown(text)
    text = ''.join(BeautifulSoup(html, features="lxml").findAll(text=True))
    return text


def main(args):
    zip_=zipfile.ZipFile(args.zipfile)
    fnames = zip_.namelist()
    counter = 0
    for fname in fnames:
        if not fname.endswith(".json"):
            print("Skipping file", fname, file=sys.stderr)
            continue
        with zip_.open(fname) as f:
            try:
                data = json.loads(f.read().decode("utf-8"))
            except json.decoder.JSONDecodeError:
                print("Error reading file, skipping", fname, file=sys.stderr)
        for article in data["data"]:
            counter += 1

            # Add metadata
            print("###C: doc_id =", counter)
            print("###C: yle_id =", article["id"])
            print("###C: url =", article["url"]["full"])
            print("###C: published =", article["datePublished"])
            print("###C: filename =", fname)

            # Article content
            for paragraph in article["content"]:
                if paragraph["type"] not in ["text", "heading"]: # skip images etc.
                    continue
                if paragraph["type"] == "heading" and isinstance(paragraph["text"], list): # 'text' = ['resource', {'id': '6385775'}]
                    print("skipped paragraph element", paragraph["text"], file=sys.stderr)
                    continue
                text = paragraph["text"].strip()

                # slows down, but if there's no hurry then the text will be cleaner
                text = fix_encoding(text)
                text = clean_markdown(text)


                print(text)
                print("")

            if counter%10000==0:
                print("Seen {x} files.".format(x=counter), file=sys.stderr)




if __name__=="__main__":

    argparser = argparse.ArgumentParser(description='Yle news archive reader')
    argparser.add_argument('--zipfile', default="/usr/share/ParseBank/YLE/ylenews-fi-2011-2018-src.zip", help='zipfile downloaded from kielipankki')
    argparser.add_argument('--lang', default="fi", help='langauge, fi/sv (currently not used, code only tested with the finnish json)')
    args = argparser.parse_args()

    main(args)
