from utils import *
import pandas as pd
import os
import math
import re
from unidecode import unidecode

def load_dcb_table_into_memory():
    """ Read dcb table and load into list """

    #creates a global variable to store DCB list of drugs. This variable will be used in 'search_in_dcb' method
    global meds_list_of_names
    meds_list_of_names = []

    print("Start Loading DCB... ")
    #gets list from file
    df_dcb = pd.read_excel(os.path.join("raw", "DCB_lista_completa_atualizada_em_marco_2016.xlsx"))
    med_column = df_dcb.columns[1]

    #Removes stranger chars from drugs' names
    m_list_of_names = [re.sub('[\(\)\{\}\[\]<>]', '',unidecode(item).strip()).upper() for item in df_dcb[med_column]]
    #sorting list of drugs
    m_list_of_names = sorted(m_list_of_names)

    #removes STOPWORDS for each drug name in list
    for med in m_list_of_names:
        meds_list_of_names.append(' '.join([word for word in med.split() if word not in STOPWORDS]))

    print("Finished.")

def check_equal(s1, s2):
    """ Checks if word are identical or fi one is abbreviation of another """
    if len(s1.split()) == 1 or len(s2.split())==1:
        return s1 == s2
    else:
        return is_abbrev(s1,s2)

def search_in_dcb(nameSearch):
    """ Search drug name in DCB table loaded into meds_list_of_names.
    This method searches a drug name in a list of sorted drugs' names using a binary search to do that.
    Starts in the middle of the list: if the name we are searhcing for isnt the middle element, the algorithm choose choose to go to the left or to the right
    of the middle element based on the alphabetical order. it does this recursively until the element is found or the list ends. """

    global meds_list_of_names

    lower_bound = 0
    upper_bound = len(meds_list_of_names)-1
    found_name = NOT_FOUND
    found = False
    while lower_bound <= upper_bound and not found:
        #get middle element in list
        middle_pos = (lower_bound+upper_bound) // 2
        #check if its equal or abbreviation of nameSearch
        if check_equal(nameSearch, meds_list_of_names[middle_pos]):
            found_name = meds_list_of_names[middle_pos]
            found = True
            with open(os.path.join("log", 'check_meds_names.csv'), 'a') as check_meds_names_file:
                check_meds_names_file.write("{}; {}\n".format(nameSearch, found_name))
        #check if nameSearch is lower or greater based on alphabetical order and choose to go up or down in the list to continue th search
        elif less_than(nameSearch, meds_list_of_names[middle_pos]):
            upper_bound = middle_pos - 1
        else:
            lower_bound = middle_pos + 1

    return found_name



def pre_processing_table(table_name, table_given_name, column_pres, column_prod, column_lab, column_code):
    """ Split table in csv files by drug name initial and processes atributtes to eliminate accent and remove stopwords"""
    print("Start Processing... " + table_name)
    #import the table file into a dataframe
    df_table = pd.read_excel(os.path.join("raw", table_name))

    #get the columns corresponding to each attibute
    pres = column_pres-1
    prod = column_prod-1
    lab = column_lab-1
    code = column_code-1

    #this for iterates in each row of the dataframe
    for index in range(len(df_table)):

        #get the lab of the current row
        lab_name = df_table.iloc[index,lab]
        #if there is no acronymn to the lab in table then the variable lab_name receives a NO_ACRONYMN value
        if lab_name == EMPTY_NAME or lab_name != lab_name:
            lab_name = NO_ACRONYMN

        #print(lab_name)
        #tranform the lab name to uppercase
        lab_name = lab_name.upper()

        #create the path to the lab directory iniside the data folder
        lab_dir_name = os.path.join(os.path.join("data", table_given_name), lab_name)

        #create the dir with path lab_dir_name if not exists
        if not os.path.exists(lab_dir_name):
            os.makedirs(lab_dir_name)

        #get the drug name of the current row
        prod_name = df_table.iloc[index,prod]
        #replace char in drug name
        prod_name_formatted = re.sub("[^\w]", " ", prod_name)
        #remove STOPWORDS fromm drug name
        prod_name_formatted = ' '.join([unidecode(word) for word in prod_name_formatted.split() if word not in STOPWORDS]).upper()
        #searche formatted drug name in dcb list of drugs. If the name it isnt found prod_name_complete receives NOT_FOUND flag
        prod_name_complete = search_in_dcb(prod_name_formatted)
        #get the first letter of current row drug name
        prod_initial = prod_name_formatted[0]
        #replace char in drug description
        prod_pres = unidecode(re.sub(",", ".", df_table.iloc[index,pres]))


        #create file with drug name initial, if not exists, and save the formatted data into it
        with open(os.path.join(lab_dir_name, prod_initial + '.csv'), 'a') as prod_initial_file:
            prod_initial_file.write("{}; {}; {}; {}; {}; {}\n".format(df_table.iloc[index,code], prod_name, prod_name_formatted, prod_name_complete, prod_pres,lab_name))
    print("Table Finished.")

