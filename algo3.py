
# coding: utf-8

# In[91]:


from itertools import islice
import numpy as np
import string
import random
import math
import algo1
import sys


# In[7]:


#parsing file with real passwords
def readPassword(inputfile):
    realPasswordList = []
    with open(inputfile) as infile:
        for line in infile:
            line = line.replace("\n", "")
            realPasswordList.append(line.strip())
    return realPasswordList   


# In[8]:


# parsing rock you file
def rock_you(path, n_rockyou):
    password_list = []
    text_file = open(path, "r")
    lines = text_file.readlines()

    #reading passwords into list
    for line in lines[:n_rockyou]:
        password = line.split(' ')[-1:][0]
        password_list.append(password[:-1])
    
    return password_list


# In[9]:


#cateorizing passwords into 3 categories: name/digits/combo
def categorize(password_list):
    letters = set('abcdefghijklmnopqrstuvwxyz')
    digits = set('123456789')

    only_letters = []
    only_digits = []
    combo = []

    for password in password_list:
        count_letters = 0
        count_digits = 0
        count_special = 0
        for c in password:
            if c in letters:
                count_letters+=1
            elif c in digits:
                count_digits+=1
            else:
                count_special+=1
        if count_letters==len(password):
            only_letters.append(password)
        elif count_digits==len(password):
            only_digits.append(password)
        else:
            combo.append(password)
            
    def isWord(s):
        count=0
        for c in s:
            if c in letters:
                count+=1
        if count==len(s):
            return True
        return False
    
    def isDigit(s):
        count=0
        for c in s:
            if c in digits:
                count+=1
        if count==len(s):
            return True
        return False
    
    for word in combo:
        sections = break_down(word)
        for item in sections:
            if isWord(item) and item not in only_letters:
                only_letters.append(item)
            elif isDigit(item) and item not in only_digits:
                only_digits.append(item)
                
    return make_dic(only_letters), make_dic(only_digits), make_dic(combo)

#function to make dictionary
def make_dic(category):
    dic = {}
    for item in category:
        dic[len(item)] = dic.get(len(item),[]) + [item]
    return dic


# In[10]:


#breaking down input password or any password into sections of Word/Digits/Special characters
def break_down(input_passwd):
    
    letters = set('abcdefghijklmnopqrstuvwxyz')
    digits = set('123456789')
    sections = []
    start = 0
    end = 0
    
    while end<len(input_passwd):
        if input_passwd[end] in letters:
            end+=1
            while end<len(input_passwd):
                if input_passwd[end] in letters:
                    end+=1
                else:
                    break
            sections.append(input_passwd[start:end])
            start=end
        elif input_passwd[end] in digits:
            end+=1
            while end<len(input_passwd):
                if input_passwd[end] in digits:
                    end+=1
                else:
                    break
            sections.append(input_passwd[start:end])
            start=end
        else:
            end+=1
            while end<len(input_passwd):
                if input_passwd[end] not in letters and input_passwd[end] not in digits:
                    end+=1
                else:
                    break
            sections.append(input_passwd[start:end])
            start=end  
                
    return sections
        
            


# In[39]:


#this function picks honey words and generates 30% of the N - the required honeyword list
def pick_honeywords(input_passwd,n):
    size = len(input_passwd)
    honey_words = []
    seen= set()
    
    while len(seen)< int(n/3):
        if size not in letters_dic:
            break
        passwd = random.choice(letters_dic[size])
        if passwd not in seen:
            seen.add(passwd)
            honey_words.append(passwd)
        if len(letters_dic[size])==len(seen):
            break
            
    seen1=set()
    while len(seen1)< int(n/3):
        if size not in digits_dic:
            break
        passwd = random.choice(digits_dic[size])
        if passwd not in seen1:
            seen1.add(passwd)
            honey_words.append(passwd)
        if len(digits_dic[size])==len(seen1):
            break
            
    seen2=set()
    while len(seen2)<int(n/3):
        if size not in combo_dic:
            break
        passwd = random.choice(combo_dic[size])
        if passwd not in seen2:
            seen2.add(passwd)
            honey_words.append(passwd)
        if len(combo_dic[size])==len(seen2):
            break

    return honey_words


# In[40]:


#This function generates honeywords to generate 40% of N(required honeywords)
#It breaks up the input password into sections (sections of words digits and special characters)
#eg. 123@world => ['123','@','world']
#eg2. hello5world => ['hello','5','world']
#then each of these sections are replaced simultaneously by picking another string from the 
#respective dicitionary of the section and generating new honey words.
#eg. hello@123 => world#456
def generate_honey_words(input_passwd, n):
    sections = break_down(input_passwd)
    honey_words = []
    seen = set()
    
    letters = set('abcdefghijklmnopqrstuvwxyz')
    digits = set('123456789')
    special_characters = list('!@$%&_?.~')
    
    def isWord(s):
        count=0
        for c in s:
            if c in letters:
                count+=1
        if count==len(s):
            return True
        return False
    
    def isDigit(s):
        count=0
        for c in s:
            if c in digits:
                count+=1
        if count==len(s):
            return True
        return False
    
    while len(honey_words)<int(n):
        new_word = ""
        for item in sections:
            if isWord(item) and len(item) in letters_dic:
                new_word += random.choice(letters_dic[len(item)])
            elif isDigit(item) and len(item) in digits_dic:
                new_word += random.choice(digits_dic[len(item)])
            else:
                new_word += random.choice(special_characters)
        if new_word not in seen:
            seen.add(new_word)
            honey_words.append(new_word)   
    return honey_words
                
            


# In[61]:


def toughnuts(n):
    letters = list('abcdefghijklmnopqrstuvwxyz')
    digits = list('123456789')
    special_characters = list('!@$%&_?.~')
    random_list = random.sample((letters + digits + special_characters), len(letters + digits + special_characters))
    tough_nuts = []
    for i in range(n):
        tough_nuts.append(''.join(random.choice(random_list) for i in range(32)))
    return tough_nuts    
    


# In[90]:


rockyou_passwords = rock_you("rockyou-withcount.txt",100000)
letters_dic, digits_dic, combo_dic = categorize(rockyou_passwords)

def main_final(N, input_passwords):
    res=[]
    for passwd in input_passwords:
        list1 = pick_honeywords(passwd, int(0.3*N))
        list2 = generate_honey_words(passwd, int(0.4*N))
        list3 = toughnuts(int(0.1*N))
        n = N - len(list1) - len(list2) - len(list3)
        random_list = random.sample(list1+list2+list3, int(N/3) if N>3 else 1)
        list4 =[]
        for item in random_list:
            list4 += algo1.honeyWordGenerator([item],N/2)[0]
        list4 = random.sample(list4, n)
        final = list1 + list2 + list3 + list4 + [passwd]
        random.shuffle(final)
        res.append(final)
        print(len(final))
    print(len(res))
    return res


# In[92]:


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("missing arguments. Please try with: python algorithm1.py n input_filename output_filename")
    n = int(sys.argv[1]) - 1
    inputfile = sys.argv[2]
    outputfile = sys.argv[3]
    # parse input file
    input_passwords = readPassword(inputfile)
    # generate n honey words
    honeyWordLists = main_final(n, input_passwords)
    # output to desired file
    algo1.storeHoneyWord(honeyWordLists, outputfile)
        

