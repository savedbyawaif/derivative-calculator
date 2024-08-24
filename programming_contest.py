functions = ["sin","cos","tan","csc","sec","cot","arcsin","arccos","arctan","ln","sqrt"]
operators = ["+","-","*","/","^"]
containers = ["(",")","~"]
#dictionary of common derivatives with corresponding keys
common_derivative = {"sin":["cos","(","interior",")"],
                     "cos":["-","sin","(","interior",")"],
                     "tan":["sec","^","2","(","interior",")"],
                     "csc":["-","csc","(","interior",")","*","cot","(","interior",")"],
                     "sec":["sec","(","interior",")","*","tan","(","interior",")"],
                     "cot":["-","csc","^","2","(","interior",")"],
                     "arcsin":["(","1",")","/","sqrt","(","1","-","(","interior",")","^","2",")"],
                     "arccos":["(","-","1",")","/","sqrt","(","1","-","(","interior",")","^","2",")"],
                     "arctan":["1","/","(","1","+","interior","^","2",")"],
                     "ln":["1","/","(","interior",")"],
                     "sqrt":["1","/","(","2","*","sqrt","(","interior",")",")"]
                     }
complist = []

def main():
    dvar = userinput()
    exp = userexp(dvar)
    derived_func = derive(exp, dvar)
    print(*derived_func[1:-1], sep = "")
    print("simplified derivative = ", *simplify(derived_func,dvar)[1:-1], sep = "")

def userinput():
    while True:
        dvar = str(input("Please declare your derivation variable: "))
        if len(dvar) == 1 and dvar.isalpha() == True:
            print(dvar + " is your derivation variable.")
            break
        else:
            print("Please print a single letter")
    return dvar

def userexp(var):
    while True:
        exp = convert(input("Please enter your expression: "))
        valid = True
        valid_char = functions + operators + [var] + containers
        for i in range(len(exp)-1):
            if exp[i] not in valid_char and exp[i].isdigit() == False:
                valid = False
                break
            if exp[i:i+2] in functions or exp[i:i+2] in operators:
                valid = False
                break
        if valid:
            return exp
        else:
            print("Please enter a valid equation")
    
def convert(inp):
    #initialises expression with padding
    converted_input = ["~"]
    stack = ""
    identifier = ""
	#iterates through every character in the input
    for char in inp:
		#checks if stack is a function
        if stack in functions and identifier == "str":
            converted_input.append(stack)
            stack = ""
            
		#checks if currect character is a number
        if char.isnumeric():
			#checks if previous character is a number, if not pushes stack to input list
            if identifier != "int" and identifier != "":
                converted_input.append(stack)
                stack = ""
            identifier = "int"
            
		#checks if current character is a letter (variable)
        if char.isalpha():
			#checks if previous character is a character, if not pushes stack to input list
            if identifier != "str" and identifier != "":
                converted_input.append(stack)
                stack = ""
            identifier = "str"
            
		#checks if stack is a viable symbol
        if char == "(" or char == ")" or char in operators:
            if stack != "":
                converted_input.append(stack)
                stack = ""
            identifier = "bracket"
        
		#checks for whitespace then skips the character
        if char == " ":
            continue
		#adds current character to the stack
        stack += char

    converted_input.append(stack)
    #finalises expression with padding
    converted_input.append("~")
    
    return converted_input

