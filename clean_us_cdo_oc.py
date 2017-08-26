# -*- coding: utf-8 -*-

import csv
import re
# The convention of importing pandas is `import pandas as pd`
import pandas as pd
from pandas import DataFrame


#open csv file created by tabula
filename = r'input.csv'
csv_file=open(filename, 'rb')
reader = csv.reader(csv_file)

#extracting all table fields to nested list from csv file

list_of_fields = []

for row in reader:
    if row[0] == '':
        break
    else:
        list_of_fields.append(row)




#all fields in the first column

column_1 = [row[i] for row in list_of_fields for i in range(1)]

#create list of tranches' names

list_of_names=[]

for i in list_of_fields[0][1:]:
    namesRegex = re.search(r'Class +(\w+(-\w+)?) +Notes', i)
    if str(i).startswith('Sub'):
        list_of_names.append('SUB')
    elif namesRegex:
        list_of_names.append(namesRegex.group(1).replace('-', ''))
    else:
        print "Unexpected column name {}".format(i)





#create list of tranches' currencies

list_of_currencies=(len(list_of_names))*['USD']



#create list of tranches' Fixing to deal currencies

list_of_fxrate = (len(list_of_names))*['1']



# create list of tranches' types

list_of_types = (len(list_of_names))*['Standard']


# create list of tranches' coupon frequencies

list_of_cfreq = (len(list_of_names))*['Quarterly']

# create list of tranches' deferral statuses

list_of_deferral=[]

index_of_deferral = [i for i, item in enumerate(column_1) if re.search(r'.*Def', item)]


for i in list_of_fields[index_of_deferral[0]][1:]:
    if i == 'No':
        list_of_deferral.append('NO')
    elif i == 'Yes':
        list_of_deferral.append('PIK')
    else:
        list_of_deferral.append('N/A')


# create list of tranches' original amounts

list_of_balances = []

index_of_balances = [i for i, item in enumerate(column_1) if re.search(r'\w*(Amount)|(Principal)\w*', item)]


for i in list_of_fields[index_of_balances[0]][1:]:
#    balance = re.search(r'\w*(((\d{3}(.)?)|(\d{2}(.)?)|(\d(.)?))+)\w*', i)
    parsed_number_list = re.findall('[^A-Za-z%$]+', i.replace(',',''))
    if len(parsed_number_list) !=1:
        raise IOError("Cannot parse number {}".format(i))
    parse_number = parsed_number_list[0]
    list_of_balances.append(parse_number)





# create list of tranches' Moody's ratings

rating_Moodys = []

index_Moodys = [i for i, item in enumerate(column_1) if re.search(r'\w*Mood', item)]
if len(index_Moodys)==0:
    rating_Moodys = (len(list_of_names)*[''])
else:
    for i in list_of_fields[index_Moodys[0]][1:]:
        if i == 'N/A':
            rating_Moodys.append('')
        else:
            moodys = re.search(r'[^\u0000-\u007F]+(\w+)', i)
            rating_Moodys.append(moodys.group(1))



# create list of tranches' S&P ratings

rating_SP = []

index_SP = [i for i, item in enumerate(column_1) if re.search(r'\w*S&P', item)]

if len(index_SP)==0:
    rating_SP = (len(list_of_names)*[''])
elif len(index_SP) == 1:
    for i in list_of_fields[index_SP[0]][1:]:
        if i == 'N/A':
            rating_SP.append('')
        else:
            sp = re.search(r'[^\u0000-\u007F]+(\w+(\+|-)?)', i)
            rating_SP.append(sp.group(1))
else:
    print "Unexpected number of SnP columns: {}".format(index_SP)





# create list of tranches' Fitch ratings

rating_Fitch = []

index_Fitch =  [i for i, item in enumerate(column_1) if re.search(r'\w*Fitch', item)]

if len(index_Fitch)==0:
    rating_Fitch = (len(list_of_names)*[''])
