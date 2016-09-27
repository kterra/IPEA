from tokenizer import *
from drug_parser import *

if __name__ == '__main__':

    # tokenizers = [Tokenizer(" COMP 500MG (CX C/1 BL C/6)"),  Tokenizer("CPR REVEST 250 MG x 30"), Tokenizer("250 MG COM REV CT BL AL PLAS INC X 30"),
    # Tokenizer("GOTAS 50 MG 15 ML x 1 (/ML)"), Tokenizer("50 MG/ML SUS OR CT FR PLAS OPC GOT X 15 ML"), Tokenizer(" 50/12.5 MG C/30 COMP"),
    # Tokenizer(" CPR 12.5 MG x 30 (/50)"), Tokenizer("250 MG/5ML PO P/ SUS OR CT FR VD AMB X 150 ML + CP MED")]

    tokenizers = [Tokenizer("CPR REVEST 250 MG x 30"), Tokenizer("GOTAS 50 MG 15 ML x 1 (/ML)"), Tokenizer(" CPR 12.5 MG x 30 (/50)"),
    Tokenizer("CREME DERMAT 15 MG 30 G x 1 (/G)")]

    for tok in tokenizers:
        parser = Parser()
        parser.parse_IMS(tok.tokenize())
        print("\n")
