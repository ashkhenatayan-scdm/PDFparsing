# -*- coding: utf-8 -*-
import re
import pandas as pd

def rename_indices(text):
    namesRegex = re.search(r'Class +(\w+(-\w+)?) +Notes', text)
    if text.startswith('Sub'):
        return 'SUB'
    elif namesRegex:
        return namesRegex.group(1).replace('-', '')
    else:
        print "Unexpected column name {}".format(i)
        return "NA"


def rename_columns(text):
#    col_map = {'Def': 'Interest deferral',
#               }
#    for k, v in col_map.items():
#        if k in text:
#            return v
#    return 'NONE'
    if 'Def'in text:
        return 'Interest deferral'
    elif 'Amount' in text or 'Principal' in text:
        return 'Original amount'
    elif 'Mood' in text:
        return 'Initial ratings (M)'
    elif 'S&P'in text:
        return 'Initial ratings (SNP)'
    elif 'Fitch' in text:
        return 'Initial ratings (F)'
    elif 'Type' in text:
        return 'Coupon type'
    elif 'Type' in text:
        return 'Coupon type'
    elif 'Rate' in text:
        return 'spread_coupon'
    elif r'Pari' in text:
        return 'Ranking'
    else:
        return 'NONE'

def set_rankings(l):
    rankings = []
    initial = True
    for i, j in enumerate(l):
        if initial:
            rankings.append(1)
            initial = False
        elif j == 'None' or l[i-1] == 'None':
            rankings.append(rankings[-1]+1)
        elif l[i-1] != 'None':
            rankings.append(rankings[-1])
    return rankings
    

if __name__ == "__main__":
    df = pd.read_csv('input.csv', index_col=0)
    
    for n, i in enumerate(df.index.tolist()):
        if str(i) == 'nan':
            break
    
    df = df.iloc[:n,:]
    
    df = df.T
    
    df.index = df.index.map(rename_indices)

    df = df.applymap(lambda x: x.replace('\r', ' ').strip('\xe2\x80\x9c\xe2\x80\x9d') if type(x) == str else x)

    df['Currency'] = 'USD'
    
    df.columns = df.columns.map(rename_columns)

    df = df[[i for i in df.columns if i !='NONE']]

    assert len(df.columns) == len(set(df.columns.tolist())), "Unexpected case when renaming columns"
    
    df['Ranking'] = set_rankings(df['Ranking'])

    # TODO: PARSE FLOAT/FIX
    
    # TODO: POPULATE coupon/spread columns
#    df['coupon'] = ''
#    df['spread'] = ''
#    df['coupon'].mask(df['Ranking'] > 3 , df['spread_coupon'], inplace=True)
