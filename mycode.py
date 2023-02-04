import csv
import sys
import pandas as pd

def spend_points(spend_amount):
    
    df = pd.read_csv('transactions.csv') #reading the csv file into a dataframe
    df.sort_values(by='timestamp', inplace=True) #sorting the values by timestamp
    df.to_csv('transactions.csv', index=False) #writing back the sorted csv

    dicti = {} #dictionary to store the final output for each payer
    total = {} #dictionary to store the total positive points for each payer 
    
    with open('transactions.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader) #ignoring the column headings
        for row in reader:
            payer = row[0]
            points = int(row[1])
            
            if payer not in dicti:
                #If the first transaction for a payer has negative points, Stop excecution as payers points cant be negative
                if points<0:
                    print("Payer's points are negative. cannot continue") 
                    break
                dicti[payer] = points #appending dicti with the new payer's points
                total[payer] = points if points>0 else 0 #appending dicti with the new payer's points
            else:
                #updating dicti and total if payer is already in dicti
                dicti[payer]+= points 
                total[payer]+= points if points>0 else 0
            
            '''the below code will execute only if the spend_amount is not zero otherwise 
            the payer's points will be updated in the dictionary for the remaining transactions'''
            
            if spend_amount != 0:
                #If the payer's points go negative, bringing it to 0 using their total positive points so far
                if dicti[payer] <= 0:
                    if(total[payer] > abs(points)):
                        dicti[payer]-= abs(points)
                        spend_amount-= abs(points)
                if dicti[payer] >= spend_amount:
                    dicti[payer] -= spend_amount
                    spend_amount = 0
                else:
                    spend_amount -= dicti[payer]
                    dicti[payer] = 0

    return dicti

if __name__ == '__main__':
    spend_amount = int(sys.argv[1]) #amount to be spent
    result = spend_points(spend_amount)
    print(result)




