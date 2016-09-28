
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



    def parse_SAMMED(self, tokenized_sentence):


        # SAMMED GRAMMAR

        # S -> CONC1 NUMBER KEYWORD C/ NUMBER FF$
        # S -> CONC1 NUMBER INFO KEYWORD NUMBER FF$
        # S -> CONC1 KEYWORD NUMBER FF$
        # S -> CONC1 PLUS CONC1 FF KEYWORD INFO KEYWORD NUMBER$


        # S -> CONC1 FF KEYWORD INFO KEYWORD NUMBER$
        # S -> CONC1 FF KEYWORD INFO KEYWORD VOL$
        # S -> CONC1 FF NUMBER INFO KEYWORD VOL$
        # S -> CONC1 FF KEYWORD NUMBER INFO KEYWORD NUMBER$
        # S -> CONC1 FF PLUS CONC1 FF PLUS CONC1 FF KEYWORD INFO KEYWORD NUMBER
        # S -> CONC1 INFO KEYWORD NUMBER$

        # S -> CONC2 FF VOL$
        # S -> CONC2 FF KEYWORD INFO KEYWORD VOL$
        # S -> CONC2 FF KEYWORD VOL$

        # S -> FF CONC1 KEYWORD NUMBER INFO$
        # S -> FF C/ CONC1$
        # S -> FF KEYWORD CONC1$

        # CONC1 -> NUMBER UNIT
        # CONC2 -> NUMBER UNIT SLASH UNIT
        # CONC2 -> NUMBER UNIT SLASH NUMBER UNIT
        # VOL -> NUMBER UNIT
        # INFO -> STRING+
        # FF -> STRING+

        number_of_tokens = len(tokenized_sentence)

        FF = ""
        CONC = ""
        VOL = ""
        INFO = ""
        KEYWORD = ""
        NUMBER = ""

        current_token = 0


        if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "NUMBER":
            CONC += tokenized_sentence[current_token][1]
            current_token +=1

            if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "UNIT":
                CONC += tokenized_sentence[current_token][1]
                current_token +=1

            if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "SLASH":
                    CONC += tokenized_sentence[current_token][1]
                    current_token +=1
                    if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "NUMBER":
                        CONC += tokenized_sentence[current_token][1]
                        current_token +=1
                    if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "UNIT":
                        CONC += tokenized_sentence[current_token][1]
                        current_token +=1
                    if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "STRING":
                        while  current_token < number_of_tokens and tokenized_sentence[current_token][0] == "STRING":
                            FF += tokenized_sentence[current_token][1] + " "
                            current_token +=1

                    if current_token +1 < number_of_tokens and tokenized_sentence[current_token][0] == "NUMBER":
                        VOL += tokenized_sentence[current_token][1]
                        current_token +=1
                        VOL += tokenized_sentence[current_token][1]
                        current_token +=1
                    elif current_token < number_of_tokens and tokenized_sentence[current_token][0] == "KEYWORD":
                        current_token +=1
                        if current_token + 1 < number_of_tokens and tokenized_sentence[current_token][0] == "NUMBER" :
                            VOL += tokenized_sentence[current_token][1]
                            current_token +=1
                            if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "UNIT":
                                VOL += tokenized_sentence[current_token][1]
                                current_token +=1
                        while  current_token < number_of_tokens and tokenized_sentence[current_token][0] == "STRING":
                            INFO += tokenized_sentence[current_token][1] + " "
                            current_token +=1
                        if current_token + 2 < number_of_tokens and tokenized_sentence[current_token][0] == "KEYWORD" :
                            current_token +=1
                            VOL += tokenized_sentence[current_token][1]
                            current_token +=1
                            if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "UNIT":
                                VOL += tokenized_sentence[current_token][1]
                                current_token +=1
                        if current_token + 1 < number_of_tokens and tokenized_sentence[current_token][0] == "KEYWORD" :
                            current_token +=1
                            VOL += tokenized_sentence[current_token][1]
                            current_token +=1


            elif current_token < number_of_tokens and tokenized_sentence[current_token][0] == "NUMBER":
                NUMBER += tokenized_sentence[current_token][1] + " "
                current_token +=1
                if current_token + 2  < number_of_tokens and tokenized_sentence[current_token][0] == "KEYWORD" and tokenized_sentence[current_token + 1][0] == "C/" :
                    current_token += 2
                    NUMBER += tokenized_sentence[current_token][1] + " "
                    current_token +=1
                elif current_token < number_of_tokens and tokenized_sentence[current_token][0] == "STRING" :
                    while  current_token < number_of_tokens and tokenized_sentence[current_token][0] == "STRING":
                        INFO += tokenized_sentence[current_token][1] + " "
                        current_token +=1
                    if current_token + 1 < number_of_tokens and tokenized_sentence[current_token][0] == "KEYWORD" :
                        current_token +=1
                        NUMBER += tokenized_sentence[current_token][1] + " "
                        current_token +=1

                if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "STRING" :
                    while  current_token < number_of_tokens and tokenized_sentence[current_token][0] == "STRING":
                        FF += tokenized_sentence[current_token][1] + " "
                        current_token +=1


            elif current_token < number_of_tokens and tokenized_sentence[current_token][0] == "PLUS":
                pass
            elif current_token < number_of_tokens and tokenized_sentence[current_token][0] == "KEYWORD":
                current_token +=1
                if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "NUMBER":
                    NUMBER += tokenized_sentence[current_token][1] + " "
                    current_token +=1
                if current_token < number_of_tokens and tokenized_sentence[current_token][0] == "STRING":
                    while  current_token < number_of_tokens and tokenized_sentence[current_token][0] == "STRING":
                        FF += tokenized_sentence[current_token][1] + " "
                        current_token +=1

        elif current_token < number_of_tokens and tokenized_sentence[current_token][0] == "STRING":
            # S -> FF CONC1 KEYWORD NUMBER INFO$
            # S -> FF C/ CONC1$
            # S -> FF KEYWORD CONC1$
            # S -> KEYWORD KEYWORD CONC1$
            pass

        if FF != "":
            print("Forma Farmaceutica: " + FF)
        if CONC != "":
            print("Concentracao: " + CONC)
        if INFO != "":
            print("Info: " +  INFO)
        if VOL != "":
            print("Volume: " + VOL)
        if NUMBER != "":
            print("Numero de Comprimidos: " + NUMBER)