else:
    for i in list_of_fields[index_Fitch[0]][1:]:
        if i == 'N/A':
            rating_Fitch.append('')
        else:
            fitch = re.search(r'[^\u0000-\u007F]+(\w+(\+|-)?(sf))', i)
            rating_Fitch.append(fitch.group(1))





# create list of tranches' coupon types

list_of_coupon_type = []

index_ctype1 = [i for i, item, in enumerate(column_1) if re.search(r'\w*(Type)', item)]


for i in list_of_fields[index_ctype1[0]][1:]:
    if re.search(r'.*Float', i):
        list_of_coupon_type.append('floating')
    elif re.search(r'.*Fixed', i):
        list_of_coupon_type.append('fixed')
    else:
        list_of_coupon_type.append('variable')



# create list of tranches' Spreads and coupons
list_of_spreads = []
list_of_coupons = []

index_spread = [i for i, item, in enumerate(column_1) if re.search(r'\w*(Rate)', item)]

for i in list_of_fields[index_spread[0]][1:]:
    spread = re.search(r'.*LIBOR.*(\d+\.\d+)', i)

    if spread is not None:
        list_of_spreads.append(spread.group(1))
    else:
        list_of_spreads.append('')


for i in list_of_fields[index_spread[0]][1:]:
    coupon = re.search(r'^\d+\.\d+', i)
    if coupon is not None:
        list_of_coupons.append(coupon.group())
    else:
        list_of_coupons.append('')




# create list of tranches' rankings

list_of_rankings = []

index_ranking = [i for i, item in enumerate(column_1) if re.search(r'\w*Pari\w*', item)]


#list_of_rankings.append('1')

for i in list_of_fields[index_ranking[0]][1:len(list_of_fields[index_ranking[0]])-1]:
    if i == 'None':
        list_of_rankings.append(int(list_of_rankings[(len(list_of_rankings) - 1)]) + 1)

    else:
        if list_of_fields[index_ranking[0]][len(list_of_rankings)+1] == 'None':
            list_of_rankings.append(int(list_of_rankings[(len(list_of_rankings) - 1)]) + 1)
        else:
            list_of_rankings.append(int(list_of_rankings[(len(list_of_rankings) - 1)]))

#rankings = []
#initial = True
#for i, j in enumerate(paripasu):
#    if initial:
#        rankings.append(1)
#        initial = False
#    elif j == 'None' or paripasu[i-1] == 'None':
#        rankings.append(rankings[-1]+1)
#    elif paripasu[i-1] != 'None':
#        rankings.append(rankings[-1])

# create list of tranches' Current Coupons, Original wals

list_of_ccoupons = (len(list_of_names))*['']
list_of_wals =(len(list_of_names))*['']



print  list_of_rankings
frame = {'Ranking': list_of_rankings, 'Tranche type': list_of_types, 'Interest deferral': list_of_deferral, 'Fixing to deal currency': list_of_fxrate,\
        'Name': list_of_names, 'Currency' : list_of_currencies, 'Original amount': list_of_balances, 'Initial ratings (M)': rating_Moodys,\
         'Initial ratings (SNP)': rating_SP, 'Initial ratings (F)': rating_Fitch, 'Coupon type': list_of_coupon_type, 'Spread': list_of_spreads,
         'Coupon': list_of_coupons, 'Current Coupon': list_of_ccoupons, 'Coupon frequency': list_of_cfreq, 'Original wal': list_of_wals}
data = DataFrame(frame, columns=['Ranking','Tranche type', 'Interest deferral', 'Fixing to deal currency', 'Name', 'Currency', 'Original amount', 'Initial ratings (M)', 'Initial ratings (SNP)', 'Initial ratings (F)',\
'Coupon type', 'Spread', 'Coupon', 'Current Coupon', 'Coupon frequency', 'Original wal'])



data.to_csv('C:\Users\Anoush Atayan\Desktop\My_First_Project.csv', index = False)

