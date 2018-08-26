import sys
from itertools import islice
import numpy as np
import string
import random
import math
import algo1


# ==============================================================================
#   Handle input / output files
# ==============================================================================

def read_rockyou():
    """Reads the top 100 Rock You passwords from 'rockyou-withcount.txt'
    from the root of this directory.
    Returns: The raw traning data as a string."""
    # Read the top 100 Rock You passwords
    with open("rockyou-withcount.txt") as datafile:
        dataraw = list(islice(datafile, 100))
    return dataraw


def read_data_input(filename):
    """Given a string for the filename, reads the input paswords.
    Returns: A list of input passwords as a list of strings."""
    # Read the input passwords
    with open(filename) as input_file:
        data_input = input_file.read().splitlines()
    return data_input


def get_train(dataraw):
    """Given the raw training data as a string, chops it up
    into a list of passwords without counts.
    Returns: A list of training passwords as a list of strings."""
    # Ordered list of [count, password] from the top 100 Rock You passwords
    dataset = list(map(lambda x: x.strip().split(), dataraw));
    # Ordered list of just passwords from the top 100 Rock You passwords
    train = list(map(lambda x: x[1], dataset))
    return train    


def write_data_output(filename, sweetwords):
    """Given a filename as a string and the list of sweetwords
    as a list of a list of strings, write the contents to an
    output file.
    Returns: The output content as a string."""
    data_output = list(map(lambda x: ','.join(x), sweetwords))
    data_output = '\n'.join(data_output)
    print(data_output)

    with open(filename, 'w') as output_file:
        output_file.write(data_output)
    output_file.closed
    
    return(data_output)




# ==============================================================================
#   HELPER: Get Subwords
# ==============================================================================
def get_subwords(data_in):
    """Returns a list of objects that define the first sub word to occur
    in a password. We define a subword to be a sequence of letters.
    If the password is only letters, the subword value is the password itself.
    If the password is only non letters, subword value is empty string.
    
    Example input: ["hello2world", "qwerty", "12345",]
    Example output: [
    {"subword": "hello", "start": 0, "end": 5},
    {"subword": "qwerty", "start": 0, "end": 5},
    {"subword": "", "start": 0, "end": 5}]"""
    swords = []
    for pw in data_in:
        # Get the first word in the password
        # where word is a sequence of letters
        pwsub = {"subword": "", "start": -1, "end": -1}
        start = -1
        end = -1
        for i,c in enumerate(pw):
            if start == -1 and c.isalpha():
                start = i
                end = i
            elif start != -1:
                end = i
                if not c.isalpha():
                    break
            end += 1
        pwsub = {"subword": pw[start:end], "start": start, "end": end}
        swords.append(pwsub)
    return swords


# ==============================================================================
#   HELPER: Get categories
# ==============================================================================
def get_categories(data_in, swords):
    """Given a list of input passwords and a list of their subwords,
    identify the category for each input from the training set.
    The training set has been manually categorized and its values
    declared locally here.
    
    1. Check if the entire password exists in the training set. If so,
       look up the category this password belongs to.
    2. If the entire password is not in the training set, check if the
       subword is in the training set. If so, look up the category this
       subword belongs to.
    3. If neither exist in the training set, let the category be ''.
    
    RETURN: a list of categories, where the i-th index represents the category
    of the i-th input password."""
    # The row number corresponding to each category
    # In other words, these are 1-indexed and not 0-indexed
    rnames =   [11,12,16,18,19,24,30,35,37,43,44,45,46,50,51,55,61,64,65,67,70,71,74,76,77,78,81,86,92,93,95,97,98,99,100]
    rmisc =    [6,8,14,26,27,31,32,33,36,39,47,57,58,59,69,73,83,85,87,89,96]
    rlove =    [5,13,15,22,34,38,52,53,56,62,68,79,80,90]
    rpopcult = [25,29,41,49,54,63,66,75,88,91,94]
    rnums =    [1,2,3,7,9,17,21,23,40,48,72,82]
    rlazy =    [4,10,20,28,42,60,84]

    # A list of passwords split by categories
    names =   list(map(lambda x: train[x-1], rnames))
    misc =    list(map(lambda x: train[x-1], rmisc))
    love =    list(map(lambda x: train[x-1], rlove))
    popcult = list(map(lambda x: train[x-1], rpopcult))
    nums =    list(map(lambda x: train[x-1], rnums))
    lazy =    list(map(lambda x: train[x-1], rlazy))

    categories = []
    for i, pw in enumerate(data_in):
        row = -1
        cat = ""
        
        for r, tpw in enumerate(train):
            if pw == tpw:
                # Check if the password is in the training set
                # If it is, set the row (1-indexed, not 0-indexed) to it
                # Then look up the row in the training password categories
                row = r + 1
                break
            elif swords[i]["subword"] == tpw:
                # Check if the subword is in the training set
                # If it is, set the row (1-indexed, not 0-indexed) to it
                # Then look up the row in the training password categories
                row = r + 1
                break
            # Else, check the next training password for a match
        
        if row != -1:
            # If we were able to find a matching training password,
            # we can identify which category pw belongs to
            if row in rnames:
                cat = "names"
            elif row in rmisc:
                cat = "misc"
            elif row in rlove:
                cat = "love"
            elif row in rpopcult:
                cat = "popcult"
            elif row in rnums:
                cat = "nums"
            elif row in rlazy:
                cat = "lazy"
        # Else, the row = -1 and cat = '' as initialized
               
        # Set the category for the i-th pw:
        categories.append(cat)
        
    return categories


