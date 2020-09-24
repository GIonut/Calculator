####################################### PREPARING DATA ############################################

def get_data():
    #get's data from the user
    data = []
    base = int(input("choose the base: ")) # a base
    string = input()
    string = string.split()
    nr1 = string[0]# first number
    sign = string[1]# the operand
    nr2 = string[2]# seconf number
    data.append(base)
    data.append(nr1)
    data.append(sign)
    data.append(nr2)
    return data[:] # returning a list containing all of the data


def check_operation(sign):
    #assing to an operator sign it's specific operation
    if sign == '+':
        return addition
    elif sign == '-':
        return subtraction
    elif sign == '*':
        return multiplication
    else :
        return division


def get_string(vector, operation):
    # prepares the output in a nicely manner. combines outputs from a list into one string
    string = ""
    if operation == division:
        return "quotient: " + str(vector[0] ) + "\n" + "remainder: " + str(vector[1])
    n = len(vector)
    if n > 1:
        i = 0
        while i < len(vector) and vector[i] == '0':
            vector.remove(vector[i])
            i += 1
    for i in vector:
        string += str(i)
    return string


def to_vector(nr):
    #transform a number into a vector
    l = list(nr)
    l.reverse()
    return l


def check_max_min(nr1, nr2):
    #checks the minimum and the maximum of two vectors, regarding the numbers of entries
    if len(nr1) >= len(nr2):
        return [nr1, nr2]
    else:
        return [nr2, nr1] # the larger vector is returned on the first position and the smallest on the second pos


def fill_with_zeroes(nr, zeroes):
    #fill with non-significant zeroes in order to have vectors with the same amount of digits
    while zeroes:
        nr.append('0')
        zeroes -= 1


def turn_digit(digit):
    #turn a number in base ten into it's correspondent digit in base 16
    digits = {
        10:'A',
        11:'B',
        12:'C',
        13:'D',
        14:'E',
        15:'F'
    }
    return digits[digit]



def turn_letter(digit):
    # turns a digit in base sixteen into it's correspondent number in base 10
    digits = {
        'A':10,
        'B':11,
        'C':12,
        'D':13,
        'E':14,
        'F':15
    }
    return digits[digit]



def get_digit_base_10(nr):
    #tries to convert a number from string format into integer format.
    try:#If it cannot be done by default it converts the digit from base 16 into base 10
        return int(nr)
    except Exception:
        digit = turn_letter(nr)
        return digit


def convert_from_ten(nr):
    #convert a number from base ten into another base using multiple divisions by ten and returning the rests in reverse order
    p = 1
    r = 0
    while nr != 0:
        r = r + (nr % 10) * p
        nr = nr // 10
        p = p*10
    return r


def convert_to_ten(base, nr):
    #converts a number from a certain base to base ten by multiplying it's digits, one by one, with powers of the base
    p = 1
    to_ten = 0
    while nr != 0 :
        digit = nr%10
        to_ten = to_ten + digit*p
        nr = nr//10
        p = p * int(base)
    return to_ten


def convert_to_ten_list(base, vector):
    # converts a number(written as a list) from a certain base to base ten by multiplying it's digits, one by one, with powers of the base
    p = 1
    to_ten = 0
    vector.reverse()
    for i in vector:
        digit = int(i)
        to_ten = to_ten + digit * p
        p = p * int(base)
    return to_ten


def prepare_data():
    #prepare the data for the functions
    data = get_data()
    base = data[0] # assign data
    nr1 = data[1]
    nr2 = data[3]
    sign = data[2]
    operation = check_operation(sign)# conect the operator with the specific operation
    number1 = to_vector(nr1)# get the operands as vectors in order to be able to parse their digits
    number2 = to_vector(nr2)#
    compare = check_max_min(number1, number2)
    maxim = compare[0]
    minim = compare[1]
    zeroes = len(maxim) - len(minim)# having the maximum and the minimum numbers coputed.
    fill_with_zeroes(minim, zeroes)# we add zeroes at the beggining of the smallest one to get the same number of digits
    number1 = maxim
    number2 = minim
    return [base, number1, operation, number2] #return the prepared data


