# This passes all the tests, including a few extra I created. It uses recursion. Here are the rules that I used:

# The first letter of the abbreviation must match the first letter of the text
# The rest of the abbreviation (the abbrev minus the first letter) must be an abbreviation for:
# the remaining words, or
# the remaining text starting from any position in the first word.
#http://stackoverflow.com/questions/7331462/check-if-a-string-is-a-possible-abbrevation-for-a-name

# tests=(
#     ('fck','fc kopenhavn',True),
#     ('fco','fc kopenhavn',False),
#     ('irl','in real life',True),
#     ('irnl','in real life',False),
#     ('ifk','ifk gotebork',True),
#     ('ifko','ifk gotebork',False),
#     ('aik','allmanna idrottskluben',True),
#     ('aid','allmanna idrottskluben',True),
#     ('manu','manchester united',True),
#     ('fz','faz zoo',True),
#     ('fzz','faz zoo',True),
#     ('fzzz','faz zoo',False),
#     )

def is_abbrev(abbrev, text):
    abbrev=abbrev.lower()
    text=text.lower()
    words=text.split()
    if len(words) == 1:
        return abbrev in text

    if not abbrev:
        return True
    if abbrev and not text:
        return False
    if abbrev[0]!=text[0]:
        return False
    else:
        return (is_abbrev(abbrev[1:],' '.join(words[1:])) or
                any(is_abbrev(abbrev[1:],text[i+1:])
                    for i in range(len(words[0]))))

def any_abbrev(word1, word2):
    if len(word1) < len(word2):
        return is_abbrev(word1, word2)
    return is_abbrev(word2, word1)

# for abbrev,text,answer in tests:
#     result=is_abbrev(abbrev,text)
#     print(abbrev,text,result,answer)
#     assert result==answer
