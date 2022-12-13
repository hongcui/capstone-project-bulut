import numpy as np
import pandas as pd
from Levenshtein import ratio
import re
from utilities import *


xls = pd.ExcelFile('iSamples Sets.xlsx')
same = pd.read_excel(xls, 'same')
different = pd.read_excel(xls, 'different')
authors = pd.read_csv("PetdbCitationsReferencingTheSameSpecimens.csv")
big_data = pd.read_csv("PetdbSpecimensGreaterThan1Citation-Corrected.csv")

dict_sample_name_citations = {}
for row in big_data.sample_names:
    all_citations_per_sample_name = re.findall(r'["].+?(?=})', row)
    for citations_per_sample_name in all_citations_per_sample_name:
        sample_name = re.findall(r'[^"]+[\^]', citations_per_sample_name)[0][:-1]
        if sample_name not in dict_sample_name_citations.keys():
            dict_sample_name_citations[sample_name] = []
        citations = re.findall(r'([\D][\\]["][\D]+.+?(?=\\))', citations_per_sample_name)
        for citation in citations:
            citation_code = citation.split('|')[0][3:]
            citation_num = citation.split('|')[1]
            dict_sample_name_citations[sample_name].append((citation_code, citation_num))

same_matches = { 'Reference1':[],
             'Dataset1':[],
             'Reference2':[],
             'Dataset2':[],
             'SampleNameSimilarity':[],
             'LocationSimilarity':[],
             'AuthorOverlap':[],
             'Same':[]}
different_matches = { 'Reference1':[],
             'Dataset1':[],
             'Reference2':[],
             'Dataset2':[],
             'SampleNameSimilarity':[],
             'LocationSimilarity':[],
             'AuthorOverlap':[],
             'Same':[]}

same_columns = ['Reference', 'Dataset', 'Sample Name', 'Material', 'Lat', 'Long', 'Taxon', 'Tectonic Setting', 'Country', 'Ocean', 'Expedition', 'Station']
same_spans = [(4,26), (30,35), (39,44), (47, 49), (53,78), (81,83), (86,88), (93,96), (98,100)]
for i, (j,k) in enumerate(same_spans):
    for i_, (j_,k_) in enumerate(same_spans):
        if i == i_:
            df = same[j:k]
            df.columns = same_columns
            same_matches = expand_matches_data(authors, dict_sample_name_citations, same_matches, df, df, 1)
        elif i_>i:
            df1 = same[j:k]
            df1.columns = same_columns
            df2 = same[j_:k_]
            df2.columns = same_columns
            same_matches = expand_matches_data(authors, dict_sample_name_citations, same_matches, df1, df2, 0)
        else:
            continue

different_columns = ['Reference', 'Dataset', 'PetDB Sample ID', 'Sample Name', 'Material', 'Taxon (rock class|rock type)', 'Tectonic Setting', 'Geolocation Names', 'Station Name', 'Lat', 'Long', 'Expedition/Cruise']

different_spans = [(6,10), (12,14), (16,18), (20,22), (25,27), (29,31), (34,36), (38,40), (42,44), (46,48)]
for i, (j,k) in enumerate(different_spans):
    for i_, (j_,k_) in enumerate(different_spans):
        if i == i_:
            df = different[j:k]
            df.columns = different_columns
            different_matches = expand_matches_data(authors, dict_sample_name_citations, different_matches, df, df, 0)
        else:
            continue

singles = {'sample_name':[], 'reference':[], 'lat':[], 'long':[]}

for (j,k) in same_spans:
    df = same[j:k]
    df.columns = same_columns
    for i, row in df.iterrows():
        if row['Sample Name'] not in dict_sample_name_citations.keys():
            continue
        singles['sample_name'].append(row['Sample Name'])
        singles['reference'].append(row['Reference'])
        singles['lat'].append(row['Lat'])
        singles['long'].append(row['Long'])


df_singles = pd.DataFrame(singles)
df_singles.to_csv("./data/singles.csv", index=False)

df_same_matches = pd.DataFrame(same_matches)
# df_different_matches = pd.DataFrame(different_matches)

df_same_matches.to_csv("./data/data.csv", index=False)








    