# ==============================================================================
#   HELPER: Add Entropy
# ==============================================================================
def add_entropy(password, subword, gw):
    """PREREQ: The subword value should be a nonempty string.
    Given a password, its subword object, and a generated replacement
    subword, generate a sweetword by replacing the original subword with
    the generated one. While replacing, also add entropy in
    up to 4 positions by random chance by inserting a random digit.
    Retruns: The newly generated sweetword with entropy."""
    start = subword["start"]
    end = subword["end"]
    gen = ""
    entropy = {
        "pre": bool(random.getrandbits(1)), 
        "start": bool(random.getrandbits(1)), 
        "end": bool(random.getrandbits(1)), 
        "suf": bool(random.getrandbits(1))
    }
    
    if entropy["pre"]:
        gen += ''.join(random.choice(string.digits))
    gen += password[:start]

    if entropy["start"]:
        gen += ''.join(random.choice(string.digits))
    gen += gw

    if entropy["end"]:
        gen += ''.join(random.choice(string.digits))
    gen += password[end:]

    if entropy["suf"]:
        gen += ''.join(random.choice(string.digits))
    
    return gen



# ==============================================================================
#   HELPER: Generate with Samples
# ==============================================================================
def gen_with_samples(password, subword, samples, N):
    """Given a password, its subword object, and a list of sample training data,
    generate N sweetwords that replace the subword with a new subword 
    generated from the samples. For N >= 10, add extra entropy in the sweetwords.
    Returns: The generated passwords, including the original, in shuffled order
    as a list of strings."""
    
    start = subword["start"]
    end = subword["end"]
    result = []
    S = len(samples)
    
    # Automatically add the original password to the sweetword generation result
    result.append(password)
    
    # Only generate N-1 new sweetwords since the original password
    # is already included
    for i in range(N-1):
        gw = samples[i % S]
        if i <= 5:
            gen = password[:start] + gw + password[end:]
        else:
            gen = add_entropy(password, subword, gw)
        
        # For large N, randomly add even more entropy by using Algo 1
        if i >= 10:
            # There's a 50% chance the first element is the original gen
            gen = algo1.honeyWordGenerator([gen], 2)[0][0]
            
        # If the generated password is a duplicate,
        # try to generate again with entropy
        while gen in result:
            gen = add_entropy(password, subword, gw)
            
        result.append(gen)
        
    random.shuffle(result)
    return result


