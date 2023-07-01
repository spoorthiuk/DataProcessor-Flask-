import libraries as lib
from libraries import fontFormater
from flask import Flask, render_template

def main():
    
    print("Welcome to DataProcessor\n\
Please paste the path of a .csv file to begin\n")
    #file_name = input('>')
    ##Test .csv file
    #file_name = r"G:\ML_Projects\American_Express_ML_Challenge\Dataset\test.csv"
    #file_name = r"G:\Self_Projects\IPL_WebScraping\IPL_t3.csv"
    file_name = r"G:\ML_Projects\Datathon\2015.csv"
    File = lib.FileDefinition(file_name)
    print(fontFormater(text_color='blue'),"Fetching contents from {}...".format(file_name),fontFormater())
    file_contents = File.read_csv(file_name=file_name)
    print(fontFormater(text_color='yellow',style='underline'),'Data Preview\n',fontFormater())
    print(fontFormater(text_color='black',bg_color='cyan',style='bold'),file_contents.head(),fontFormater())
    print(fontFormater(text_color='purple'),File.get_shape(file = file_contents),fontFormater())
    print(fontFormater(text_color='yellow',style='underline'),'Columns:',fontFormater())
    File.get_columns(file_contents=file_contents)
    print(fontFormater(text_color='yellow',style='underline'),'\n Column Desctription',fontFormater())
    column_description = File.get_column_description(file_contents = file_contents)
    print(fontFormater(text_color='yellow',style='underline'),'\nColumn Analysis\n',fontFormater())
    File.get_column_analysis(column_description = column_description)
    File.generate_data_summary(file_contents=file_contents)

    
    


main()