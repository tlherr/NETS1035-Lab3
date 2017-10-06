"""
 Thomas Herr
 200325519

 Create a python program that takes twp inputs, a string search pattern and a string to search through
"""

class InputLengthException(Exception):
    pass

"""
Search a string for a given pattern, return number of matches and their positions

:param to_search: String to be searched
:param pattern: The pattern to search for
:return: returns nothing
"""
def search_string(to_search, pattern):
    if(len(to_search)<20):
        raise InputLengthException("String must be at least 20 characters")
    if(len(pattern)>4):
        raise InputLengthException("Search string is max 4 characters")

    # Use find to find the number of times a given search string is in the longer string
    count = 0
    positions = []
    lbound = 0
    rbound = len(pattern)

    while(rbound<=len(to_search)):
        # Cut a substring
        substr = to_search[lbound:rbound]
        result = substr.find(pattern)
        if(result!=-1):
            count+=1
            positions.append(lbound)
        lbound+=1
        rbound+=1
    print(count, positions)


to_search = input('Enter a string (at least 20 characters): ')
pattern = input('Enter a substring to search for:')
try:
    search_string(to_search, pattern)
    exit(0)
except InputLengthException as e:
    print("Invalid Input. Exiting...")
    exit(1)