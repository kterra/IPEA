import collections
import re

class Tokenizer:

    def __init__(self, text):
        self.text = text
        print(self.text)
        self.text_size = len(text)
        self.text_current_index = -1
        self.keywords = ['MG','G','ML','L','CT', 'CX','BLT' 'X']

    def get_next_character(self):
        self.text_current_index += 1
        #print(self.text[self.text_current_index])
        return self.text[self.text_current_index]

    def peek_next_character(self, peek_unit):
        self.text_current_index += peek_unit
        if self.text_current_index < self.text_size:
            character = self.text[self.text_current_index]
        else:
            character = "EOF"
        self.text_current_index -= peek_unit
        return character

    def read_number(self):
      value = ""
      while self.peek_next_character(1).isdigit() or self.peek_next_character(1) == ".":
          value += self.get_next_character()
      return ("NUMBER", '{0:g}'.format(float(value)))

    def read_specials(self):
        value = ""
        if self.peek_next_character(1) == '/':
            value += self.get_next_character()
            while self.peek_next_character(1).isspace():
                self.get_next_character()

            value += self.get_next_character()
            value = value.upper()

            if value == '/G':
                return (value, value)

            elif value == '/L':
                return (value, value)

            elif value == '/M':
                if self.peek_next_character(1).upper() == 'L':
                    value += self.get_next_character()
                    value = value.upper()
                    return (value, value)

            elif value == '/5':
                while self.peek_next_character(1).isspace():
                    self.get_next_character()
                value += self.get_next_character()
                value = value.upper()
                if value == '/5M':
                    if self.peek_next_character(1).upper() == 'L':
                        value += self.get_next_character()
                        value = value.upper()
                        return (value, value)
            else:
                while not self.peek_next_character(1).isspace() and self.peek_next_character(1) != "EOF":
                    value += self.get_next_character()
                return ("STRING", value)

        elif self.peek_next_character(1) == 'C' and self.peek_next_character(2) == '/':
            value += self.get_next_character()
            value += self.get_next_character()
            return (value, value)
        elif self.peek_next_character(1) == ')':
            value += self.get_next_character()
            return ("RIGHT_PARENTHESIS", value)

        elif self.peek_next_character(1) == '(':
            value += self.get_next_character()
            return ("LEFT_PARENTHESIS", value)
        elif self.peek_next_character(1) == '+':
            value += self.get_next_character()
            return ("PLUS", value)
        else:
            return "NONE"

    def read_string(self):
        value = ""
        while self.peek_next_character(1).isalpha() and self.peek_next_character(1) != "EOF":
            value += self.get_next_character()

        value = value.upper()
        if value in self.keywords:
            return ("KEYWORD", value)

        return ("STRING", value)

    def next_token(self):
      character = self.peek_next_character(1)

      if character.isdigit():
          return self.read_number()
      else:
          special = self.read_specials()
          if special == "NONE":
              return self.read_string()
          else:
              return special

    def tokenize(self):
        tokens = []
        while self.text_current_index < self.text_size - 1:
            #print("{} {}".format(self.text_current_index,self.text_size))
            if self.peek_next_character(1).isspace():
                self.get_next_character()
            else:
                token = self.next_token()
                #print(token)
                tokens.append(token)

        return tokens


if __name__ == '__main__':

    tokenizer = Tokenizer(" 500 MG COM CT BL AL PLAS INC X 56")
    print(tokenizer.tokenize())