################################################ CALCULATOR ####################################################################

def addition(base, number1, number2):
    # adds two numbers in a certaine base
    _sum = [] # sum will be computed as a vector with entities representing its digits
    carry = 0 # we need a carry in case of adding two letter which have a sum greater or equal than the base. in this case, carry will be set to 1
    n = len(number1) # the length of the first number( since the two numbers are equal in length as a consequence of filling the smallest number wit non-significat zeros)
    for i in range(n):# parse the vectors representing the digits of the two numbers, in reverse order
        digit1 = get_digit_base_10(number1[i])# if the symbol of the digit is a leeter from base 16 digits, it will be converted in base 10
        digit2 = get_digit_base_10(number2[i])#
        add_in_10 = carry + digit1 + digit2# we perform addition in base ten between the two digits
        if add_in_10 >= base:# if the sum of the two digits is greater or equal to the base
            carry = 1# set carry to one
            digit = add_in_10 % base # get the actual digit of the actual sum
        else:# otherwise
            carry = 0# we set the carry to it's initial value, 0
            digit = add_in_10# and the digit of the actual sum does not need to be modified
        if base > 10 and digit > 9:# if the digit is a number representing a digit in base 16
            digit = turn_digit(digit)#we convert it into a letter symbol
        _sum.append(str(digit))# and add it as a valid digit of the actual sum
    _sum.append(str(carry))# if the last operation provides a set-to-1 carry  we wiil consider it as the last digit of the actual sum
    _sum.reverse()# we reverse the digit to get the sum, because we performed operation starting from the last digits  of the numbers
    return _sum# finally return the sum


def subtraction(base, number1, number2):
    #subtract two numbers in a certain base
    carry = 0# start with an initial carry of value 0
    _sub = []# the subtraction of the two numbers will be hold in a list
    n = len(number1)# get the length of the numbers, equal as number of digits
    for i in range(n):# parse the numbers
        digit1 = get_digit_base_10(number1[i])# making sure there are actually digits and not letters from the repres in base 16
        digit2 = get_digit_base_10(number2[i])
        sub_in_10 = carry + digit1 - digit2# subtract the two digits and add the carry which can be -1 in case of "barrow"
        if sub_in_10 < 0:#if the subtraction of the digits provided a negative value
            carry = -1# it means we have to barrow from a higher level digit in our number and set carry to -1
            digit = base + sub_in_10# # get the actual digit in the final value
        else:# otherwise set carry to 0
            carry = 0
            digit = sub_in_10# and add the digit as it is
        if base > 10 and digit > 9:
            digit = turn_digit(digit)# making sure first, if it is a digit in base sixteen, to represent it with the proper symbol
        _sub.append(str(digit))
    _sub.reverse()# reverse the digits to get the final value
    return _sub


def multiplication(base, number1, number2):
    #multiplicate a number with a digit in a certain base
    _prod = []# product will be hold in a list
    carry = 0# start with an initial carry
    n = len(number1)# get the length of the number
    digit2 = get_digit_base_10(number2[0])# making sure that the digit we multiply with is in base ten, since the operation will be in base ten
    for i in range(n):# parse the number's digits
        digit1 = get_digit_base_10(number1[i])
        mul_in_10 = carry + digit1 * digit2# multiply the digit and number2 in base ten
        carry = mul_in_10 // base# carry will get the value of the integer division between the product and the base
        digit = mul_in_10 % base# the actual digit will get the value of the remainder of the division
        if base > 10 and digit > 9:
            digit = turn_digit(digit)# making sure we have the correct representation symbol
        _prod.append(digit)# append the digit to the final product
    _prod.append(carry)# append the carry as well
    _prod.reverse()# reverse to get the actual value
    return _prod


