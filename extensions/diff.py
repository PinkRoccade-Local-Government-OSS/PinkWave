#!/usr/bin/python
"""
diff Extension
Easily get the differents between 2 strings
"""

# Returns difference in second string
def diff(str1,str2):
    str1 = str1.strip()
    str2 = str2.strip()

    # Convert string to characte list
    str1 = list(str1)
    str2 = list(str2)

    # Count highest character list
    highest = len(str1)
    if len(str2) > highest:
        highest = len(str2)

    # Iterate through all characters
    for i in range(0,highest):
        try:
            # If same character found, remove first character from array
            if str1[0] == str2[0]:
                str1 = str1[1:]
                str2 = str2[1:]
            else:
                break
        except IndexError: break

    # Iterate through all characters
    for i in range(0,highest+1):
        try:
            # If same character found, remove last character from array
            if str1[len(str1)-1] == str2[len(str2)-1]:
                str1 = str1[:len(str1)-1]
                str2 = str2[:len(str2)-1]
            else:
                break
        except IndexError: break

    return "".join(str2)

if __name__ == '__main__':

    import sys, os
    from unittest import TestCase
    from unittest import main

    class testDiffString(TestCase):
        def test_plus(self):
            str1 = "hello this is a cool text from the unit test"
            str2 = "hello this is a awesome book from the unit test"
            result = diff(str1,str2)
            expected = "awesome book"
            self.assertEquals(expected,result)
            print result

    main()
