from utils import *
import pandas as pd
import os
import re
from unidecode import unidecode

#The functions in this file will be used to search for drugs matches

def search_drugs_names_matches(source1, source2):
    """ Read labs directory into lists and call method find_possible_matches to search for drugs matches. """

    #Get sources' dirs paths
    source1_path = os.path.join("data", source1)
    source2_path = os.path.join("data", source2)

    #Get list of labs' dirs in sources' dirs
    labs_src1 = [f.path for f in os.scandir(source1_path) if f.is_dir() ]
    labs_src2 = [f.path for f in os.scandir(source2_path) if f.is_dir() ]
    print(labs_src1)
    print(len(labs_src1))
    print(labs_src2)
    print(len(labs_src2))


    print("Start reading files...")
    #Comparing only folders of same labs in each source
    if len(labs_src1) > 0:
        for lab in labs_src1:
            if len(labs_src2) > 0:
                if lab in labs_src2:
                    print("Start reading lab dir... " + lab)
                    #Get list of files in labs' dirs
                    files_src1 = os.listdir(lab)
                    files_src2 = os.listdir(lab)
                    get_drugs_in_files(source1,lab, files_src1,source2, lab,files_src2)
            else:
                files_src1 = os.listdir(lab)
                files_src2 = os.listdir(source2_path)
                get_drugs_in_files(source1,lab, files_src1,source2, source2_path,files_src2)
    else:
        print("Start reading CATMAT dir... ")
        files_src1 = os.listdir(source1_path)
        if len(labs_src2) > 0:
            for lab in labs_src2:
                files_src2 = os.listdir(lab)
                get_drugs_in_files(source1,source1_path, files_src1,source2, lab,files_src2)
        else:
            files_src2 = os.listdir(source2_path)
            get_drugs_in_files(source1, source1_path, files_src1, source2, source2_path,files_src2)


def get_drugs_in_files(source1, source1_path, files_src1, source2, source2_path,files_src2):
        for filename in files_src1:
            if filename in files_src2:
                print("Start reading files... " + filename)
                #Open files of corresponding lab
                f1 = open(os.path.join(source1_path, filename), 'r',encoding='iso-8859-1')
                f2 = open(os.path.join(source2_path, filename), 'r',encoding='iso-8859-1')

                #Read file 1 into list drugs1
                drugs1 = []
                line = f1.readline()
                while(line != ''):
                    drugs1.append(line.split(';'))
                    line = f1.readline()

                #Read file 2 into list drugs2
                drugs2 = []
                line = f2.readline()
                while(line != ''):
                    drugs2.append(line.split(';'))
                    line = f2.readline()

                #Close files
                f1.close()
                f2.close()
                print("Files read.")

                #Tranforms list of lists in list of tuples then tranform list in set to eliminate duplicateds and returns to list again
                drugs1 = list(set(map(tuple, drugs1)))
                drugs2 = list(set(map(tuple, drugs2)))
                print("Trying to find matches for files... " + filename)
                #Call find_possible_matches to search drugs' matches by drug names
                find_possible_matches(drugs1, source1, drugs2, source2)
                print("Process finished for files... " + filename)


