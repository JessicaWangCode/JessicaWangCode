# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 21:44:08 2021

@author: 27666

"""
import random
from collections import Counter
import string
import re
import matplotlib.pyplot as plt
import numpy as np
import CaesarModule
#!EXTRA# Create a Caesar Cipher Python mudule that is imported to perform encryption and decryption.


#PART 3
def get_message():    
    #PART 3.1
    #Get message from user via input or file
    input_mode= input("enter a message entry mode(m/f):")
    while True:       
        if input_mode == "m":
            #PART3.2 enter message directly
            message_input = input("enter a message:")
            message = message_input.upper()#PART 1.4 Upper case
            break
        elif input_mode == "f":
            #PART 3.4 read in a file as message
            file_name = input("enter file name or file path:")
            with open(file_name +".txt","r") as p:                
                message_input = p.read()
                message=message_input.upper()#PART 1.4 Upper case
                break
        else:
            #PART 3.3 print error & reinput when incorrect input
            print("error. Please enter again.")
            input_mode= input("choose a input_mode(m/f):")
    #Print out input message     
    print(message)
    return message



def selectN():
    #PART 1.2  Get rotation number from user or generate random number
    rot_type = input("choose a rotation type(M/R):")
    while True:   
        if rot_type == "M":
            rotN = int(input("enter a rotation number:"))
            break
        elif rot_type == "R":
            #PART 1.2 Generate random number
            rotN = random.randint(1,25)
            print(rotN)
            break
        else:
            #PART 1.3 print error & reinput when incorrect input
            print("error. Please enter again.")
            rot_type = input("choose a rotation type(M/R):")
    return rotN

def compare_list(): 
    #PART 4.2.a  read in words.txt 
    with open('words.txt', 'r') as f:     
             comparelist=[]
             comparelist.append(f.read())
             comparelist=comparelist[0].rstrip("\n").upper().split()
             return comparelist
             
def word_list(message):
         #remove punctuation
         trans=str.maketrans({key: None for key in string.punctuation})
         message=message.translate(trans)  
         #Remove newlines and split message into words list
         words = message.replace("\n", " ").split(" ")
         #Get first 10 words from words list
         words10list = words[:10]    
         return words10list
         
def length_list(words10list):
    #Get length of every word in the 10 words list
    lengthlist = []
    for i in words10list: 
        lengthlist.append(len(i))
    return lengthlist    


#decodelist = 25 convertlist
def decode_list(words10list,lengthlist):
    #PART 4.2.b Iterate through 25 rotations on the 10 words
    decodelist = []
    word10string = str(words10list)       
    for autoN in range(0,26):
        decodestring = ''      
        convertlist = []
        for char in range(0,len(word10string)):
                          if 65<=ord(word10string[char])<=90:  
                             decodestring+=(chr((ord(word10string[char])-autoN-65)%26+65))  
                                                
      
       
        convertlist = convert(decodestring,lengthlist)          
        decodelist.append(convertlist)                 
    return decodelist



def convert(decodestring,lengthlist):
    #Convert each rotated string into list by using length for each word
    convertlist = []
    
    for l in lengthlist:
       word = ''
       
       while len(word)<l:
          word += decodestring[0]
          decodestring = decodestring[1:]
          
       convertlist.append(word)
    return convertlist
     #eg:convertlist = ['BLOW', 'BLOW', 'THOU', 'WINTER', 'WIND', 'THOU', 'ART', 'NOT', 'SO', 'UNKIND']  
          

 

               
def compare_vs_decode(convertlist,comparelist,message,decodelist,result):             
#PART 4.2.c.i match word in the rotated first 10 words with common English words                   
   for d in convertlist:
      #PART 4.2.c.ii if one word discovered, present 10 words then ask for confirmation
      if d in comparelist:
                       print (' '.join(convertlist))  
                       B = input("Is it right?(Yes/No):")
                       if B == "Yes":
                            #PART4.2.c.iii Apply successful rotation to rest of message after confimation
                            autoN = decodelist.index(convertlist) 
                            print("rotation number is",autoN)
                            for i in range(0,len(message)):
                                if 65<=ord(message[i])<=90:                              
                                    result += ('{}'.format(chr((ord(message[i])-autoN-65)%26+65)))          
                                else:
                                    result += ('{}'.format(message[i]))
                            #PART4.2.c.iv Print the decrypted message
                            print(result)
                            
                            break
                       elif B == "No":
                          #PART4.2.c.iii continue iterate if "No"
                          pass
                       else:
                             B = input("Sorry, Wrong input. Pleae input Yes or No:") 
   return result

def statistic(message):
    #PART 2.1 compute data create five metrics
    #remove number
    message=re.sub('[\d]','',message)
    #remove punctuation
    trans=str.maketrans({key: None for key in string.punctuation})
    message=message.translate(trans)
    #convert to a list
    if not message.isspace():
        #PART 2.1-Compute total number of words from words list
        words = message.split(" ")
    else:
        words = []
    #PART 2.1-Number of unique words from words set
    words_set = set()
    words_dic = {}
    for word in words:        
        words_dic[word] = words_dic.get(word,0)+1
             
        if word not in words_set:
            words_set.add(word)
            
    title_list = ["Total number of words:","Number of unique words:","minimum word length:","maximum word length:","most common letter:"]
    statistic_list=[len(words),len(words_set)]
    def myfunc(e):
                return len(e)
    if len(words)>0:
        #PART 2.1-sort minimum word length
        words.sort(key=myfunc)
        statistic_list.append(len(words[0]))
        #PART 2.1-sort maximum word length
        words.sort(reverse=True, key=myfunc)
        statistic_list.append(len(words[0]))
    else:
        statistic_list+=[0,0]
    #PART 2.1-Compute most common letter
    message = message.replace(" ", "")
    if len(message)>0:         
        statistic_list.append(Counter(message).most_common()[0][0])
    else:
        statistic_list.append("No word found")
        
    #PART 2.2 save each metric in a file
    with open('metrics.txt', 'w') as m:
        for n,s in zip(title_list,statistic_list):
            m.write(n+' '+str(s)+'\n')

    
    print("\n")
    #PART 2.3 Sort all unique words by frequency
    #!EXTRA# Generate bar chart showing frequency of the five most common words
    word_bar_list = []
    frequency_bar_list = []
    for counter in Counter(words).most_common(5):  
        print(counter[0]+":"+str(counter[1]))
        #PART 2.4 print five most common words sorted in descending order           
        word_bar_list.append(counter[0])
        frequency_bar_list.append(counter[1])
    plt.subplot(211) # 2 rows, 1 column, index 1
    x_pos = np.arange(len(word_bar_list)) # array with element for each group
    plt.bar(x_pos, frequency_bar_list) # bar chart
    plt.xticks(x_pos,word_bar_list ) # replace labels
    plt.xlabel('word')
    plt.ylabel('frequency')
    plt.subplots_adjust(hspace = 0.4) # adjust spacing
    plt.show()
    plt.savefig("plots.png")         
#PART 1.1 main program

message = get_message()


#Get cipher_mode from user
cipher_mode = input("Choose a cipher mode(E/D/A):")
while True:  
   if cipher_mode == "E":
        
      #PART 1.4 Print out encrypted message
      e = CaesarModule.Caesar(message,selectN())
      print(e.encryption())         
      statistic(message)
      break   
      
   elif cipher_mode == "D":
         d = CaesarModule.Caesar(message,selectN())
         print(d.decryption())
         statistic(d.decryption())
         break
   
   #PART 4.1 Additional option A indicating auto-decrypt
   elif cipher_mode == "A":
         
         #words10list = list of the first 10 words
         words10list=word_list(message)
         
         #lengthlist = length of each word from the 10 words
         lengthlist = length_list(words10list)
         
         #decodelist = nested list of 26 rotated words lists
         decodelist = decode_list(words10list,lengthlist)
         
         #comparelist = common English words list imported from word.txt
         comparelist = compare_list()
         
         result = ''
         for eachdl in decodelist:
             #compare rotated word lists with common English words list
             result = compare_vs_decode(eachdl,comparelist,message,decodelist,result)
         
         #PART 4.2.c.v Disenable collecting metrics if not successful
         if len(result)==0:
                 print("Sorry,not found!") 
         else:
             statistic(result)
         break
         
   else:
        #PART 1.3 print error & reinput when incorrect input
        print("error. Please enter again.")
        cipher_mode = input("choose a cipher_mode(E/D/A):")



    
    


        

                           
    
        
        
        
        