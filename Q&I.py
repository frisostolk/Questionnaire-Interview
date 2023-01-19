# Filename Q&I.py
# Description: Changing the questionnaire results in something readable
# Date: 14-01-2022
# Author: F.R.P. Stolk


# Libraries

import pandas as pd
import numpy as np


def calculate_averages(df):
    """ Performing calculations to calculate means per group and overall + extreme and neutral answers """

    # Counting all the given answers
    df["5"] = df[df == 5].T.count()
    df["7"] = df[df == 7].T.count()
    df["1"] = df[df == 1].T.count()
    df["3"] = df[df == 3].T.count()
    df["4"] = df[df== 4].T.count()

    # calculate mean per group
    df['meanA'] = df[["A1", "A2", "A3", "A4", "A5", "A6", "A7"]].mean(axis=1, skipna=True)
    df['meanB'] = df[["B1", "B2", "B3", "B4", "B5"]].mean(axis=1, skipna=True)
    df['meanBI'] = df[["BI1",  "BI2", "BI3", "BI4", "BI5"]].mean(axis=1, skipna=True)
    df['meanPE'] = df[["PE1",  "PE2", "PE3", "PE4", "PE5", "PE6"]].mean(axis=1, skipna=True)
    df['meanSN'] = df[["SN1",  "SN2", "SN3", "SN4", "SN5", "SN6", "SN7"]].mean(axis=1, skipna=True)
    df['meanTotal'] = df[["A1", "A2", "A3", "A4", "A5", "A6", "A7","B1", "B2", "B3", "B4", "B5","BI1",  "BI2", "BI3", "BI4", "BI5","PE1",  "PE2", "PE3", "PE4", "PE5", "PE6","SN1",  "SN2", "SN3", "SN4", "SN5", "SN6", "SN7"]].mean(axis=1, skipna=True)

    # calculating age basis on year
    df["D2"] =  2023 - df["D2"] 


    # Rewriting Mean per group for 7 to match with 5 point likert scale
    df.loc[df['Column'] == 7, 'meanA'] = df['meanA'] * (5/7)
    df.loc[df['Column'] == 7, 'meanTotal'] = df['meanTotal'] * (5/7)
    df.loc[df['Column'] == 7, 'meanB'] = df['meanB'] * (5/7)
    df.loc[df['Column'] == 7, 'meanBI'] = df['meanBI'] * (5/7)
    df.loc[df['Column'] == 7, 'meanPE'] = df['meanPE'] * (5/7)
    df.loc[df['Column'] == 7, 'meanSN'] = df['meanSN'] * (5/7)

    # Rewriting extreme answers
    mask = df["Column"] == 5
    df.loc[mask, "Extreme"] = df["5"]

    mask = df["Column"] == 7
    df.loc[mask, "Extreme"] = df["7"]

    df["Extreme"] = df["Extreme"] + df["1"]

    # Rewriting Neutral answers
    mask = df["Column"] == 5
    df.loc[mask, "Neutral"] = df["3"]

    mask = df["Column"] == 7
    df.loc[mask, "Neutral"] = df["4"]

    return df


def main():
    """ Main Function to read CSV and rewriting to be readable in R """

    # import csv
    file = pd.read_csv("results6.csv", header=0)
    columns = file.columns.tolist()

    # Loop through all columns and rewrite written answer to numbers
    for column in columns:
        file.loc[file[column] == "Helemaal oneens", column] = 1
        file.loc[file[column] == "Oneens", column] = 2
        file.loc[(file[column] == "Neutraal") & (file["Column"] == 5) , column] = 3
        file.loc[(file[column] == "Eens") & (file["Column"] == 5) , column] = 4
        file.loc[(file[column] == "Helemaal eens") & (file["Column"] == 5) , column] = 5
        file.loc[(file[column] == "Helemaal Eens") & (file["Column"] == 5) , column] = 5

        file.loc[(file[column] == "Enigszins oneens") & (file["Column"] == 7) , column] = 3
        file.loc[(file[column] == "Neutraal") & (file["Column"] == 7) , column] = 4
        file.loc[(file[column] == "Enigszins eens") & (file["Column"] == 7) , column] = 5
        file.loc[(file[column] == "Eens") & (file["Column"] == 7) , column] = 6
        file.loc[(file[column] == "Helemaal eens") & (file["Column"] == 7) , column] = 7

    # Peform calculations
    file = calculate_averages(file)

    # Save file to csv
    file.to_csv("output.csv", index = False)



if __name__ == '__main__':
    main()