def find_possible_matches(drugs1, source1, drugs2, source2):
    """ Search drugs' matches comparing drugs' names"""
    matches = []
    no_matches = {}

    for drug in drugs1:

        try:
            #Get drug's attributes
            drug1_code = drug[PROD_CODE_INDEX]
            drug1_name = drug[PROD_NAME_FORMATTED_INDEX]
            drug1_initial = drug1_name.strip()[0]
            drug1_complete_name = drug[PROD_NAME_COMPLETE_INDEX]
            drug1_pres =  re.sub("\n", "",drug[PROD_PRES_INDEX])
            drug1_lab = re.sub("\n", "", drug[PROD_LAB_INDEX])
            if len(drug) > 6:
                drug1_unit = drug[PROD_UNIT_INDEX]
                drug1_vol = re.sub("\n", "", drug[PROD_VOL_INDEX])

            for possible_match in drugs2:
                matched = False
                if len(drug) > 6:
                    current_matches = [drug1_code, drug1_name, drug1_complete_name, drug1_pres, drug1_lab,drug1_unit,drug1_vol]
                else:
                    current_matches = [drug1_code, drug1_name, drug1_complete_name, drug1_pres, drug1_lab]


                #Get drug's attributes for possible match drug
                try:
                    drug2_code = possible_match[PROD_CODE_INDEX]
                    drug2_name = possible_match[PROD_NAME_FORMATTED_INDEX]
                    drug2_complete_name = possible_match[PROD_NAME_COMPLETE_INDEX]
                    drug2_pres =  re.sub("\n", "",possible_match[PROD_PRES_INDEX])
                    drug2_lab = re.sub("\n", "", possible_match[PROD_LAB_INDEX])
                    if len(possible_match) > 6:
                        drug2_unit = possible_match[PROD_UNIT_INDEX]
                        drug2_vol = re.sub("\n", "", possible_match[PROD_VOL_INDEX])
                except:
                    print(possible_match)
                #Check macth by drugs' names by calling any_abbrev utility method
                if NOT_FOUND in drug1_complete_name or NOT_FOUND in drug2_complete_name:
                    print("foi")
                    if any_abbrev(drug1_name, drug2_name):
                        print("ok")
                        if len(drug) > 6:
                            current_matches = current_matches + [drug2_code, drug2_name, drug2_complete_name ,drug2_pres, drug2_lab,drug2_unit,drug2_vol]
                        else:
                            current_matches = current_matches + [drug2_code, drug2_name, drug2_complete_name ,drug2_pres, drug2_lab]
                        matched = True

                else:
                    print("foi2")
                    #Check macth by drugs' names by  comparing if drugs' names are identical
                    if drug1_complete_name ==  drug2_complete_name:
                        print("ok2")
                        print(drug1_complete_name)
                        print(drug2_complete_name)
                        print("complete names verifyied.")
                        current_matches = current_matches + list(possible_match)
                        matched = True

                if matched:
                    matches.append(current_matches)
                else:
                    if drug1_initial in no_matches.keys():
                        current = no_matches[drug1_initial]
                        current.append(drug)
                        no_matches[drug1_initial] = current
                    else:
                        no_matches[drug1_initial] = [drug]
        except:
            print(drug)


    print( str(len(no_matches.values())) + " no matches found.")
    print(str(len(matches)) + " matches found.")

    # Store no matches and macthes quantities
    with open(os.path.join("log", 'no_matches_stats_'+ source1 + '_'+ source2 + '_'+'.csv'), 'a') as stats_file:
        stats_file.write("{}\n".format(len(no_matches.values())))
    with open(os.path.join("log", 'matches_stats_'+ source1 + '_'+ source2 + '_'+'.csv'), 'a') as stats_file:
        stats_file.write("{}\n".format(len(matches)))

    #Store attributes of drugs that didnt match by name
    for key in no_matches.keys():
        with open(os.path.join("no_matches", key + '.csv'), 'a') as no_matches_file:
            for no_match in list(set(no_matches[key])):
                no_match = list(no_match)
                last_item = len(no_match) - 1
                for item in no_match[:last_item]:
                    no_matches_file.write("{};".format(item))
                no_matches_file.write("{}\n".format(no_match[last_item]))
    print("No matches saved.")

    #Store attributes of drugs that matched by name
    with open(os.path.join("matches", 'matches_'+ source1 + '_'+ source2 +'.csv'), 'a') as matches_file:
        for match in matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                matches_file.write("{};".format(item))
            matches_file.write("{}\n".format(match[last_item]))

    print("Matches saved.")

def search_drugs_presentation_matches(source1, source2):
    """ Search drugs' matches comparing drugs' presentation description"""

    #Open and read file that contais drugs matched by name
    matches_file = open(os.path.join( "matches", 'matches_'+ source1 + '_'+ source2 +'.csv'), 'r')
    possible_matches = []
    line = matches_file.readline()
    while(line != ''):
        possible_matches.append(line.split(';'))
        line = matches_file.readline()
    matches_file.close()

    #Tranforms list of lists in list of tuples then tranform list in set to eliminate duplicateds and returns to list again
    possible_matches = list(set(map(tuple, possible_matches)))

    matches = []
    no_matches = []

    #Get possible matches by name, check their digits patterns using utility method called check_digits_pattern and compare results
    for match in possible_matches:
        try:
            drug1_pres = match[PM_PROD_PRES_INDEX_1]
            drug1_pres_units = check_digits_pattern(drug1_pres)
            drug2_pres = match[PM_PROD_PRES_INDEX_2]
            drug2_pres_units = check_digits_pattern(drug2_pres)
            if compare_lists(drug1_pres_units, drug2_pres_units):
                matches.append(match)
            else:
                no_matches.append(match)
        except:
            print(match)

    #Store attributes of drugs that matched by presentation description
    with open(os.path.join("matches", 'matches_pres_'+ source1 + '_'+ source2 + '_'+'.csv'), 'a') as matches_file:
        for match in matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                matches_file.write("{};".format(item))
            matches_file.write("{}".format(match[last_item]))
    print("Matches by Pres saved.")

    #Store attributes of drugs that didnt match by presentation description
    with open(os.path.join("log", 'no_matches_pres_'+ source1 + '_'+ source2 + '_'+'.csv'), 'a') as no_matches_file:
        for match in no_matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                no_matches_file.write("{};".format(item))
            no_matches_file.write("{}".format(match[last_item]))
    print("No Matches by Pres saved.")


