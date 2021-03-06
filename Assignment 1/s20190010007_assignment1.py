# -*- coding: utf-8 -*-
"""S20190010007_Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18p0xiry1jbO-xApUhgBsgzoMJjtMz60e

# **AI ASSIGNMNET 1**
# **Anirudh Jakhotia**
# **Roll No : S20190010007**

## Imports
"""

import numpy as np
import random
import parser
from math import *

"""# **Problem 1**
# **Solving Sudoku using Genetic Algorithm**

#### Passing partially completed grid
"""

startingState = ["x8xxxxx9x", "xx75x28xx", "6xx8x7xx5", "37xx8xx51", "2xxxxxxx8", "95xx4xx32", "8xx1x4xx9", "xx19x36xx", "x4xxxxx2x"]

"""## Checking Row,Column and Sub grid"""

def Function_for_SuitNo(temp_State,no_of_rows,no_of_columns):
  numerical_set2=set()
  numerical_set1={1,2,3,4,5,6,7,8,9}

  for n2 in range(0,len(temp_State[no_of_rows])):
    if n2==no_of_columns:
      continue
    if temp_State[no_of_rows][n2]!='x':
      #Row Checking
      numerical_set2.add(int(temp_State[no_of_rows][n2]))  

  for n1 in range(0,len(temp_State)):
    if n1==no_of_rows:
      continue
    if temp_State[n1][no_of_columns]!='x':
      #Column Checking 
      numerical_set2.add(int(temp_State[n1][no_of_columns]))  

  for n1 in range((no_of_rows//3)*3,(no_of_rows//3)*3+3):
    for n2 in range((no_of_columns//3)*3,(no_of_columns//3)*3+3):
      if n1==no_of_rows and n2==no_of_columns:
        continue
      if temp_State[n1][n2]!='x':
        #Sub Grid Checking 
       numerical_set2.add(int(temp_State[n1][n2]))   

  numerical_set3 = numerical_set1.difference(numerical_set2)  
  return numerical_set3

"""## Individual Rankings"""

def Function_for_rankingIndividuals(individuals):

  def fitness_function(state):
    Estimate=0
    for p in range(0,9):
      for q in range(0,9):
        set_1 = Function_for_SuitNo(state,p,q)
        if int(state[p][q]) in set_1:
          Estimate+=1
    return Estimate

  return sorted([(i,fitness_function(i)) for i in individuals],key = lambda x:x[1],reverse=True)  

def Selection_function(fitness_values):
  outcome=0
  for i in range(0,len(fitness_values)):
    outcome+=fitness_values[i][1]
  selected_list=[]
  for i in range(0,len(fitness_values)):
    selected_list.append(int((fitness_values[i][1]/outcome)*100))

  return selected_list

"""## Crossover function"""

def Crossover_function(pos1,pos2):
  token = random.randint(1,7)
  pos3 = pos1[:token] + pos2[token:]
  pos4 = pos2[:token] + pos1[token:]
  return pos3,pos4

"""## Mutation """

def Function_for_mutation(temp_state,non_replaced):
  while True:
    token1 = random.randint(0,8)
    token2 = random.randint(0,8)
    if (token1,token2) in non_replaced:
      continue
    set_1 = Function_for_SuitNo(temp_state,token1,token2)
    if len(set_1)==0:  
      set_1={1,2,3,4,5,6,7,8,9}
    break
  tokens = random.randint(0,len(set_1)-1)
  temp_state[token1] = temp_state[token1][0:token2]+str(list(set_1)[tokens])+temp_state[token1][token2+1:]

"""## RandomStartPopulation function"""

def Function_for_randomStartPopulation(Starting_state,n):
  no_of_people=[]
  for p in range(0,n):
    temp_state = Starting_state.copy()
    for q in range(0,9):
      for r in range(0,9):
        if Starting_state[q][r]=='x':
          set_1 = Function_for_SuitNo(temp_state,q,r)
          if len(set_1)==1:
            tokens = 0
          else:
            if len(set_1)==0:
              set_1={1,2,3,4,5,6,7,8,9}  
            tokens = random.randint(0,len(set_1)-1)
          temp_state[q] = temp_state[q][0:r]+str(list(set_1)[tokens])+temp_state[q][r+1:]      
    no_of_people.append(temp_state)

  return no_of_people  

def Function_for_nonReplacedStates(Starting_state):
  record1=[]
  for q in range(0,9):
    for r in range(0,9):
      if Starting_state[q][r]!='x':
        record1.append((q,r))
  return record1

"""## RandomSelect function"""

def function_for_randomSelect(select):
  token = random.randint(0,100)
  i = 0
  for i in range(0,len(select)):
    token-=select[i]
    if token<0:
      break
  return i    

number=100
non_replaced_states = Function_for_nonReplacedStates(startingState)
population = Function_for_randomStartPopulation(startingState,number)
new_population = population.copy()

x=1000
total_population = []
pop=0

for p in range(0,x):
  successor_population = Function_for_rankingIndividuals(new_population)
  choices = Selection_function(successor_population)
  upcoming_generation=[]

  if successor_population[0][1]==81:
    pop=1
    print(successor_population[0][0],successor_population[0][1])
    break

  for p in range(0,number//2):
    token1 = function_for_randomSelect(choices)
    token2 = function_for_randomSelect(choices)
    k1,k2 = Crossover_function(successor_population[token1][0],successor_population[token2][0])
    upcoming_generation.append(k1)
    upcoming_generation.append(k2)

  for n1 in upcoming_generation:
    Function_for_mutation(n1,non_replaced_states)
  
  new_population = upcoming_generation
  total_population = Function_for_rankingIndividuals(new_population)

print("The best 5 individual-states from the final population are : ")
print(" ")
if pop==0:
  for p in range(0,5):
    print(total_population[p][0]," fitness value: ",total_population[p][1])

"""## Printing Best 5 Individual states as a Sudoku grid"""

print("The best 5 individual-states from the final population as a Sudoku Grid : ")
print(" ")
if pop==0:
  for p in range(0,5):
    for q in range(len(total_population[0][0])):
        [print(total_population[p][0][q][k],end=' ') for k in range(9)]
        print()
    print("Fitness value: {}\n".format(total_population[p][1]))

"""# **Problem 2**
# **Solving function using Genetic Algorithm**
"""

fun = input("Enter the function :")
fun = fun.replace("^","**")
print("Enter a range of values seperated by space : ",end="")
p,q = input().split()
p = int(p)
q = int(q)
nums = len(bin(q).replace("0b",""))
numerical_set2 = set(range(p,q+1))  # all equations involving 2 varaiables x and y

#Function = "x**2-2*y+3"
#numerical_set2={0,1,2,3,4,5,6,7}

"""## Conversion of Integer to Binary"""

def function_for_intToBin(a,number):
  outcome = bin(a).replace("0b","")
  if len(outcome)==3:
    return outcome
  else:
    q = number-len(outcome)
    utility=''
    for i in range(0,q):
      utility+='0'
    outcome = utility+outcome
    return outcome

"""## Crossover, Mutation and Ranking functions"""

def Function(function,x,y):
  code = parser.expr(function).compile()
  return eval(code)

def Function_for_crossover(temp_state1,temp_state2,m):
  tokens = random.randint(0,2*m-1)
  temp_state3 = temp_state1[tokens:] + temp_state2[:tokens]
  temp_state4 = temp_state1[:tokens] + temp_state2[tokens:]
  return temp_state3,temp_state4

def Function_for_mutation(temp_state,m):
  tokens = random.randint(0,(2*m)-1)
  if temp_state[tokens]=='0':
    A='1'
  else:  
    A='0'
  temp_state = temp_state[0:tokens]+A+temp_state[tokens+1:]

def rankingPopulation_function(individuals,function,kk):
  def fitnessFunction(state,function,kk):
    a = state[:kk]
    b = state[kk:]
    a = int(a,2)
    b = int(b,2)
    return Function(function,a,b)
  return sorted([(h,fitnessFunction(h,function,kk)) for h in individuals],key = lambda x:x[1])

"""## RandomSelection Function"""

def function_for_randomStart(nums,first,last,kk):
  no_of_people=[]
  for i in range(0,nums):
    a = random.randint(first,last)
    b = random.randint(first,last)
    outcome = function_for_intToBin(a,kk)
    utility = function_for_intToBin(b,kk)
    result = outcome+utility
    no_of_people.append(result)
  return no_of_people

def function_for_randomSelect(nums,top_population):
   p = random.randint(0,nums-1)
   q = random.randint(0,nums-1)
   if top_population[p][1] < top_population[q][1]:
     return p
   else:
     return q

"""## Minimum Value of Final Population"""

number=10
population = function_for_randomStart(number,p,q,nums)
new_population = population.copy()
x=100

for k in range(0,x):
  successor_population = rankingPopulation_function(new_population,fun,nums)
  upcoming_generation = []

  for l in range(0,number//2):
    token1 = function_for_randomSelect(number,successor_population)
    token2 = function_for_randomSelect(number,successor_population)
    k1,k2 = Function_for_crossover(successor_population[token1][0],successor_population[token2][0],nums)
    upcoming_generation.append(k1)
    upcoming_generation.append(k2)

  for n1 in upcoming_generation:
    Function_for_mutation(n1,nums)  

  new_population = upcoming_generation.copy()
  total_population = rankingPopulation_function(new_population,fun,nums)

for p in range(0,5):
  print("For",total_population[p][0],"The Minimum value of z is :",total_population[p][1])

