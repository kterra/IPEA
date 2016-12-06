import re

##############################################################################################
#                               Constants used for readability                                #
##############################################################################################

EMPTY_NAME = 0
NO_LAB_COLUMN = 0
NO_ACRONYMN = "NO_ACR"
STOPWORDS = ['COM', 'SEM', 'DE', 'DA', 'MG']
NOT_FOUND = "NOT FOUND"

PROD_CODE_INDEX = 0
PROD_NAME_INDEX = 1
PROD_NAME_FORMATTED_INDEX = 2
PROD_NAME_COMPLETE_INDEX = 3
PROD_PRES_INDEX = 4
PROD_LAB_INDEX = 5 #empty for CATMAT
PROD_UNIT_INDEX = 6 #only CATMAT
PROD_VOL_INDEX = 7 #only CATMAT



PM_PROD_PRES_INDEX_1 = 3
PM_PROD_PRES_INDEX_2 = 8

##############################################################################################
#                                     Utility Methods                                        #
##############################################################################################

##############################################################################################
def compare_lists(list1, list2):
    """ Compare to lists.
    Return True if they are equal and False otherwise.
    """
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
##############################################################################################

##############################################################################################
def less_than(s1,s2):
    """Verify if one word is alphabetically successor of another """
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
##############################################################################################

#################################### Abbreviation Methods ####################################
###################### Used to identify abbreviations in drugs' names ########################

def is_abbrev(abbrev, text):
    """
        The first letter of the abbreviation must match the first letter of the text
        The rest of the abbreviation (the abbrev minus the first letter) must be an abbreviation for:
        the remaining words, or the remaining text starting from any position in the first word.

        avaible in: http://stackoverflow.com/questions/7331462/check-if-a-string-is-a-possible-abbrevation-for-a-name
    """
    abbrev=abbrev.lower()
    text=text.lower()
    words=text.split()
    if len(words) == 1:
        return abbrev in text

    if not abbrev:
        return True
    if abbrev and not text:
        return False
    if len(abbrev.split()) != len(words):
        return False
    if abbrev[0]!=text[0]:
        return False
    else:
        return (is_abbrev(abbrev[1:],' '.join(words[1:])) or
                any(is_abbrev(abbrev[1:],text[i+1:])
                    for i in range(len(words[0]))))


def any_abbrev(word1, word2):
    """ Identifity the smallest word and called is_abbrev to verify if the small one is an abbreviation of the biggest one."""
    if len(word1) < len(word2):
        return is_abbrev(word1, word2)
    return is_abbrev(word2, word1)

# for abbrev,text,answer in tests:
#     result=is_abbrev(abbrev,text)
#     print(abbrev,text,result,answer)
#     assert result==answer

#####################################################################################################

#################################### REGEX Identification Methods ####################################
#################### Used to identify patterns in drugs' presentation description ####################

def check_digits_pattern(drug_pres):
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

    pms = re.findall(regex, drug_pres, flags=re.IGNORECASE)
    #print(med_pres)
    results = []
    units = []

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
