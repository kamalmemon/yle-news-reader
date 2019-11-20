""" Loads each dataframe pickle and concats into a combined dataframe """

import pandas as pd
import os

def _get_all_files(directory, extension='.pkl'):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(directory):
        for file in f:
            if '.pkl' in file:
                files.append(os.path.join(r, file))
    return files

def concat_dataframes(directory, filter_wild_card='2011'):
    df_pickle_files =  _get_all_files(directory)
    # Filtering filenames
    df_pickle_files = list(filter(lambda f: filter_wild_card in f,
                                  df_pickle_files))
    # Concatting dataframes
    df = pd.concat([pd.read_pickle(fname) for fname in df_pickle_files])
    
    # Dropping duplicate texts
    df.drop_duplicates('text', inplace=True)
    
    # Removing multiple texts
    #counts = df.text.value_counts()
    #df = df.loc[df.text.isin(counts[counts < 2].index), :]
    
    return df