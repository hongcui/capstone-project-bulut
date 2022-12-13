from Levenshtein import ratio
import re

def extract_lat_and_long(point):
    if point.startswith('LINESTRING'): # we do not know how to handle linestring positions yet
        return -1
    point = re.findall(r'[(][\S\s]+[)]', point)[0][1:-1] # i.e. get -43.7 11 from POINT(-43.7 11)
    latitude = float(point.split(' ')[0])
    longtitude = float(point.split(' ')[1])
    dir_lat = 'N'
    dir_long = 'E'
    if latitude < 0:
        dir_lat = 'S'
        latitude = abs(latitude)
    if longtitude < 0:
        dir_long = 'W'
        longtitude = abs(longtitude)
    str_lat = str(latitude) + ' ' + dir_lat
    str_long = str(longtitude) + ' ' + dir_long
    return str_lat, str_long

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

def get_author_overlap(authors, dict_sample_name_citations, ref1, sample_name1, ref2, sample_name2):
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
    if sample_name1 not in dict_sample_name_citations.keys():
        #print("sample_name1 is not in big data file: ", sample_name1)
        return -1
    sample_name1_citations = dict_sample_name_citations[sample_name1]
    for citation_code, citation_num in sample_name1_citations:
        if citation_code == ref1:
            citation_num1 = int(citation_num)
    if sample_name2 not in dict_sample_name_citations.keys():
        #print("sample_name2 is not in big data file: ", sample_name2)
        return -2
    sample_name2_citations = dict_sample_name_citations[sample_name2]
    for citation_code, citation_num in sample_name2_citations:
        if citation_code == ref2:
            citation_num2 = int(citation_num)
    if not citation_num1:
        #print("citation_num1 is None, meaning author is not in big data file: ", ref1)
        return -1
    if not citation_num2:
        #print("citation_num2 is None, meaning author is not in big data file:", ref2)
        return -2
    authors1 = list(authors['authors'][authors['citation_num'] == citation_num1])[0].split(';')
    authors2 = list(authors['authors'][authors['citation_num'] == citation_num2])[0].split(';')
    
    if is_common_item(authors1, authors2):
        return 1
    else:
        return 0
    
def expand_matches_data(authors, dict_sample_name_citations, matches, df1, df2, same):
    for i, row in df1.iterrows():
        for j, row2 in df2.iterrows():
            if j>i:
                if row['Sample Name'] in dict_sample_name_citations.keys():
                    if row2['Sample Name'] in dict_sample_name_citations.keys():
                        overlap = get_author_overlap(authors, dict_sample_name_citations, row['Reference'], row['Sample Name'], row2['Reference'], row2['Sample Name'])
                        if overlap == -1:
                            break
                        elif overlap == -2:
                            continue
                        else:
                            matches['AuthorOverlap'].append(overlap)
                        matches['Reference1'].append(row['Reference'])
                        matches['Reference2'].append(row2['Reference'])
                        matches['Dataset1'].append(row['Dataset'])
                        matches['Dataset2'].append(row2['Dataset'])
                        matches['SampleNameSimilarity'].append(ratio(row['Sample Name'], row2['Sample Name']))
                        matches['LocationSimilarity'].append(get_location_similarity(row['Lat'], row['Long'], row2['Lat'], row2['Long']))
                        matches['Same'].append(same)
                    else:
                        continue
                else:
                    break
    return matches