#intakes a list and a derivation variable and returns derivation with respect to derivation variable
def derive(inp, dvar):
    #initial setup of function lists and booleans for product and quotient rule
    func1 = []
    func1fill = 0
    func2 = []
    func2fill = 0
    try:
        #initialization of variables before loops
        i = 0
        #initializes memory constant as 1
        constant = [1]
        bracket_count = 0
        comp_count = 0
        operator = ""
        func_pass = 1
        #passes to check for instances of product and quotient rule
        while func_pass > 0:
            #scans each element in expression
            while i < len(inp):
                #checks for function instance
                if inp[i] == "(" or inp[i] in functions:
                    #increases bracket function count, NOT function count
                    bracket_count += 1 - 1*functions.count(inp[i])
                    #checks for existing function instances
                    if func1fill == 0:
                        #allows first function list to be filled
                        func1fill = 1
                    #checks for filed first function list
                    elif func1fill == 2:
                        #allows second function list to be filled
                        func2fill = 1
                        
                #fills first function list with current element if allowed
                if func1fill == 1:
                    func1.append(inp[i])
                    
                #fills second function list with current element if allowed  
                if func2fill == 1:
                    func2.append(inp[i]) 
                    
                #checks for end of function instance
                if inp[i] == ")":
                    #decreases bracket function count
                    bracket_count -= 1
                    #checks if first function list is currently being filled
                    if func1fill == 1 and bracket_count == 0:
                        #shows first function list as filled and disallows filling
                        func1fill = 2
                    #checks if second function list is currently being filled
                    elif func1fill == 2 and bracket_count == 0:
                        #shows second function list as filled and disallows filling
                        func2fill = 2
                        
                #checks for multiplication or division signs inbetween functions
                if bracket_count == 0 and inp[i] in operators[2:4]:
                    operator = inp[i]
                
                #checks if both function lists are filled
                if func1fill == 2 and func2fill == 2:
                    #adds a function pass and initializes result list
                    func_pass += 1
                    comp_func = []
                    #if functions are multiplied use product rule
                    if operator == "*":
                        comp_func = power_rule(func1,func2,dvar)
                    #if functions are divided use quotient rule
                    elif operator == "/":
                        comp_func = quotient_rule(func1,func2,dvar)
                    #adds result expression to a memory list
                    complist.append(comp_func)
                    #deletes both functions and operator from original expression
                    while bracket_count > 0 or (inp[i] not in operators[0:2] and inp[i] != "~"):
                        if inp[i] == "(":
                            bracket_count -= 1
                        if inp[i] == ")":
                            bracket_count +=1
                        inp.pop(i)
                        i = i - 1
                    i += 1
                    #inserts placeholder element corresponding to index of memory array
                    inp.insert(i, "c:" + str(comp_count))
                    i += 1
                    comp_count += 1
                    
                #if not in function instance and + or - operator is encountered, or both lists are filled, resets function lists and booleans
                if (bracket_count == 0 and inp[i] in operators[0:2]) or (func1fill == 2 and func2fill == 2):
                    func1.clear()
                    func2.clear()
                    func1fill = 0
                    func2fill = 0
                    
                i += 1
            #resets function lists and booleans, and expression index for next pass
            func1.clear()
            func2.clear()
            func1fill = 0
            func2fill = 0
            i = 0
            func_pass -= 1
            bracket_count = 0
        i = 0
        #iterates every element of expression
        while i < len(inp):
            #checks for coefficients to variables which do not use multiplication symbol (ex. 2x)
            if inp[i].isnumeric() and inp[i+1] == dvar:
                #adds constant to a memory list, then removes constant
                constant[0] = int(inp[i])
                inp.remove(inp[i])
            #checks for numbers which are added or subtracted, then sets to 0
            if inp[i].isnumeric():
                front = inp[i+1] in operators[0:2] or inp[i+1] in containers
                back = inp[i-1] in operators[0:2] or inp[i-1] in containers
                if front and back:
                    inp[i] = "0"
            #checks if element is the derivation variable
            if inp[i] == dvar:
                #checks if variable has a power
                if inp[i+1] == "^":
                    #applies derivative rule
                    inp, constant, i = deriv_rule(inp, constant, i)
                else:
                    #derives variable to memory constant
                    inp[i] = str(constant[0])
                    #resets memory constant
                    constant[0] = 1
            #checks if element is a common function
            if inp[i] in functions:
                #checks if function does not have a power
                if inp[i+1] != "^":
                    #puts power to 1
                    inp.insert(i+1, "^")
                    inp.insert(i+2, "1")
                #applies derivative rule
                inp, constant, i = deriv_rule(inp, constant, i)
                
                #initializes variables for chain rule
                saved_element = inp[i]
                char = ""
                bracket = ["~"]
                #initializes first function instance
                bracket_count = 1
                
                #move index of list until it reaches an opening bracket
                while char != "(":
                    char = inp[i]
                    i+=1
                char = inp[i]
                #copies the interior of a function to a memory list until there are no more function instances
                while bracket_count > 0:
                    if char == "(":
                        #adds a function instance
                        bracket_count += 1
                    #adds current element to a memory list
                    char = inp[i]
                    bracket.append(char)
                    i += 1
                    char = inp[i]
                    if char == ")" and bracket_count > 0:
                        #removes a function instance
                        bracket_count -=1
                bracket.append("~")
                #setup for common derivative
                i+=1
                inp.insert(i,"*")
                i+=1
                #inserts common derivative of dictionary keys
                for element in common_derivative[saved_element]:
                    #inserts interior function within the proper place in common derivative
                    if element == "interior":
                        #inserts interior function within the proper place in common derivative
                        inp, i = bracket_insert(inp, bracket[1:-1], i)
                    else:
                        inp.insert(i, element)
                        i+=1
                
                #setup for chain rule for interior function
                inp.insert(i,"*")
                i += 1
                inp.insert(i, "(")
                i += 1
                
                #multiplies current term by the derivation of the interior function
                inp, i = bracket_insert(inp, derive(bracket, dvar)[1:-1], i)

                inp.insert(i, ")")
            i += 1
        i = 0
        #iterates through list to fill placeholders from product/quotient rule
        while i < len(inp):
            #checks if current element is a placeholder
            if len(inp[i].split(":")) > 1:
                index = int(inp[i].split(":")[1])
                #removes placeholder
                inp.pop(i)
                #fills placeholder value with contents from memory list
                for element in complist[index]:
                    inp.insert(i, element)
                    i += 1
            i += 1
    except:
        print("error")
    return(inp)