def classify_de_para_ims_sammed():

    df_de_para_ims_sammed = pd.read_excel(os.path.join("raw", "De_Para_IMS_SAMMED_FORMATADA.xlsx"))

    lab1_column = df_de_para_ims_sammed.columns[0]
    prod1_name_column = df_de_para_ims_sammed.columns[1]
    apr1_column = df_de_para_ims_sammed.columns[2]
    cod_ggrem_column = df_de_para_ims_sammed.columns[3]
    valido_column = df_de_para_ims_sammed.columns[4]
    expr1007_column = df_de_para_ims_sammed.columns[5]
    cod_pro_column = df_de_para_ims_sammed.columns[6]
    cod_ims_column = df_de_para_ims_sammed.columns[7]
    cod_fcc_column = df_de_para_ims_sammed.columns[8]
    lab2_column = df_de_para_ims_sammed.columns[9]
    prod2_name_column = df_de_para_ims_sammed.columns[10]
    apr2_column = df_de_para_ims_sammed.columns[11]
    qtd13_column = df_de_para_ims_sammed.columns[12]
    fat13_column = df_de_para_ims_sammed.columns[13]

    no_matches = []
    matches = []

    for ix in range(len(df_de_para_ims_sammed[prod1_name_column])):


        lab1 = df_de_para_ims_sammed[lab1_column][ix]
        prod1_name = df_de_para_ims_sammed[prod1_name_column][ix]
        apr1 = df_de_para_ims_sammed[apr1_column][ix]
        cod_ggrem = df_de_para_ims_sammed[cod_ggrem_column][ix]
        valido = df_de_para_ims_sammed[valido_column][ix]
        expr1007 = df_de_para_ims_sammed[expr1007_column][ix]
        cod_pro = df_de_para_ims_sammed[cod_pro_column][ix]
        cod_ims = df_de_para_ims_sammed[cod_ims_column][ix]
        cod_fcc = df_de_para_ims_sammed[cod_fcc_column][ix]
        lab2 = df_de_para_ims_sammed[lab2_column][ix]
        prod2_name = df_de_para_ims_sammed[prod2_name_column][ix]
        apr2 =  df_de_para_ims_sammed[apr2_column][ix]
        qtd13 =  df_de_para_ims_sammed[qtd13_column][ix]
        fat13 =  df_de_para_ims_sammed[fat13_column][ix]

        current_matches = [lab1, prod1_name, apr1, cod_ggrem, valido, expr1007, cod_pro, cod_ims]

        #Check macth by drugs' names by calling any_abbrev utility method or comparing if drugs' names are identical
        if any_abbrev(prod1_name, prod2_name) or prod1_name ==  prod2_name:
            current_matches = current_matches + [cod_fcc, lab2, prod2_name, apr2, qtd13, fat13]

        if len(current_matches) > 8:
            matches.append(current_matches)
        else:
            no_matches.append(current_matches)

    #Store attributes of drugs that matched by name
    with open(os.path.join("matches", 'matches_de_para_ims_sammed.csv'), 'a') as matches_file:
        for match in matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                matches_file.write("\"{}\",".format(item))
            matches_file.write("\"{}\"\n".format(match[last_item]))

    print("Matches saved.")

    #Store attributes of drugs that matched by name
    with open(os.path.join("no_matches", 'no_matches_de_para_ims_sammed.csv'), 'a') as no_matches_file:
        for match in no_matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                no_matches_file.write("\"{}\",".format(item))
            no_matches_file.write("\"{}\"\n".format(match[last_item]))

    print("No Matches saved.")
