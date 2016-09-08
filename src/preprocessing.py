import pandas as pd
import os
import math
import re
from unidecode import unidecode
from abbrev import is_abbrev
from constants import *


def pre_processing_dcb_table():
    print("Start Processing DCB... ")
    df_dcb = pd.read_excel(os.path.join("raw", "DCB_lista_completa_atualizada_em_março_2016.xlsx"))

    dcb_dir_name = os.path.join("data", "DCB")
    if not os.path.exists(dcb_dir_name):
        os.makedirs(dcb_dir_name)

    for index in range(len(df_dcb)):
        prod_complete_name = df_dcb.iloc[index,1].upper()
        prod_complete_name_formatted = ' '.join([unidecode(word) for word in prod_complete_name.split() if word not in STOPWORDS])
        prod_initials = prod_complete_name_formatted[0] + prod_complete_name_formatted[1]

        with open(os.path.join(dcb_dir_name, prod_initials + '.csv'), 'a') as prod_initial_file:
            prod_initial_file.write("{}, {}\n".format(prod_complete_name, prod_complete_name_formatted))

    print("DCB Finished.")

def load_dcb_table_into_memory():
    global meds_list_of_names
    meds_list_of_names = []

    print("Start Loading DCB... ")
    df_dcb = pd.read_excel(os.path.join("raw", "DCB_lista_completa_atualizada_em_março_2016.xlsx"))
    med_column = df_dcb.columns[1]

    m_list_of_names = [re.sub('[\(\)\{\}\[\]<>]', '',unidecode(item).strip()).upper() for item in df_dcb[med_column]]
    m_list_of_names = sorted(m_list_of_names)
    for med in m_list_of_names:
        meds_list_of_names.append(' '.join([word for word in med.split() if word not in STOPWORDS]))

    print("Finished.")

def less_than(s1,s2):
    words_string1 = s1.split()
    words_string2 = s2.split()
    rank = min(len(words_string1),len(words_string2))
    for i in range(rank):
        if words_string1[i] in words_string2[i]:
            if i < rank - 1:
                return words_string1[i+1] < words_string2[i+1]
        else:
            break
    return s1 < s2

def check_equal(s1, s2):
    if len(s1.split()) == 1 or len(s2.split())==1:
        return s1 == s2
    else:
        return is_abbrev(s1,s2)

def find_in_dcb(nameSearch):
    global meds_list_of_names

    lower_bound = 0
    upper_bound = len(meds_list_of_names)-1
    found_name = NOT_FOUND
    found = False
    while lower_bound <= upper_bound and not found:
        middle_pos = (lower_bound+upper_bound) // 2

        if check_equal(nameSearch, meds_list_of_names[middle_pos]):
            found_name = meds_list_of_names[middle_pos]
            found = True
            with open(os.path.join("log", 'check_meds_names.csv'), 'a') as check_meds_names_file:
                check_meds_names_file.write("{}, {}\n".format(nameSearch, found_name))
        elif less_than(nameSearch, meds_list_of_names[middle_pos]):
            upper_bound = middle_pos - 1
        else:
            lower_bound = middle_pos + 1

    return found_name



def pre_processing_table(table_name, table_given_name, column_pres, column_prod, column_lab, column_code):
    print("Start Processing... " + table_name)
    df_table = pd.read_excel(os.path.join("raw", table_name))

    pres = column_pres-1
    prod = column_prod-1
    lab = column_lab-1
    code = column_code-1

    for index in range(len(df_table)):

        lab_name = df_table.iloc[index,lab]
        if lab_name == EMPTY_NAME or lab_name != lab_name:
            lab_name = NO_ACRONYMN

        lab_name = lab_name.upper()

        lab_dir_name = os.path.join(os.path.join("data", table_given_name), lab_name)

        if not os.path.exists(lab_dir_name):
            os.makedirs(lab_dir_name)

        prod_name = df_table.iloc[index,prod]
        prod_name_formatted = re.sub("[^\w]", " ", prod_name)
        prod_name_formatted = ' '.join([unidecode(word) for word in prod_name_formatted.split() if word not in STOPWORDS]).upper()
        prod_name_complete = find_in_dcb(prod_name_formatted)
        prod_initial = prod_name_formatted[0]
        prod_pres = unidecode(re.sub(",", ".", df_table.iloc[index,pres]))

        with open(os.path.join(lab_dir_name, prod_initial + '.csv'), 'a') as prod_initial_file:
            prod_initial_file.write("{}, {}, {}, {}, {}, {}\n".format(df_table.iloc[index,code], prod_name, prod_name_formatted, prod_name_complete, prod_pres,lab_name))
    print("Table Finished.")