#intakes list, constant, and iteration number, then applies derivative rule and returns all parameters
def deriv_rule(inp, constant, i):
    #reduces power by 1
    inp[i+2] = str(int(inp[i+2])-1)
    inp.insert(i, "*")
    #power - 1 by any remembered constant
    deriv = (int(inp[i+3])+1)*constant[0]
    #resets memory constant
    constant[0] = 1
    #multiplies variable by earlier calculated constant
    inp.insert(i, str(deriv))
    i += 2
    return inp, constant, i

#intakes list, contents, and iteration number, then fills specified brackets with contents and returns list
def bracket_insert(inp, bracket, i):
    for element in bracket:
        inp.insert(i, element)
        i += 1
    return inp, i

def quickappend(lst, char):
    lst.append(")")
    lst.append(char)
    lst.append("(")
	
#intakes two functions and applies the power rule formula, then returns simplified derivation
def power_rule(func1, func2, dvar):
		#strips extraneous brackets off the exterior of both functions
    if func1[0] == "(" and func1[-1] == ")":
        func1 = func1[1:-1]
    if func2[0] == "(" and func2[-1] == ")":
        func2 = func2[1:-1]
		#pads both functions in preparation for derivation
    func1.insert(0,"~")
    func1.append("~")
    func2.insert(0,"~")
    func2.append("~")
		#adds derivation of both functions to list variables
    d_func1 = derive(func1[:], dvar)
    d_func2 = derive(func2[:], dvar)
    new_list = ["~","("]
		#fills bracket with original function 1
    for element in func1[1:-1]:
        new_list.append(element)
    quickappend(new_list, "*")
		#fills bracket with derived function 2
    for element in d_func2[1:-1]:
        new_list.append(element)
    quickappend(new_list, "+")
		#fills bracket with original function 2
    for element in func2[1:-1]:
        new_list.append(element)
    quickappend(new_list, "*")
		#fills bracket with derived function 1
    for element in d_func1[1:-1]:
        new_list.append(element)
    new_list.append(")")
    new_list.append("~")
		#returns simplified derivative without padding
    return simplify(new_list,dvar)[1:-1]
	
