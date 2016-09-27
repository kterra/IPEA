
class Parser:

    def parse_IMS(self, tokenized_sentence):

        # IMS GRAMMAR
        # S -> FF CONC KEYWORD NUMBER$
        # S -> FF CONC VOL KEYWORD NUMBER$
        # S -> FF CONC VOL KEYWORD NUMBER EXTRA$
        # FF -> STRING+
        # CONC -> NUMBER UNIT
        # VOL -> NUMBER UNIT
        # EXTRA -> LEFT_PARENTHESIS SLASH NUMBER UNIT RIGHT_PARENTHESIS
        # EXTRA -> LEFT_PARENTHESIS SLASH UNIT RIGHT_PARENTHESIS

        number_of_tokens = len(tokenized_sentence)

        FF = ""
        CONC = ""
        VOL = ""
        KEYWORD = ""
        NUMBER = ""

        current_token = 0
        while current_token< number_of_tokens and tokenized_sentence[current_token][0] == "STRING":
            FF += tokenized_sentence[current_token][1] + " "
            current_token +=1

        if current_token + 1 < number_of_tokens:
            CONC += tokenized_sentence[current_token][1]
            current_token +=1
            CONC += tokenized_sentence[current_token][1]
            current_token +=1

        if  current_token + 1 < number_of_tokens and tokenized_sentence[current_token][0] == "NUMBER":
            VOL += tokenized_sentence[current_token][1]
            current_token +=1
            VOL += tokenized_sentence[current_token][1]
            current_token +=1
        if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "KEYWORD":
            KEYWORD = tokenized_sentence[current_token][1]
            current_token +=1

        if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "NUMBER":
            NUMBER = tokenized_sentence[current_token][1]
            current_token +=1

        if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "LEFT_PARENTHESIS":
            current_token +=1
            while current_token < number_of_tokens - 1 :
                CONC += tokenized_sentence[current_token][1]
                current_token +=1

        print("Forma Farmaceutica: " + FF)
        print("Concentracao: " + CONC)
        print("Volume: " + VOL)
        print("Numero de Comprimidos: " + NUMBER)



    def parse_SAMMED(tokenized_sentence):

        # SAMMED GRAMMAR
        # S -> CONC1 FF CT INFO KEYWORD NUMBER$
        # S -> CONC1 FF CT INFO KEYWORD VOL$
        # S -> CONC1 FF NUMBER INFO KEYWORD VOL$
        # S -> CONC1 FF CT NUMBER INFO KEYWORD NUMBER$
        # S -> CONC1 INFO C/ NUMBER$
        # S -> CONC1 NUMBER KEYWORD C/ NUMBER FF$
        # S -> CONC1 NUMBER INFO KEYWORD NUMBER FF$
        # S -> CONC1 C/ NUMBER FF$
        # S -> CONC1 PLUS CONC1 FF CT INFO KEYWORD NUMBER$
        # S -> CONC1 KEYWORD NUMBER FF$
        # S -> FF CONC1 KEYWORD NUMBER INFO$
        # S -> FF C/ CONC1$
        # S -> FF KEYWORD CONC1$
        # S -> CONC2 FF NUMBER UNIT$
        # S -> CONC2 FF CT INFO KEYWORD VOL$
        # CONC1 -> NUMBER UNIT
        # CONC1 -> UNIT NUMBER
        # CONC2 -> NUMBER UNIT SLASH UNIT
        # CONC2 -> NUMBER UNIT SLASH NUMBER UNIT
        # VOL -> NUMBER UNIT
        # INFO -> STRING+
        # FF -> STRING+

        pass
