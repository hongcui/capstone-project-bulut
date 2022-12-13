import numpy as np
import pandas as pd
from xgboost import XGBClassifier
import re
from Levenshtein import ratio
from utilities import *

singles = pd.read_csv('./data/singles.csv')
authors = pd.read_csv("PetdbCitationsReferencingTheSameSpecimens.csv")
big_data = pd.read_csv("PetdbSpecimensGreaterThan1Citation-Corrected.csv")
new_samples = pd.read_csv("PetDBSpecimenData.csv")

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

model = XGBClassifier()
model.load_model("./saved-models/xgb_model.json")
n = 10
for i, row_new in new_samples.iterrows():
    matches = { 'SampleNameSimilarity':[],
            'LocationSimilarity':[],
            'AuthorOverlap':[]}
    is_matched = False
    new_sample_name = row_new['specimen_name']
    new_sample_reference = row_new['citation_code']
    if extract_lat_and_long(row_new['geometry_text']) != -1:
        new_sample_lat, new_sample_long = extract_lat_and_long(row_new['geometry_text'])
    else:
        continue
    for j,row in singles.iterrows():
        overlap = get_author_overlap(authors, dict_sample_name_citations, row['reference'], row['sample_name'], new_sample_reference, new_sample_name)
        if overlap == -1:
            break
        elif overlap == -2:
            continue
        else:
            matches['AuthorOverlap'].append(overlap)
        matches['SampleNameSimilarity'].append(ratio(row['sample_name'], new_sample_name))
        matches['LocationSimilarity'].append(get_location_similarity(row['lat'], row['long'], new_sample_lat, new_sample_long)) # for future use: we can set a threshold and not consider any sample that is too far away from the new sample so that the inference can be more efficient
        is_matched = True
    if is_matched:
        features_inference = pd.DataFrame(matches)
        probs = model.predict_proba(features_inference)
        similarity_scores = probs[:,1]
        best_n = np.argsort(-similarity_scores)[:n]
        for i in best_n:
            print(singles.loc[[i]])
        break







