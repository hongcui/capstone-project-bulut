import numpy as np
import pandas as pd
from Levenshtein import ratio
import re

def get_location_similarity(lat1, long1, lat2, long2): # investigate distance methods between 2 locations
    NS1 = lat1[-1].lower()
    NS2 = lat2[-1].lower()
    WE1 = long1[-1].lower()
    WE2 = long2[-1].lower()
    lat1 = int(float(lat1[:-2]))
    long1 = int(float(long1[:-2]))
    lat2 = int(float(lat2[:-2]))
    long2 = int(float(long2[:-2]))
    if NS1 == NS2 and WE1 == WE2 and lat1 == lat2 and long1 == long2:
        return 1
    else:
        return 0
    
def is_common_item(l1, l2):
    common = False
    for el1 in l1:
        for el2 in l2:
            if el1.strip() == el2.strip():
                common = True
    return common

def get_author_overlap(ref1, sample_name1, ref2, sample_name2):
    if len(ref1.split(',')) != 2:
        print("Error, comma split did not work at ref1.")
        print(ref1.split(','))
        return -1 
    if len(ref2.split(',')) != 2:
        print("Error, comma split did not work at ref2.")
        print(ref2.split(','))
        return -1
    ref1 = ref1.split(',')[0] + ", " + ref1.split(',')[1]
    ref2 = ref2.split(',')[0] + ", " + ref2.split(',')[1]
    citation_num1 = None
    citation_num2 = None
    sample_name1_citations = dict_sample_name_citations[sample_name1]
    for citation_code, citation_num in sample_name1_citations:
        if citation_code == ref1:
            citation_num1 = int(citation_num)
    sample_name2_citations = dict_sample_name_citations[sample_name2]
    for citation_code, citation_num in sample_name2_citations:
        if citation_code == ref2:
            citation_num2 = int(citation_num)
    if not citation_num1:
        print("citation_num1 is None, meaning author is not in data: ", ref1)
        return -1
    if not citation_num2:
        print("citation_num2 is None, meaning author is not in data ", ref2)
        return -1
    authors1 = list(authors['authors'][authors['citation_num'] == citation_num1])[0].split(';')
    authors2 = list(authors['authors'][authors['citation_num'] == citation_num2])[0].split(';')
    
    if is_common_item(authors1, authors2):
        return 1
    else:
        return 0
    
def expand_matches_data(matches, df1, df2, same):
    for i, row in df1.iterrows():
        for j, row2 in df2.iterrows():
            if j>i:
                if row['Sample Name'] in dict_sample_name_citations.keys():
                    if row2['Sample Name'] in dict_sample_name_citations.keys():
                        matches['Reference1'].append(row['Reference'])
                        matches['Reference2'].append(row2['Reference'])
                        matches['Dataset1'].append(row['Dataset'])
                        matches['Dataset2'].append(row2['Dataset'])
                        matches['SampleNameSimilarity'].append(ratio(row['Sample Name'], row2['Sample Name']))
                        matches['LocationSimilarity'].append(get_location_similarity(row['Lat'], row['Long'], row2['Lat'], row2['Long']))
                        overlap = get_author_overlap(row['Reference'], row['Sample Name'], row2['Reference'], row2['Sample Name'])
                        if overlap != -1:
                            matches['AuthorOverlap'].append(overlap)
                        else:
                            continue
                        matches['Same'].append(same)
                    else:
                        print("sample name not found: ", row2['Sample Name'])
                        continue
                else:
                    print("sample name not found: ", row['Sample Name'])
                    break
    return matches

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
            same_matches = expand_matches_data(same_matches, df, df, 1)
        elif i_>i:
            df1 = same[j:k]
            df1.columns = same_columns
            df2 = same[j_:k_]
            df2.columns = same_columns
            same_matches = expand_matches_data(same_matches, df1, df2, 0)
        else:
            continue

different_columns = ['Reference', 'Dataset', 'PetDB Sample ID', 'Sample Name', 'Material', 'Taxon (rock class|rock type)', 'Tectonic Setting', 'Geolocation Names', 'Station Name', 'Lat', 'Long', 'Expedition/Cruise']

different_spans = [(6,10), (12,14), (16,18), (20,22), (25,27), (29,31), (34,36), (38,40), (42,44), (46,48)]
for i, (j,k) in enumerate(different_spans):
    for i_, (j_,k_) in enumerate(different_spans):
        if i == i_:
            df = different[j:k]
            df.columns = different_columns
            different_matches = expand_matches_data(different_matches, df, df, 0)
        else:
            continue


df_same_matches = pd.DataFrame(same_matches)
# df_different_matches = pd.DataFrame(different_matches)

print(df_same_matches)
df_same_matches.to_csv("./data/data.csv", index=False)








    