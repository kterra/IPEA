from tokenizer import *
from dparser import *

if __name__ == '__main__':



    tokenizers_ims = [Tokenizer("CPR REVEST 250 MG x 30"), Tokenizer("GOTAS 50 MG 15 ML x 1 (/ML)"), Tokenizer(" CPR 12.5 MG x 30 (/50)"),
    Tokenizer("CREME DERMAT 15 MG 30 G x 1 (/G)")]

    tokenizers_sammed = [Tokenizer(" 20 MG 2BLT C/ 7 CAP"), Tokenizer("0.75 MG 1 BL X 2 COMP"), Tokenizer("50 MG/ML SUS OR CT FR PLAS OPC GOT X 15ML"),
    Tokenizer(" 0.2 MG/ML XPE CT FR PET AMB X 120 ML + CP MED"), Tokenizer(" 10MG/G GEL CREM CT BG AL X 60G"), Tokenizer(" 100MG C/12 COMP"),
    Tokenizer(" 100MG/ML SOL FR X 50 ML MICRORAL"), Tokenizer(" 25 MG/5ML XPE C/ 120 ML"), Tokenizer(" 50/12.5 MG C/30 COMP")]

    for tok in tokenizers_ims:
        parser = Parser()
        parser.parse_IMS(tok.tokenize())
        print("\n")

    for tok in tokenizers_sammed:
        parser = Parser()
        parser.parse_SAMMED(tok.tokenize())
        print("\n")
