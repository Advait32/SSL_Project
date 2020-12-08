from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from difflib import SequenceMatcher
import pygments.lexers
import pygments.token
import hashlib
import sys
import argparse
import re
import os
from difflib import SequenceMatcher
import pygments.lexers
import pygments.token
import hashlib
import sys
import argparse
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

class LogicView(APIView):
    
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        Dir_name = body_data['file_p']
        Output = []
        for filname in os.listdir('media/'+ Dir_name):
          for filname1 in os.listdir('media/'+ Dir_name):
              if filname!=filname1:
                  Output.append((filname+' '+' '+' '+' '+' '+filname1+' '+' ',' '+' '+str(final_function('media/'+ Dir_name+'/'+filname,'media/'+Dir_name+'/'+filname1)))) 

            
            #print(filname)
            #print(filname1)
            #f = open(filname, 'r')

            #f1 = open(filname,'r')
            #f2 = open(filname1,'r')
            
            #print(filname,filname1,plagiarismCheck('media/'+ Dir_name+'/'+filname,'media/'+Dir_name+'/'+filname1))
        for fi in os.listdir('media/'+ Dir_name):
            os.remove('media/'+Dir_name+'/'+fi)
        os.rmdir('media/'+Dir_name)
        return Response(Output, status=status.HTTP_201_CREATED)
          
      #return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(#\*.*?\*/|#[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, str(string))


def removechar(string):
    string = string.replace("import",'')
    #string = string.replace(" as ",'')
    string = string.replace("(",'')
    string = string.replace(")",'')

    return string

def tokenize(filename):
    file = open(filename, "r")
    text = file.read()
    #text = removechar(text) 
    lexer = pygments.lexers.guess_lexer_for_filename(filename, text)
    tokens = lexer.get_tokens(text)
    tokens = list(tokens)
    result = []
    file.close()
    lenT = len(tokens)
    count1 = 0    #tag to store corresponding position of each element in original code file
    count2 = 0    #tag to store position of each element in cleaned up code text
    # these tags are used to mark the plagiarized content in the original code files.
    for i in range(lenT):

        if tokens[i][0] in pygments.token.Keyword :
            result.append(('i', count1, count2))
            count2 +=1
        if tokens[i][0] == pygments.token.Name and not i == lenT - 1 and not tokens[i + 1][1] == '(':
            result.append(('N', count1, count2))  #all variable names as 'N'
            count2 += 1
        elif tokens[i][0] in pygments.token.Literal.String:
            result.append(('S', count1, count2))  #all strings as 'S'
            count2 += 1
        elif tokens[i][0] in pygments.token.Name.Function:
            result.append(('F', count1, count2))   #user defined function names as 'F'
            count2 += 1
        elif tokens[i][0] == pygments.token.Text or tokens[i][0] in pygments.token.Comment:
            pass   #whitespaces and comments ignored
        else:
            result.append((tokens[i][1], count1, count2))  
            #tuples in result-(each element e.g 'def', its position in original code file, position in cleaned up code/text) 
            count2 += len(tokens[i][1])
        count1 += len(tokens[i][1])

    return result

def toText(arr):
    cleanText = ''.join(str(x[0]) for x in arr)
    return cleanText



#sha-1 encoding is used to generate hash values
def hash(text):
    #this function generates hash values
    hashval = hashlib.sha1(text.encode('utf-8'))
    hashval = hashval.hexdigest()[-4 :]
    hashval = int(hashval, 16)  #using last 16 bits of sha-1 digest
    return hashval

#function to form k-grams out of the cleaned up text
def kgrams(text, k = 15 ):
    tokenList = list(text)        
    n = len(tokenList)
    kgrams = []
    for i in range(n - k + 1):
        kgram = ''.join(tokenList[i : i + k])
        hv = hash(kgram)
        kgrams.append((kgram, hv, i, i + k))  #k-gram, its hash value, starting and ending positions are stored
        #these help in marking the plagiarized content in the original code.
    return kgrams

#function that returns the index at which minimum value of a given list (window) is located
def minIndex(arr):
    minI = 0
    minV = arr[0]
    n = len(arr)
    for i in range(n):
        if arr[i] <= minV:
            minV = arr[i]
            minI = i
    return minI

#we form windows of hash values and use min-hash to limit the number of fingerprints
def fingerprints(arr, winSize = 5):
    HL = []
    for i in arr:
        HL.append(i[1])   
    arrLen = len(HL)
    prevMin = 0
    currMin = 0
    temp = 0
    max_index = arr[winSize][3]
    windows = []
    fingerprintList = []
    #print(arrLen-winSize)
    for i in range(arrLen - winSize):
        win = HL[i: i + winSize]  #forming windows
        windows.append(win)
        
        currMin = i + minIndex(win)
        if not currMin == prevMin:  #min value of window is stored only if it is not the same as min value of prev window              
            min_index = arr[i][2]
            temp = min_index
            max_index = arr[i+winSize][3]
            fingerprintList.append((min_index,HL[currMin],max_index))  #reduces the number of fingerprints while maintaining guarantee
            prevMin = currMin  #refer to density of winnowing and guarantee threshold (Stanford paper)
        #print(currMin,end=" ")
        else:
            max_index = arr[i+winSize][3]
    #print(fingerprintList)
    return fingerprintList

def hashList(arr):
    HL = []
    for i in arr:
        HL.append(i[1])
    return HL    

#takes k-gram list as input and returns a list of only hash values

