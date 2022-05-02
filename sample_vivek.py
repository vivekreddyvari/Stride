from bs4 import BeautifulSoup
import re


string = """ 



EUR 119,95



"""

string_n = """


Vorige
  |  


Dames  /  


Schoenen  /  


Sandalen  /  


Teensandalen  /  


Teensandalen - bianco


"""

string_m = """


Vorige
  |  


Dames  /  


Schoenen  /  


Korte laarzen - grey



"""

string1 = string_n.split("\n")


def filter_blanks(string):
    values = [val.strip("\xa0/") for val in string if val != '' and val != ' ']

    return values

value_returned = filter_blanks(string1)



print(value_returned)
print(len(value_returned))
print(value_returned[2] + ' ' + value_returned[3] + ' ' + value_returned[4])



# print(string1)

# string2 = ('Blauwe Adidas Sneakers', 'Blauwe Adidas')
# print(type(string2))

# print(string2[0])
# print(string2[1])