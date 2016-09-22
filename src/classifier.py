from utils import *
import pandas as pd
import os
import re

#The functions in this file will be used to search for drugs matches

def search_drugs_names_matches(source1, source2):
    """ Read labs directory into lists and call method find_possible_matches to search for drugs matches. """

    #Get sources' dirs paths
    source1_path = os.path.join("data", source1)
    source2_path = os.path.join("data", source2)

    #Get list of labs' dirs in sources' dirs
    labs_src1 = os.listdir(source1_path)[1:]
    labs_src2 = os.listdir(source2_path)[1:]


    print("Start reading files...")
    #Comparing only folders of same labs in each source
    for lab in labs_src1:
        if lab in labs_src2:
            print("Start reading lab dir... " + lab)
            #Get list of files in labs' dirs
            files_src1 = os.listdir(os.path.join(source1_path, lab))
            files_src2 = os.listdir(os.path.join(source2_path, lab))

            for filename in files_src1:
                if filename in files_src2:
                    print("Start reading files... " + filename)
                    #Open files of corresponding lab
                    f1 = open(os.path.join(os.path.join(source1_path, lab), filename), 'r',encoding='iso-8859-1')
                    f2 = open(os.path.join(os.path.join(source2_path, lab), filename), 'r',encoding='iso-8859-1')

                    #Read file 1 into list drugs1
                    drugs1 = []
                    line = f1.readline()
                    while(line != ''):
                        drugs1.append(line.split(','))
                        line = f1.readline()

                    #Read file 2 into list drugs2
                    drugs2 = []
                    line = f2.readline()
                    while(line != ''):
                        drugs2.append(line.split(','))
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
                    find_possible_matches(drugs1, drugs2)
                    print("Process finished for files... " + filename)

    #Comparing drugs in folder no_matches with all_labs
    for lab in labs_src2:
        files_src1 = os.listdir("no_matches")
        files_src2 = os.listdir(os.path.join(source2_path, lab))

        for filename in files_src1:
            if filename in files_src2:
                print("Start reading files... " + filename)
                #Open files of corresponding lab
                f1 = open(os.path.join("no_matches", filename), 'r',encoding='iso-8859-1')
                f2 = open(os.path.join(os.path.join(source2_path, lab), filename), 'r',encoding='iso-8859-1')

                #Read file 1 into list drugs1
                drugs1 = []
                line = f1.readline()
                while(line != ''):
                    drugs1.append(line.split(','))
                    line = f1.readline()

                #Read file 2 into list drugs2
                drugs2 = []
                line = f2.readline()
                while(line != ''):
                    drugs2.append(line.split(','))
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
                find_possible_matches(drugs1, drugs2)
                print("Process finished for files... " + filename)

    #Comparing drugs in folder NO_ACR in source2(SAMMED) with all labs in source1(PMB)
    for lab in labs_src1:
        files_src1 = os.listdir(os.path.join(source1_path, lab))
        files_src2 = os.listdir(os.path.join(source2_path, NO_ACRONYMN))

        for filename in files_src1:
            if filename in files_src2:
                print("Start reading files... " + filename)
                #Open files of corresponding lab
                f1 = open(os.path.join(os.path.join(source1_path, lab), filename), 'r',encoding='iso-8859-1')
                f2 = open(os.path.join(os.path.join(source2_path, NO_ACRONYMN), filename), 'r',encoding='iso-8859-1')

                #Read file 1 into list drugs1
                drugs1 = []
                line = f1.readline()
                while(line != ''):
                    drugs1.append(line.split(','))
                    line = f1.readline()

                #Read file 2 into list drugs2
                drugs2 = []
                line = f2.readline()
                while(line != ''):
                    drugs2.append(line.split(','))
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
                find_possible_matches(drugs1, drugs2)
                print("Process finished for files... " + filename)




