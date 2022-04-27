# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 11:34:11 2021

@author: 27666
"""

#!EXTRA# Define a Caesar cipher class containing encryption and decryption methods
class Caesar():
    def __init__(self,string,rotN):
         self.string=string
         self.rotN=rotN
    def encryption(self):
        result = ''
        for i in range(0,len(self.string)):                          
                                if 65<=ord(self.string[i])<=90:                              
                                    result += ('{}'.format(chr((ord(self.string[i])+self.rotN-65)%26+65)))          
                                else:
                                    result += ('{}'.format(self.string[i]))   
        return result
    def decryption(self):
        result = ''
        for i in range(0,len(self.string)):                          
                                if 65<=ord(self.string[i])<=90:                              
                                    result += ('{}'.format(chr((ord(self.string[i])-self.rotN-65)%26+65)))          
                                else:
                                    result += ('{}'.format(self.string[i]))   
        return result