def pre_processing_CATMAT_table(table_name, table_given_name, column_pres, column_prod, column_unit, column_vol, column_code):
    """ Split CATMAT table in csv files by drug name initial and processes atributtes to eliminate accent and remove stopwords"""
    print("Start Processing... " + table_name)
    #import the table file into a dataframe
    df_table = pd.read_excel(os.path.join("raw", table_name))

    #get the columns corresponding to each attibute
    pres = column_pres-1
    prod = column_prod-1
    unit = column_unit-1
    vol = column_vol-1
    code = column_code-1

    #create the path to the lab directory iniside the data folder
    table_dir_name = os.path.join("data", table_given_name)

    #create the dir with path lab_dir_name if not exists
    if not os.path.exists(table_dir_name):
        os.makedirs(table_dir_name)

    #this for iterates in each row of the dataframe
    for index in range(len(df_table)):

        #get the drug name of the current row
        prod_name = df_table.iloc[index,prod]
        #replace char in drug name
        prod_name_formatted = re.sub("[^\w]", " ", prod_name)
        #remove STOPWORDS fromm drug name
        prod_name_formatted = ' '.join([unidecode(word) for word in prod_name_formatted.split() if word not in STOPWORDS]).upper()
        #searche formatted drug name in dcb list of drugs. If the name it isnt found prod_name_complete receives NOT_FOUND flag
        prod_name_complete = search_in_dcb(prod_name_formatted)
        #get the first letter of current row drug name
        prod_initial = prod_name_formatted[0]
        #replace char in drug description
        prod_pres = unidecode(re.sub(",", ".", df_table.iloc[index,pres]))
        #get the unit in the current row
        prod_unit = df_table.iloc[index,unit]
        #get the volumn in the current row
        prod_vol = unidecode(re.sub(",", ".", str(df_table.iloc[index,vol])))
        #if unit is not empty append it into prod_pres
        if prod_unit:
            prod_pres = prod_pres + " " + prod_unit
        #if volumn is not empty append it into prod_pres
        if prod_vol and not prod_vol == "0":
            prod_pres = prod_pres + " " + prod_vol

        #creates file with drug name initial, if not exists, and save the formatted data into it
        with open(os.path.join(table_dir_name, prod_initial + '.csv'), 'a') as prod_initial_file:
            prod_initial_file.write("{}; {}; {}; {}; {}; {}\n".format(df_table.iloc[index,code], prod_name, prod_name_formatted, prod_name_complete, prod_pres ,NO_ACRONYMN))
    print("Table Finished.")

# def pre_processing_dcb_table():
#     print("Start Processing DCB... ")
#     df_dcb = pd.read_excel(os.path.join("raw", "DCB_lista_completa_atualizada_em_março_2016.xlsx"))
#
#     dcb_dir_name = os.path.join("data", "DCB")
#     if not os.path.exists(dcb_dir_name):
#         os.makedirs(dcb_dir_name)
#
#     for index in range(len(df_dcb)):
#         prod_complete_name = df_dcb.iloc[index,1].upper()
#         prod_complete_name_formatted = ' '.join([unidecode(word) for word in prod_complete_name.split() if word not in STOPWORDS])
#         prod_initials = prod_complete_name_formatted[0] + prod_complete_name_formatted[1]
#
#         with open(os.path.join(dcb_dir_name, prod_initials + '.csv'), 'a') as prod_initial_file:
#             prod_initial_file.write("{}, {}\n".format(prod_complete_name, prod_complete_name_formatted))
#
#     print("DCB Finished.")