def find_possible_matches(drugs1, drugs2):
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
            drug1_pres = drug[PROD_PRES_INDEX]
            drug1_lab = re.sub("\n", "", drug[PROD_LAB_INDEX])

            for possible_match in drugs2:
                current_matches = [drug1_code, drug1_name, drug1_complete_name, drug1_pres, drug1_lab]

                #Get drug's attributes for possible match drug
                try:
                    drug2_code = possible_match[PROD_CODE_INDEX]
                    drug2_name = possible_match[PROD_NAME_FORMATTED_INDEX]
                    drug2_complete_name = possible_match[PROD_NAME_COMPLETE_INDEX]
                    drug2_pres = possible_match[PROD_PRES_INDEX]
                    drug2_lab = re.sub("\n", "", possible_match[PROD_LAB_INDEX])
                except:
                    print(possible_match)
                #Check macth by drugs' names by calling any_abbrev utility method
                if drug1_complete_name != NOT_FOUND and drug2_complete_name != NOT_FOUND:
                    if any_abbrev(drug1_name, drug2_name):
                        current_matches = current_matches + [drug2_code, drug2_name, drug2_complete_name ,drug2_pres, drug2_lab]

                else:
                    #Check macth by drugs' names by  comparing if drugs' names are identical
                    if drug1_complete_name ==  drug2_complete_name:
                        print(drug1_complete_name)
                        print(drug2_complete_name)
                        print("complete names verifyied.")
                        current_matches = current_matches + list(possible_match)

                if len(current_matches) > len(drug):
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
    with open(os.path.join("log", 'no_matches_stats.csv'), 'a') as stats_file:
        stats_file.write("{}\n".format(len(no_matches.values())))
    with open(os.path.join("log", 'matches_stats.csv'), 'a') as stats_file:
        stats_file.write("{}\n".format(len(matches)))

    #Store attributes of drugs that didnt match by name
    for key in no_matches.keys():
        with open(os.path.join("no_matches", key + '.csv'), 'a') as no_matches_file:
            for no_match in list(set(no_matches[key])):
                no_match = list(no_match)
                last_item = len(no_match) - 1
                for item in no_match[:last_item]:
                    no_matches_file.write("{},".format(item))
                no_matches_file.write("{}\n".format(no_match[last_item]))
    print("No matches saved.")

    #Store attributes of drugs that matched by name
    with open(os.path.join("matches", 'matches.csv'), 'a') as matches_file:
        for match in matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                matches_file.write("{},".format(item))
            matches_file.write("{}\n".format(match[last_item]))

    print("Matches saved.")

def search_drugs_presentation_matches():
    """ Search drugs' matches comparing drugs' presentation description"""

    #Open and read file that contais drugs matched by name
    matches_file = open(os.path.join( "matches", "matches.csv"), 'r')
    possible_matches = []
    line = matches_file.readline()
    while(line != ''):
        possible_matches.append(line.split(','))
        line = matches_file.readline()
    matches_file.close()

    #Tranforms list of lists in list of tuples then tranform list in set to eliminate duplicateds and returns to list again
    possible_matches = list(set(map(tuple, possible_matches)))

    matches = []
    no_matches = []

    #Get possible matches by name, check their digits patterns using utility method called check_digits_pattern and compare results
    for match in possible_matches:
        drug1_pres = match[PM_PROD_PRES_INDEX_1]
        drug1_pres_units = check_digits_pattern(drug1_pres)
        drug2_pres = match[PM_PROD_PRES_INDEX_2]
        drug2_pres_units = check_digits_pattern(drug2_pres)
        if compare_lists(drug1_pres_units, drug2_pres_units):
            matches.append(match)
        else:
            no_matches.append(match)

    #Store attributes of drugs that matched by presentation description
    with open(os.path.join("matches", 'matches_pres.csv'), 'a') as matches_file:
        for match in matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                matches_file.write("{},".format(item))
            matches_file.write("{}".format(match[last_item]))
    print("Matches by Pres saved.")

    #Store attributes of drugs that didnt match by presentation description
    with open(os.path.join("log", 'no_matches_pres.csv'), 'a') as no_matches_file:
        for match in no_matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                no_matches_file.write("{},".format(item))
            no_matches_file.write("{}".format(match[last_item]))
    print("No Matches by Pres saved.")