def division(base, number1, number2):
    #divides two values in a certain base
    number1.reverse()# reverse the reversed number to get the initial one
    divisor = get_digit_base_10(number2[0])# convert the divisor into base 10 because the operation will be made in base 10
    quotient = []# the quotien will be hold into a list
    remainder = 0# remainder is 0 at first
    group = []# we need to divide a group of two digits if the divisor is greater than just one digit
    digit1 = get_digit_base_10(number1[0])#checking that case; it can happen only with the first letter
    if digit1 >= divisor:# bc after this it will get the value of the remainder
        div_in_10 = digit1 // divisor# of the division between the group and the divisor
        group.append(digit1 % divisor)#which is less then the divisor
        if base > 10 and div_in_10 > 9:
            div_in_10 = turn_digit(div_in_10)
        quotient.append(str(div_in_10))# finally add it to the quotient and continue with thw remaining digits
    else:#otherwise just add it to the quotient
        group.append(str(digit1))
    n = len(number1)
    for i in range(1, n):# since we have already manage to deal with the first letter we start cotinue with the second one
        digit1 = get_digit_base_10(number1[i])
        group.append(digit1)# getting that two digits group
        newnr = convert_to_ten_list(base, group)# convert it into base 10
        div_in_10 = newnr // divisor# do the division
        newnr = newnr % divisor# save the remainder
        remainder = str(newnr)# which in the end will be the final remainder
        if base > 10 and div_in_10 > 9:
            div_in_10 = turn_digit(div_in_10)
        quotient.append(str(div_in_10))# add the result of the division into the quotient
        group = []# clear the group
        group.append(newnr)# and add to it the remainder
    if base > 10 and int(remainder) > 9:
        remainder = turn_digit(int(remainder))# finaly making sure of the correct representation in any base
    quotient = get_string(quotient, None)
    return [quotient, remainder]# and return the quotient and the remainder


############################################ Tests ############################################################################

def test_addition():
    number1 = ['6', '3', '4', '1']
    number2 = ['6','5', '0', '0']
    base = 7
    add = addition(base, number1, number2)
    string = get_string(add, addition)
    assert(string == '1525')
    number1 = ['F', '6', 'B', 'A', '4', '5']
    number2 = ['D', '7', '9', '0', 'D', 'C']
    base = 16
    add = addition(base, number1, number2)
    string = get_string(add, addition)
    assert (string == '121B4EC')

def test_subtraction():
    number1 = ['6', '3', '4', '1']
    number2 = ['6', '5', '0', '0']
    base = 7
    sub = subtraction(base, number1, number2)
    string = get_string(sub, subtraction)
    assert (string == '1350')
    number1 = ['4', '5', '3', '0', '1', '2']
    number2 = ['6', '6', '4', '5', '5', '0']
    base = 7
    sub = subtraction(base, number1, number2)
    string = get_string(sub, subtraction)
    assert (string == '121555')

def test_multiplication():
    number1 = ['5', '4', '3', '2', '1']
    number2 = ['5', '0', '0', '0', '0']
    base = 6
    mul = multiplication(base, number1, number2)
    string = get_string(mul, multiplication)
    assert (string == '111101')
    number1 = ['4', 'F', '3', '2', 'A']
    number2 = ['B', '0', '0', '0', '0']
    base = 16
    mul = multiplication(base, number1, number2)
    string = get_string(mul, multiplication)
    assert (string == '6F8B7C')

def test_division():
    number1 = ['1', '0', '1', '0', '2']
    number2 = ['2', '0', '0', '0', '0']
    base = 6
    div = division(base, number1, number2)
    assert (div == ['10030', '1'])
    number1 = ['6', '8', 'F', '0', 'A', '2']
    number2 = ['E', '0', '0', '0', '0', '0']
    base = 16
    div = division(base, number1, number2)
    assert (div == ['3011B', 'C'])

def run_all_tests():
    test_addition()
    test_subtraction()
    test_multiplication()
    test_division()

############################################################## MAIN ##########################################################################################################3

if __name__ == "__main__":
            run_all_tests()
            cont = 1
            while cont == 1:
                data = prepare_data()
                base = data[0]
                number1 = data[1]
                number2 = data [3]
                operation = data[2]
                output = operation(base, number1, number2)
                string = get_string(output, operation)
                print(string)
                cont = int(input("continue? Press 1: "))