#intakes two functions and applies the quotient rule formula, then returns simplified derivation
def quotient_rule(func1, func2, dvar):
		#strips extraneous brackets off the exterior of both functions
    if func1[0] == "(" and func1[-1] == ")":
        func1 = func1[1:-1]
    if func2[0] == "(" and func2[-1] == ")":
        func2 = func2[1:-1]
		#pads both functions in preparation for derivation
    func1.insert(0,"~")
    func1.append("~")
    func2.insert(0,"~")
    func2.append("~")
		#adds derivation of both functions to list variables
    d_func1 = derive(func1[:], dvar)
    d_func2 = derive(func2[:], dvar)
    new_list = ["~","(","("]
		#fills bracket with original function 2
    for element in func2[1:-1]:
        new_list.append(element)
    quickappend(new_list, "*")
		#fills bracket with derived function 1
    for element in d_func1[1:-1]:
        new_list.append(element)
    quickappend(new_list, "-")
		#fills bracket with derived function 2
    for element in func1[1:-1]:
        new_list.append(element)
    quickappend(new_list, "*")
		#fills bracket with original function 2
    for element in d_func2[1:-1]:
        new_list.append(element)
    new_list.append(")")
    quickappend(new_list, "/")
		#fills bracket with original function 2
    for element in func2[1:-1]:
        new_list.append(element)
    new_list.append(")")
    new_list.append("^")
    new_list.append("2")
    new_list.append("~")
		#returns simplified derivative without padding
    return simplify(new_list,dvar)[1:-1]