# ==============================================================================
#   Generate Sweetwords
# ==============================================================================
def gen_sweetwords(train, data_in, N):
    """Given the training data and input passwords, generate N sweetwords
    for each input password. One of the sweetwords is the input password.
    
    1. Start by checking if the subword of input password OR
       the entire input password itself belong to a category.
       
    2. If a category can be identified AND it is not the 'nums' category,
       select up to 3 + ln(N) sample training passwords from the category.
       Then, generate N sweetwords using those samples.

    3. Else if the subword is not short (> 4 chars) select up to ln(N) sample
       training passwords at random from the entire training set.
       Then, generate N sweetwords using those samples.
       
    4. Else (the subword is too short and/or the password is all non-letters)
       use algo1 to generate N sweetwords.
    
    Let the output be a list of N sweetwords (including the input password)
    for each input password.
    Returns: The output as a list of list of strings.
    """
    # The row number corresponding to each category
    # In other words, these are 1-indexed and not 0-indexed
    rnames =   [11,12,16,18,19,24,30,35,37,43,44,45,46,50,51,55,61,64,65,67,70,71,74,76,77,78,81,86,92,93,95,97,98,99,100]
    rmisc =    [6,8,14,26,27,31,32,33,36,39,47,57,58,59,69,73,83,85,87,89,96]
    rlove =    [5,13,15,22,34,38,52,53,56,62,68,79,80,90]
    rpopcult = [25,29,41,49,54,63,66,75,88,91,94]
    rnums =    [1,2,3,7,9,17,21,23,40,48,72,82]
    rlazy =    [4,10,20,28,42,60,84]

    # A list of passwords split by categories
    names =   list(map(lambda x: train[x-1], rnames))
    misc =    list(map(lambda x: train[x-1], rmisc))
    love =    list(map(lambda x: train[x-1], rlove))
    popcult = list(map(lambda x: train[x-1], rpopcult))
    nums =    list(map(lambda x: train[x-1], rnums))
    lazy =    list(map(lambda x: train[x-1], rlazy))
    category = {"names": names, "misc": misc, "love": love, "popcult": popcult, "nums": nums, "lazy": lazy}
    
    output = []
    swords = get_subwords(data_in)
    catnms = get_categories(data_in, swords)
    
    for i, pw in enumerate(data_in):
        genpwds = []
        if (catnms[i] in category.keys()) and (catnms[i] != "nums"):
            # If the password or subword exists in the training data
            randsamples = np.random.choice(category[catnms[i]], 3 + round(math.log1p(N))).tolist()
            randsamples.append(pw)
            
            # Remove duplicates in samples:
            samples = []
            for elem in randsamples:
                if elem not in samples:
                    samples.append(elem)

            genpwds.extend(gen_with_samples(pw, swords[i], samples, N))
            output.append(genpwds)
            
        elif len(swords[i]["subword"]) > 4:
            # If the password or subword does not exist in the training data
            # But, the subword is long enough to replace
            randsamples = np.random.choice(train, round(math.log1p(N))).tolist()
            randsamples.append(pw)
            
            # Remove duplicates in samples:
            samples = []
            for elem in randsamples:
                if elem not in samples:
                    samples.append(elem)
            
            genpwds.extend(gen_with_samples(pw, swords[i], samples, N))
            output.append(genpwds)
        
        else:
            # If the subword is too short or if the password is all non-letters
            algo1_result = algo1.honeyWordGenerator([pw], N-1)[0]
            genpwds.extend(algo1_result)
            output.append(genpwds)
            
    return output        


# ==============================================================================
#   TEST: Test outputs
# ==============================================================================
def test_output(data_in, data_out, N):
    """Given the input passwords, output sweetwords, and desired N,
    checks if each input password is in the list of its corresponding
    sweetwords. Also checks if there are N sweetwords.
    Recall, if N = 5 then 1 password is the original and 4 are generated.
    Prints out any errors or a success message."""
    errors = 0
    for i, pw in enumerate(data_in):
        if pw not in data_out[i]:
            errors += 1
            print("[!!] Input password {", pw, "} was not found in the output. (Line", i+1, ")")
        if len(data_out[i]) != N:
            errors +=1
            print ("[!!] Input password {", pw, "} has", len(data_out[i]), "out of N = ", N, "sweetwords. (Line", i+1, ")")
    if errors == 0:
        print("[~~] NO ERRORS FOUND")



# ==============================================================================
#   MAIN
# ==============================================================================
if __name__ == '__main__':
    """Does the following:
    1. Read the training data
    2. Read the input passwords
    3. Gets list of training passwords.
    4. Gets output of sweetword generation.
    5. OPTIONAL: Checks for errors.
    6. Writes the generated sweetwords to an output file.
    7. OPTIONAL: Print contents of  output as a success message."""
    try:
        n = int(sys.argv[1])
        input_filename = sys.argv[2]
        output_filename = sys.argv[3]
        if type(n) is not int:
            raise Exception()
        if type(input_filename) is not str:
            raise Exception()
        if type(output_filename) is not str:
            raise Exception()
    except:
        print(
        "-----------------------------------------------------------------------\n"+
        "[!!] ERROR:\n"+
        "Use the format 'python algo2.py n input_filename output_filename'\n"+ 
        "when using this program. Where n is an int and where input_filename and\n"+
        "output_filename are strings corresponding to a filename.\n"+
        "-----------------------------------------------------------------------\n")
    
    
    # If no errors detected with input arguments, continue!
    dataraw = read_rockyou()
    input_passwords = read_data_input(input_filename)
    train = get_train(dataraw)
    output_sweetwords = gen_sweetwords(train, input_passwords, n)
    
    # COMMENT THIS OUT FOR FINAL
    # FOR DEBUGGING ONLY
    # test_output(input_passwords, output_sweetwords, 10)
    
    success = write_data_output(output_filename, output_sweetwords)
    if len(success) > 0:
        print("[~~] Done writing to output!")