def plagiarismCheck(file1, file2):
    f1 = open(file1, 'r')
    text = f1.read()
    text = removechar(text)
    f1.close()
    filetowrite = open(file1,'w')
    filetowrite.write(text)
    filetowrite.close()
    fx = open(file1, 'r')
    token1 = tokenize(file1) 
    #print(token1[1][1])
    str1 = toText(token1)
    token2 = tokenize(file2)
    str2 = toText(token2)
    #str1 = removechar(str1)
    kGrams1 = kgrams(str1)  #stores k-grams, their hash values and positions in cleaned up text
    kGrams2 = kgrams(str2)
    HL1 = hashList(kGrams1)  #hash list derived from k-grams list
    HL2 = hashList(kGrams2)
    fpList1 = fingerprints(kGrams1)
    fpList2 = fingerprints(kGrams2)
    count=0;
    start = []   #to store the start values corresponding to matching fingerprints
    end = []   #to store end values
    code = fx.read()  #original code
    newCode = ""   #code with marked plagiarized content
    points = []
    # print(token1[1][2])
    # print(kGrams1[fpList1[1][0]][2])
    # print(kGrams1[fpList1[1][0]][3])
    for i in fpList1:
        for j in fpList2:
            if i[1] == j[1]:   #fingerprints match
                flag = 0
                flag2 = 0
                match = HL1.index(i[1])   #index of matching fingerprints in hash list, k-grams list
                newStart = kGrams1[i[0]][2]
                newEnd = kGrams1[i[0]][3]
                #print(newStart,"\t",newEnd)
                for k in token1:
                    if k[2] == newStart:   #linking positions in cleaned up code to original code
                        startx = k[1]
                        flag = 1
                    if k[2] == newEnd:
                        endx = k[1]
                        flag2 = 1
                if flag >= 1:
                    if flag2 >= 1:
                        points.append([startx, endx])

                flag = 0
                flag2 = 0
                match = HL1.index(i[1])   #index of matching fingerprints in hash list, k-grams list
                newStart = kGrams1[match][2]
                newEnd = kGrams1[match][3]
                #print(newStart,"\t",newEnd)
                for k in token1:
                    if k[2] == newStart:   #linking positions in cleaned up code to original code
                        startx = k[1]
                        flag = 1
                    if k[2] == newEnd:
                        endx = k[1]
                        flag2 = 1
                if flag >= 1:
                    if flag2 >= 1:
                        points.append([startx, endx])

    points.append([0,1])
    points.append([2,3])            
    points.sort(key = lambda x: x[0])
    points = points[1:]
    #print(points[0])
    #print(points[1])
    mergedPoints = []
    if points[0] is not None:
        mergedPoints.append(points[0])
    j=0
    for i in range(1, len(points)):
        last = mergedPoints[len(mergedPoints) - 1]
        if j==0:
            j +=1
            if points[0][0] >= last[0] and points[0][0] <= last[1]: #merging overlapping regions
                if points[0][1] > last[1]:
                    mergedPoints = mergedPoints[: len(mergedPoints)-1]
                    mergedPoints.append([last[0], points[0][1]])
                else:
                    pass
            else:
                mergedPoints.append(points[0])

        if points[i][0] >= last[0] and points[i][0] <= last[1]: #merging overlapping regions
            if points[i][1] > last[1]:
                mergedPoints = mergedPoints[: len(mergedPoints)-1]
                mergedPoints.append([last[0], points[i][1]])
            else:
                pass
        else:
            mergedPoints.append(points[i])
    newCode = code[: mergedPoints[0][0]]
    plagCount = 0
    for i in range(len(mergedPoints)):
        if mergedPoints[i][1] > mergedPoints[i][0]:
            plagCount += mergedPoints[i][1] - mergedPoints[i][0]
            newCode = newCode + '\x1b[6;30;42m' + code[mergedPoints[i][0] : mergedPoints[i][1]] + '\x1b[0m'
            if i < len(mergedPoints) - 1:
                newCode = newCode + code[mergedPoints[i][1] : mergedPoints[i+1][0]]
            else:
                newCode = newCode + code[mergedPoints[i][1] :]
        else:
            plagCount +=  mergedPoints[i][0] - mergedPoints[i][1]               
    #print('%.2f'%(100*plagCount/len(code)))        
    #print(newCode)        
    return('%.2f'%(100*plagCount/len(code))) 

def plagerised_ratio(filename1, filename2):
    tokens1 = tokenize(filename1) #(elements of cleaned up code, their position in original code, position in cleaned up code)
    file1 = toText(tokens1)  #cleaned up code - greatly increases effectiveness of plagiarism checker
    tokens2 = tokenize(filename2)
    file2 = toText(tokens2)
    SM = SequenceMatcher(None, file1, file2)
    similarity_ratio = SM.ratio()
    # ratio of plagiarised content
    return('%.2f'%(100*similarity_ratio))  

def maximum(a,b,c):
    if a>=b and a>=c:
        return a
    if b>=a and b>=c:
        return b   
    if c>=a and c>=b:
        return c    

vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
def bag_of_words(file1 , file2):
    text = []
    text.append(open(file1).read())
    text.append(open(file2).read()) 
    vectors = vectorize(text)
    sim_score = cosine_similarity(vectors,vectors)[0][1]  
    return('%.2f'%(100*sim_score))  

def final_function(file1,file2):
    return(max(float(bag_of_words(file1 , file2)),float(plagerised_ratio(file1 , file2)) ,float(plagiarismCheck(file1 , file2) )))