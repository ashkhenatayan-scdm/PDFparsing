# -*- coding: utf-8 -*-
"""
Created on Wed May 03 08:25:01 2017

@author: Ashkhen_A
"""
import pandas as pd
import os
import re


def rename_indices(text):
    namesRegex = re.search(r'Class +(\w+(-\w+)?) +Notes', text)
    if text.startswith('Sub'):
        return 'SUB'
    elif namesRegex:
        return namesRegex.group(1).replace('-', '')
    else:
        print "Unexpected column name {}".format(i)
        return "NA"

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

def rename_columns(text):
    col_map = {r'Def': 'Interest deferral', 'Amount': 'Principal', 'Mood': 'Initial ratings (M)', 'S&P': 'Initial ratings (SNP)', 'Fitch': 'Initial ratings (F)', 'Type': 'Coupon type','Rate': 'spread_coupon', 'Pari': 'Ranking'}
    for k, v in col_map.items():
       if k in text:
           return v
       else:
           return 'NONE'
# def rename_columns(text):
#     if 'Def' in text:
#         return 'Interest deferral'
#     elif 'Amount' in text or 'Principal' in text:
#         return 'Original amount'
#     elif 'Mood' in text:
#         return 'Initial ratings (M)'
#     elif 'S&P' in text:
#         return 'Initial ratings (SNP)'
#     elif 'Fitch' in text:
#         return 'Initial ratings (F)'
#     elif 'Type' in text:
#         return 'Coupon type'
#     elif 'Type' in text:
#         return 'Coupon type'
#     elif 'Rate' in text:
#         return 'spread_coupon'
#     elif r'Pari' in text:
#         return 'Ranking'
#     else:
#         return 'NONE'

if __name__ == "__main__":
    df = pd.read_csv(r'C:\Users\Ashkhen_A\Downloads\input.csv' )
    for column in df:
        if 'Unnamed' in column:
            df = df.drop(column, axis=1)
    s = df.ix[:, 0]
    df = df.set_index(s)

    for n, i in enumerate(df.index.tolist()):
        if str(i) == 'nan':
            break
    df = df.iloc[:n, :]
    df = df.T
    df = df.drop(df.index[0])
    df.index = df.index.map(rename_indices)
    df['Currency'] = 'USD'
    df['Fixing to deal currency'] = '1'
    df['Coupon frequency'] = 'Quarterly'
    df['Tranche type'] = 'Standard'
    df.columns = map(rename_columns,df.columns)
    df = df[[i for i in df.columns if i != 'NONE']]

    assert len(df.columns) == len(set(df.columns.tolist())), "Unexpected case when renaming columns"

    df['Ranking'] = set_rankings(df['Ranking'])
    print df






