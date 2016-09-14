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
                    f1 = open(os.path.join(os.path.join(source1_path, lab), filename), 'r',encoding='iso-8859-1')
                    f2 = open(os.path.join(os.path.join(source2_path, lab), filename), 'r',encoding='iso-8859-1')

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

    print( str(len(no_matches.values())) + " no matches found.")
    print(str(len(matches)) + " matches found.")


    with open(os.path.join("log", 'no_matches_stats.csv'), 'a') as stats_file:
        stats_file.write("{}\n".format(len(no_matches.values())))
    with open(os.path.join("log", 'matches_stats.csv'), 'a') as stats_file:
        stats_file.write("{}\n".format(len(matches)))


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

def prsentation_matches():
    matches_file = open(os.path.join( "matches", "matches.csv"), 'r')

    possible_matches = []
    line = matches_file.readline()
    while(line != ''):
        possible_matches.append(line.split(','))
        line = matches_file.readline()

    matches_file.close()
    possible_matches = list(set(map(tuple, possible_matches)))

    matches = []
    no_matches = []
    for match in possible_matches:
        med1_pres = match[PM_PROD_PRES_INDEX_1]
        med1_pres_units = check_digits_pattern(med1_pres)
        med2_pres = match[PM_PROD_PRES_INDEX_2]
        med2_pres_units = check_digits_pattern(med2_pres)
        if compare_lists(med1_pres_units, med2_pres_units):
            matches.append(match)
        else:
            no_matches.append(match)
    with open(os.path.join("matches", 'matches_pres.csv'), 'a') as matches_file:
        for match in matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                matches_file.write("{},".format(item))
            matches_file.write("{}".format(match[last_item]))
    print("Matches by Pres saved.")

    with open(os.path.join("no_matches", 'no_matches_pres.csv'), 'a') as no_matches_file:
        for match in no_matches:
            last_item = len(match) - 1
            for item in match[:last_item]:
                no_matches_file.write("{},".format(item))
            no_matches_file.write("{}".format(match[last_item]))
    print("No Matches by Pres saved.")

def check_digits_pattern(med_pres):
    regex = r"\s?(\d+)\s?M?G|" +\
    r"\s?(\d+\.\d*)\s?MG?L?/G?L?|" +\
    r"\s?(\d+\.\d*)\s?M?G|" +\
    r"x?X?\s?(\d+)\s?M?G|" + \
    r"x?X?\s?(\d+)\s?M?L|" +\
    r"CT\s?C?/?\s?(\d+)|" +\
    r"\s?(\d+)\s?BLT|" +\
    r"\s?C/\s?(\d+)|" +\
    r"X\s?([1-9]\d+|[2-9]$)|" +\
    r"x?X?\s?1$|" +\
    r"x?X?\s?1\s|" +\
    r"[+]\s?\d+|" +\
    r"\s?(\d+)"

    pms = re.findall(regex, med_pres, flags=re.IGNORECASE)
    #print(med_pres)
    results = []

    item1 = None
    item5 = None
    item6 = None
    item7 = None
    item8 = None
    for ix in range(len(pms)):
        item = pms[ix]
        #print(item)

        if item[0]:
            results.append(item[0])
        if item[2]:
            results.append('{0:g}'.format(float(item[2])))
        if item[1]:
            item1 = item[1]
        if item[3]:
            results.append(item[3])
        if item[4]:
            results.append(item[4])
        if item[5]:
            item5 = item[5]
        if item[6]:
            item6 = item[6]
        if item[7]:
            item7 = item[7]
        if item[8]:
            item8 = item[8]
        if item[9]:
            results.append(item[9])

    if item1:
        if item8:
            results.append('{0:g}'.format(float(item1)*int(item8)))
        else:
            results.append(item1)
    else:
        if item6:
            if item7:
                results.append(str(int(item6)*int(item7)))
            else:
                results.append(item6)
        else:
            if item7:
                results.append(item7)

        if item5:
            if item8:
                results.append(str(int(item5)*int(item8)))
            else:
                results.append(item5)
        else:
            if item8:
                results.append(item8)

    #print(sorted(results))
    return sorted(results)

def compare_lists(list1, list2):

    if list1 and list2:
        if len(list1) != len(list2):
            return False
        else:
            for ix in range(len(list1)):
                if list1[ix] != list2[ix]:
                    return False
            return True
    else:
        return False