#intakes an expression in list format, then simplifies the expression by eliminating double coefficients, 0 terms, and extraneous powers
def simplify(inp, dvar):
    i = 0
    simp_pass = 1
    #sets up code for multiple simplification passes
    while simp_pass > 0:
        #iterates through entire list but buffer character
        while i < len(inp)-1:
            #initializes the current list element as a variable, as well as the elements directly adjacent
            char = inp[i]
            front = inp[i+1]
            back = inp[i-1]
            #strips the brackets off lone numbers
            if back == "(" and front == ")" and char.isnumeric():
                i -= 1
                inp.pop(i)
                inp.pop(i+1)
                simp_pass += 1
            #strips the brackets off lone variables
            if back == "(" and front == ")" and char == dvar and inp[i-2] not in functions:
                i -= 1
                inp.pop(i)
                inp.pop(i+1)
                simp_pass += 1
            #checks if the two characters adjacent to an asterisk are numbers, and multiplies them if true
            if char == "*":
                if front.isnumeric() and back.isnumeric():
                    i -= 1
                    inp.pop(i)
                    inp.pop(i)
                    inp.pop(i)
                    num = int(front) * int(back)
                    inp.insert(i, str(num))
            #checks if the two characters adjacent to an asterisk are numbers and are not coefficients, and multiplies them if true
            if char == "+":
                if front.isnumeric() and back.isnumeric() and (inp[i+2] in operators[0:2] or inp[i+2] in containers[1:3]):
                    i -= 1
                    inp.pop(i)
                    inp.pop(i)
                    inp.pop(i)
                    num = int(front) + int(back)
                    inp.insert(i, str(num))
            #checks for stacked powers and combines them
            if char == "^":
                if front.isnumeric() and back.isnumeric() and inp[i-2] == "^":
                    i -= 1
                    inp.pop(i)
                    inp.pop(i)
                    inp.pop(i)
                    num = int(front) * int(back)
                    inp.insert(i, str(num))
            #checks for specific edge cases related to 0
            if char == "0":
                #checks for added/subtracted zeroes in the middle or end of an expression
                if (front in operators[0:2] and back in operators[0:2]) or (front in containers[1:3] and back in operators[0:2]):
                    inp.pop(i-1)
                    inp.pop(i-1)
                    i -= 2
                #checks for added/subtracted zeroes in the beginning of an expression
                elif front in operators[0:2] and back in containers[1:3]:
                    inp.pop(i)
                    inp.pop(i)
                    i -= 1
                #checks for 0 powers, and reduces affected expressions to 1
                elif back == "^" and (front in containers or front in operators[0:3]):
                    #initializes amount of function isntances encountered
                    bracket_count = 1
                    #deletes elements to the left until there are no more function instances
                    while bracket_count > 0 and inp[i] != "~":
                        #removes a function instance
                        if inp[i] == "(" or inp[i] in functions:
                            bracket_count -= 1
                        #adds a function instance
                        if inp[i] == ")":
                            bracket_count += 1
                        inp.pop(i)
                        i -= 1
                    i += 1
                    #checks if a remaining container is left over
                    if inp[i] not in operators[0:4]:
                        #deletes elements to the right until a function instance is found
                        while inp[i] != "(":
                            inp.pop(i)
                        inp.pop(i)
                        bracket_count = 1
                        #deletes elements to the right until there are no more function instances
                        while bracket_count > 0 and (inp[i] != "~"):
                            if inp[i] == "(":
                                #adds a function instance
                                bracket_count += 1
                            if inp[i] == ")":
                                #removes a function instance
                                bracket_count -= 1
                            if inp[i] == "~":
                                break
                            inp.pop(i)
                    #inserts 1 in place of old function and adds a new simplification pass
                    inp.insert(i, "1")
                    simp_pass += 1
                #checks for an instance of 0 multiplication
                elif inp[i+1] == "*" or inp[i-1] == "*":
                    direction = 0
                    #if 0 is multiplied to the left sets direction right
                    if inp[i+1] == "*":
                        direction = 1
                    #if 0 is multiplied to the right sets direction left
                    elif inp[i-1] == "*":
                        direction = -1
                    #initializes first function instance
                    bracket_count = 1
                    #deletes elements in the specified direction until the first instance of a function occurs
                    while inp[i] != containers[int((1-direction)/2)] and inp[i] != "~":
                        inp.pop(i)
                        i = i - int((1-direction)/2)
                    #checks if current element is at the end of the expression
                    if inp[i] == "~":
                        #changes i opposite to the direction, then inserts 0
                        i = i + int((1-direction)/2)
                        inp.insert(i,"0")
                    else:
                        #deletes current element
                        inp.pop(i)
                        i = i - int((1-direction)/2)
                    #deletes elements to the right until there are no more function instances
                    while bracket_count > 0 or (inp[i] not in operators[0:2] and inp[i] != "~"):
                        if inp[i] == "(":
                            #changes function instance depending on direction
                            bracket_count = bracket_count + direction
                        if inp[i] == ")":
                            #changes function instance depending on direction
                            bracket_count = bracket_count - direction
                        if inp[i] == "~":
                            break
                        inp.pop(i)
                        i = i - int((1-direction)/2)
                    #inserts 0 in place of old function and adds a new simplification pass
                    inp.insert(i + int((1-direction)/2), "0")
                    simp_pass += 1
            #checks for specific edge cases related to 1
            if char == "1":
                #if 1 is an exponent, deletes exponent
                if back == "^" and (front in containers or front in operators[0:3]):
                    inp.pop(i-1)
                    inp.pop(i-1)
                    i -= 2
                #if 1 is multiplied to the right, deletes 1 term
                elif back == "*" and (front in containers[1:3] or front in operators[0:3]):
                    inp.pop(i-1)
                    inp.pop(i-1)
                    i -= 2
                #if 1 is multiplied to the left, deletes 1 term
                elif front == "*" and (back in containers[0:3] or back in operators[0:3]):
                    inp.pop(i)
                    inp.pop(i)
                    i -= 1

            i += 1
        simp_pass -= 1
        i = 0
    return inp

main()