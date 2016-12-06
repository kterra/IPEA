#Regex Test Cases
import re

def check_digits_pattern(med_pres):
    regex = r"\s?(\d+)\s?M?C?G|" +\
    r"\s?(\d+\.?\d*?)\s?MG?L?/G?L?|" +\
    r"\s?(\d+\.\d*)\s?M?C?G|" +\
    r"\s?(\d+\.\d*)\s?M?L|" +\
    r"\s?(\d+\.\d*)\s?[DOSE(S)]|" +\
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
    print(med_pres)
    results = []

    item1 = None
    item7 = None
    item8 = None
    item9 = None
    item10 = None
    for ix in range(len(pms)):
        item = pms[ix]
        print(item)

        if item[0]:
            results.append(item[0])
        if item[2]:
            results.append('{0:g}'.format(float(item[2])))
        if item[3]:
            results.append('{0:g}'.format(float(item[3])))
        if item[4]:
            results.append('{0:g}'.format(float(item[4])))
        if item[1]:
            item1 = item[1]
        if item[5]:
            results.append(item[5])
        if item[6]:
            results.append(item[6])
        if item[7]:
            item7 = item[7]
        if item[8]:
            item8 = item[8]
        if item[9]:
            item9 = item[9]
        if item[10]:
            item10 = item[10]
        if item[11]:
            results.append(item[11])

    if item1:
        if item10:
            results.append('{0:g}'.format(float(item1)*int(item10)))
        else:
            results.append(item1)
    else:
        if item8:
            if item9:
                results.append(str(int(item8)*int(item9)))
            else:
                results.append(item8)
        else:
            if item9:
                results.append(item9)

        if item7:
            if item10:
                results.append(str(int(item7)*int(item10)))
            else:
                results.append(item7)
        else:
            if item8:
                results.append(item9)



    print(sorted(results))
    return sorted(results)

if __name__ == '__main__':


    #
    # check_digits_pattern("CPR 40 MG x 10")
    # check_digits_pattern("40 MG COM REVEST CT 3 BL AL PLAS INC X 10")
    # print("\n")
    #
    # check_digits_pattern("750 MG PÓ SOL INJ CT FA VD INC + 1 AMP DIL VD INC X 6 ML")
    # check_digits_pattern("CEFUROXIMA SOD.MG F.AMP 750 MG 6 ML x 1")
    # print("\n")
    #
    # check_digits_pattern("0.750 MG PÓ SOL INJ CT FA VD INC + 1 AMP DIL VD INC X 6 ML")
    # check_digits_pattern("CEFUROXIMA SOD.MG F.AMP 0.75 MG 6 ML x 1")
    # print("\n")
    #
    # check_digits_pattern("1 G COM REV CT BL AL PLAS INC X 30")
    # check_digits_pattern("CLOR.METFORMINA MG CPR REVEST 1 G x 30")
    # print("\n")
    #
    # check_digits_pattern("1G PÓ P/ SOL INJ CT FA VD INC + DIL AMP PLAS INC X 10 ML")
    # check_digits_pattern("CEFALOTINA SODI.MG F.AMP C/DILU 1 G 10 ML x 1")
    # print("\n")
    #
    # check_digits_pattern("1G PÓ P/ SOL INJ CT 50 FA VD INC + 50 DIL AMP PLAS INC  X 10 ML (EMB HOSP)")
    # check_digits_pattern("CEFALOTINA SODI.MG F.AMP C/DILU 1 G 10 ML x 50")
    # print("\n")
    #
    # check_digits_pattern("CPR REVEST 50 MG x 30")
    # check_digits_pattern("100 MG + 25 MG COM REV CT BL AL PLAS OPC X 15")
    # print("\n")
    #
    # check_digits_pattern(" CPR REVEST 20 MG x 14")
    # check_digits_pattern(" 20 MG 2BLT C/ 14 COMP")
    # print("\n")
    #
    # check_digits_pattern("CPR REVEST 50 MG x 8")
    # check_digits_pattern("50 MG COM REV CT BL AL PLAS OPC X 8")
    # print("\n")
    #
    # check_digits_pattern(" CPR 20 MG x 28")
    # check_digits_pattern(" 20MG C/ 28 CPR.")
    # print("\n")
    #
    # check_digits_pattern("CREME 50 MG 10 G x 1 (/G)")
    check_digits_pattern("50 MG/G CREM DERM CT BG AL X 10 G")
    print("\n")
    #
    # check_digits_pattern(" CPR 10 MG x 30")
    # check_digits_pattern(" 10MG COM CT 3 BL AL PLAS BRANCO OPC X 10")
    # print("\n")

    # check_digits_pattern("CREME 15 G x 1")
    # check_digits_pattern("1.0 MG/G CREM DERM CT BG AL X 15")
    # print("\n")

    #check_digits_pattern("CREME 15 G x 1")
    check_digits_pattern("ANTI RHO(D), 300 MCG, SOLUÇÃO INJETÁVEL 200.00 DOSE(S)")
    check_digits_pattern("1 G FRASCO 20.00 ML")

    print("\n")
