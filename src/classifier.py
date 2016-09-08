import pandas as pd
from constants import *
import os
from abbrev import any_abbrev
import re


def product_matches(source1, source2):
    source1_path = os.path.join("data", source1)
    source2_path = os.path.join("data", source2)
    labs_src1 = os.listdir(source1_path)[1:]
    #print(labs_src1)
    labs_src2 = os.listdir(source2_path)[1:]
    #print(labs_src2)

    print("Start reading files...")
    for lab in labs_src1:
        if lab in labs_src2:
            print("Start reading lab dir... " + lab)
            files_src1 = os.listdir(os.path.join(source1_path, lab))
            files_src2 = os.listdir(os.path.join(source2_path, lab))

            for filename in files_src1:
                if filename in files_src2:
                    print("Start reading files... " + filename)
                    f1 = open(os.path.join(os.path.join(source1_path, lab), filename), 'r')
                    f2 = open(os.path.join(os.path.join(source2_path, lab), filename), 'r')

                    meds1 = []
                    line = f1.readline()
                    while(line != ''):
                        meds1.append(line.split(','))
                        line = f1.readline()

                    meds2 = []
                    line = f2.readline()
                    while(line != ''):
                        meds2.append(line.split(','))
                        line = f2.readline()

                    f1.close()
                    f2.close()
                    print("Files read.")

                    meds1 = list(set(map(tuple, meds1)))
                    meds2 = list(set(map(tuple, meds2)))

                    print("Trying to find matches for files... " + filename)
                    find_possible_matches(meds1, meds2)
                    print("Process finished for files... " + filename)




def find_possible_matches(meds1, meds2):
    matches = []
    no_matches = {}

    for med in meds1:
        prod1_code = med[PROD_CODE_INDEX]
        prod1_name = med[PROD_NAME_FORMATTED_INDEX]
        prod1_initial = prod1_name.strip()[0]
        prod1_complete_name = med[PROD_NAME_COMPLETE_INDEX]
        prod1_pres = med[PROD_PRES_INDEX]
        prod1_lab = re.sub("\n", "", med[PROD_LAB_INDEX])

        for possible_match in meds2:
            current_matches = [prod1_code,prod1_name,prod1_complete_name,prod1_pres,prod1_lab]

            prod2_code = possible_match[PROD_CODE_INDEX]
            prod2_name = possible_match[PROD_NAME_FORMATTED_INDEX]
            prod2_complete_name = possible_match[PROD_NAME_COMPLETE_INDEX]
            prod2_pres = possible_match[PROD_PRES_INDEX]
            prod2_lab = re.sub("\n", "", possible_match[PROD_LAB_INDEX])

            if prod1_complete_name != NOT_FOUND and prod2_complete_name != NOT_FOUND:
                if any_abbrev(prod1_name, prod2_name):
                    current_matches = current_matches + [prod2_code,prod2_name,prod2_complete_name,prod2_pres,prod2_lab]

            else:
                if prod1_complete_name ==  prod2_complete_name:
                    print(prod1_complete_name)
                    print(prod2_complete_name)
                    print("complete names verifyied.")
                    current_matches = current_matches + list(possible_match)

            if len(current_matches) > len(med):
                matches.append(current_matches)
            else:
                if prod1_initial in no_matches.keys():
                    current = no_matches[prod1_initial]
                    current.append(med)
                    no_matches[prod1_initial] = current
                else:
                    no_matches[prod1_initial] = [med]

    print(str(len(no_matches.values())) + " no matches found.")
    print(str(len(matches)) + " matches found.")

    for key in no_matches.keys():
        with open(os.path.join("no_matches", key + '.csv'), 'a') as no_matches_file:
            for no_match in list(set(no_matches[key])):
                no_match = list(no_match)
                last_item = len(no_match) - 1
                for item in no_match[:last_item]:
                    no_matches_file.write("{},".format(item))
                no_matches_file.write("{}\n".format(no_match[last_item]))
    print("No matches saved.")

    with open(os.path.join("matches", 'matches.csv'), 'a') as matches_file:
        for match in matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                matches_file.write("{},".format(item))
            matches_file.write("{}\n".format(match[last_item]))

    print("Matches saved.")

def find_matches_by_pres():
    matches_file = open(os.path.join(os.path.join("data", "matches"), "matches.csv"), 'r')

    possible_matches = []
    line = matches_file.readline()
    while(line != ''):
        possible_matches.append(line.split(','))
        line = matches_file.readline()

    matches_file.close()
    possible_matches = list(set(map(tuple, possible_matches)))
    for match in possible_matches:
        med1_pres = match[PM_PROD_PRES_INDEX_1]
        med1_pres_units = check_digits_pattern(med1_pres)
        med2_pres = match[PM_PROD_PRES_INDEX_2]
        med2_pres_units = check_digits_pattern(med2_pres)

    pass

def check_digits_pattern(med_pres):
    regex = r"(\s?\d+\s?M?G)|X?\s?(\d+\s?M?L?)"
    pms = re.findall(regex, med_pres,flags=re.IGNORECASE)
    results = []
    for item in pms:
        if item[0]:
            results.append(item[0])
        if item[1]:
            results.append(item[1])
    print(sorted(results))

def compare_lists(list1, list2):
    
    pass


# Regex
# option 1: (\s*\d+\s*M*G)|(\d+)|(\d+\s*ML) |X*\s*(\d+\s*[ML]*)
# option 2: (\s?\d+\s?M?G)|X?\s?(\d+\s?M?L?)|(/M?L)
# option 3: (\s?\d+\s?M?G)|X?\s?(\d+\s?M?L?)
#
# Test Cases
# 750 MG PÓ SOL INJ CT FA VD INC + 1 AMP DIL VD INC X 6 ML
# CEFUROXIMA SOD.MG F.AMP 750 MG 6 ML x 1
#
# 1 G COM REV CT BL AL PLAS INC X 30
# CLOR.METFORMINA MG CPR REVEST 1 G x 30
#
# 1G PÓ P/ SOL INJ CT FA VD INC + DIL AMP PLAS INC X 10 ML
# CEFALOTINA SODI.MG F.AMP C/DILU 1 G 10 ML x 1
#
# 1G PÓ P/ SOL INJ CT 50 FA VD INC + 50 DIL AMP PLAS INC  X 10 ML (EMB HOSP)
# CEFALOTINA SODI.MG F.AMP C/DILU 1 G 10 ML x 50
