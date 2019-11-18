import zipfile
import argparse
import sys
import json
import re
import os
from markdown import markdown
from bs4 import BeautifulSoup
import ftfy
import pandas as pd


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
    zip_ = zipfile.ZipFile(args.zipfile)
    fnames = zip_.namelist()
    num_files = len(fnames)
    counter = 0
    print("Parsing job started..")
    for fname in fnames:
        counter += 1
        df = pd.DataFrame(
            columns=['doc_id', 'yle_id', 'url', 'published', 'text'])
        
        # Reading json data
        if not fname.endswith(".json"):
            print("Skipping file ", fname)
            continue
        with zip_.open(fname) as f:
            try:
                data = json.loads(f.read().decode("utf-8"))
            except json.decoder.JSONDecodeError:
                print("Error reading file, skipping ", fname)

        for article in data["data"]:
            # Metadata
            metadata = {
                'doc_id': counter,
                'yle_id': article["id"],
                'url': article["url"]["full"],
                'published': article["datePublished"]
            }

            # Article content
            for paragraph in article["content"]:
                # skip images etc.
                if paragraph["type"] not in ["text", "heading"]:
                    text = "N/A"
                    continue
                # 'text' = ['resource', {'id': '6385775'}]
                if paragraph["type"] == "heading" and isinstance(paragraph["text"], list):
                    text = "N/A"
                    print("skipped paragraph element", paragraph["text"])
                    continue
                text = paragraph["text"].strip()

                # slows down, but if there's no hurry then the text will be cleaner
                text = fix_encoding(text)
                text = clean_markdown(text)

            # Parsed data dictionary
            parsed_data = {
                **metadata,
                'text': text
            }
            df = df.append(parsed_data, ignore_index=True)

            # Making output directory
            try:
                output_fullpath = os.path.join(args.outputdir, fname)
                os.makedirs(os.path.dirname(output_fullpath), exist_ok=True)
                output_fullpath = os.path.splitext(output_fullpath)[0]+'.pkl'  # pkl extension for df files
            except Exception as e:
                print("Error creating output path!")
                print(e)

            # Saving dataframe as pickle
            df.to_pickle(output_fullpath)

        if counter % 5 == 0:
            print("Parsed {x}/{y} files..".format(x=counter, y=num_files))
    print("Finished parsing.")

if __name__ == "__main__":

    argparser = argparse.ArgumentParser(
        description='Yle news archive reader - parse archive data to Pandas dataframes')
    argparser.add_argument('--zipfile', default="./data/ylenews-fi-2011-2018-src.zip",
                           help='zipfile downloaded from kielipankki')
    argparser.add_argument('--outputdir', default="./data/parsed/",
                           help='output directory for parsed dataframes')
    args = argparser.parse_args()

    main(args)
