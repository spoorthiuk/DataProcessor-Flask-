"""
This file contains all the library functions required by the main file
author:Spoorthi U K
"""

import pandas as pd
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.image('./assets/dataProcessor.png',10,8,15)
        self.ln(15)
    def footer(self):
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10,str(self.page_no()), 0, 0, 'C')

class FileDefinition:

    def __init__(self, input_file_name):
        self.input_file_name = input_file_name
        pass

    def read_csv(self,file_name):
        file_contents = pd.read_csv(file_name)
        return file_contents
    
    def get_shape(self,file):
        rows = file.shape[0]
        cols = file.shape[1]
        return '\nThe file contains \n\
Rows:{}\n\
Columns:{}\n'.format(rows,cols)
    
    def get_columns(self,file_contents):
        for col_id in range(0,len(file_contents.columns)):
            print(file_contents.columns[col_id])

    def get_column_description(self,file_contents):
        col_desc = {}
        for col in file_contents.columns:
            if col not in col_desc.keys():
                col_desc[col] = {}
                isna_col = file_contents[col].isna()
            print('{}:'.format(col))
            for row_id in range(0,len(file_contents[col])):
                row = file_contents[col][row_id]
                row_data_type = str(type(row).__name__)
                if row_data_type not in col_desc[col].keys():
                    col_desc[col][row_data_type] = 0
                if 'is_na' not in col_desc[col].keys():
                    col_desc[col]['is_na'] = 0
                if(isna_col[row_id] == True):
                    col_desc[col]['is_na'] +=1
                else:
                    col_desc[col][row_data_type] += 1
            for col_data_type in col_desc[col].keys():
                print('{}:{}'.format(col_data_type,col_desc[col][col_data_type]))
        return col_desc
            
    def get_column_analysis(self,column_description):
        column_analysis = {}
        for col in column_description.keys():
            column_analysis[col] = {}
            print(fontFormater(text_color='purple'),'{}:'.format(col),fontFormater())
            reason = ''
            if column_description[col]['is_na'] > 0:
                reason += 'The column contains {} null values. '.format(column_description[col]['is_na'])
            
            if len(column_description[col].keys()) > 2:
                reason += 'The column contains {} different data types. '.format(len(column_description[col].keys())-1)
            
            if len(column_description[col].keys()) == 1:
                reason += 'The column contains only null values'

            if(reason == ''):
                print(fontFormater(text_color='green'),'The column clears the analysis!',fontFormater())
                column_analysis[col]['green'] = 'The column clears the analysis!'
            else:
                print(fontFormater(text_color='red'),reason,fontFormater())
                column_analysis[col]['red'] = reason
        return column_analysis

    def print_table_elements(self,file_contents,no_of_rows,pdf):
        MARGIN = 10
        head_elements = file_contents.head(no_of_rows)
        columns = head_elements.columns
        #Printing the columns
        #The page is divided in such a way that maximum number of columns can be fit . Any additional columns will be printed after the rows of the previous columns have been printed
        #Defining width of each column
        row_len = 0
        cur_no_of_cols = 0
        cur_col = 0
        cur_col_width = []
        col_data_printed = []
        #Define how many tables are required per page
        number_of_tables_per_page = 3
        for col_entry in columns:
            row_len_lis = []
            row_len_lis.append(len(col_entry))
            #Get the length of each row for a column to decide on the width of the column i.e 5 times the maximumn row length
            for row in head_elements[col_entry]:
                if(type(row)==str):
                    row_len_lis.append(len(row))
                else:
                    row_len_lis.append(1)
            max_col_len = max(row_len_lis)
            col_width = max_col_len*5
            if(col_width > 210-2*MARGIN):
                col_width = 210-2*MARGIN
            row_len += col_width
            #Print the column headers
            if(row_len <= 210-2*MARGIN):
                cur_no_of_cols += 1
                col_width = max_col_len*5
                if(col_width > 210-2*MARGIN):
                    col_width = 210-2*MARGIN
                cur_col_width.append(col_width)
                pdf.set_font('Arial','B', 10)
                pdf.cell(w=col_width,h = 10,txt=col_entry,border=1,align='C')
            #Print the rows of the columns printed previously    
            if row_len > 210-2*MARGIN:
                pdf.ln()
                for row_id in range(0,no_of_rows):
                    for col_id in range(cur_col,len(cur_col_width)+cur_col):
                        if(columns[col_id] not in col_data_printed):
                            col_data_printed.append(columns[col_id])
                        pdf.set_font('Arial','', 10)
                        pdf.cell(w=cur_col_width[col_id-cur_col],h = 10,txt=str(file_contents[columns[col_id]][row_id]),border=1,align='C')
                    pdf.ln()
                cur_col +=cur_no_of_cols
                cur_no_of_cols = 0
                cur_col_width = []
                row_len = 0
                number_of_tables_per_page -= 1
                if(number_of_tables_per_page > 0):
                    pdf.ln()
                else:
                    pdf.add_page()
                    #pdf.ln(15)
                    number_of_tables_per_page=3
                cur_no_of_cols += 1
                col_width = max_col_len*5
                if(col_width > 210-2*MARGIN):
                    col_width = 210-2*MARGIN
                cur_col_width.append(col_width)
                pdf.set_font('Arial','B', 10)
                pdf.cell(w=col_width,h = 10,txt=col_entry,border=1,align='C')
                row_len += col_width
            
            if col_entry == columns[-1] and col_entry not in col_data_printed:
                pdf.ln()
                for row_id in range(0,no_of_rows):
                    for col_id in range(cur_col,len(cur_col_width)+cur_col):
                        if(columns[col_id] not in col_data_printed):
                            col_data_printed.append(columns[col_id])
                        pdf.set_font('Arial','', 10)
                        pdf.cell(w=cur_col_width[col_id-cur_col],h = 10,txt=str(file_contents[columns[col_id]][row_id]),border=1,align='C')
                    pdf.ln() 
    
    def print_column_description_and_analysis(self, file_contents, pdf):
        column_description = self.get_column_description(file_contents=file_contents)
        for column in column_description.keys():
            pdf.set_font('Arial','B', 10)
            pdf.cell(w= 0, h= 10, txt= '{}:'.format(column), align= 'L',ln=1)
            for data_type in column_description[column].keys():
                pdf.set_font('Arial','', 10)
                pdf.cell(w= 0, h= 10, txt= '{}:{}'.format(data_type,str(column_description[column][data_type])), align= 'L',ln=1)
        #Get the column analysis
        pdf.set_font('Arial','B', 15)
        pdf.cell(w= 0, h= 10, txt= 'Column Analysis', align= 'L') 
        pdf.ln(15)
        self.print_column_analysis(column_description=column_description,pdf=pdf)

    def print_column_analysis(self,column_description, pdf):
        column_anaysis = self.get_column_analysis(column_description=column_description)
        for column in column_anaysis.keys():
            pdf.set_font('Arial','B', 10)
            pdf.set_text_color(r= 0, g= 0, b = 0) 
            pdf.cell(w= 0, h= 10, txt= '{}:'.format(column), align= 'L',ln=1)
            if('red'in column_anaysis[column].keys()):
                pdf.set_font('Arial','', 10)
                pdf.set_text_color(r= 100, g= 0, b = 0) 
                pdf.cell(w= 0, h= 10, txt= '{}'.format(column_anaysis[column]['red']), align= 'L',ln=1)
            else:
                pdf.set_font('Arial','', 10)
                pdf.set_text_color(r= 0, g= 100, b = 0) 
                pdf.cell(w= 0, h= 10, txt= '{}'.format(column_anaysis[column]['green']), align= 'L',ln=1)
    
    def generate_data_summary(self,file_contents):
        pdf = PDF()
        pdf.add_page()  
        pdf.set_text_color(r= 38, g= 0, b = 77)  
        pdf.set_font('Arial','B', 20)
        #Print the document header
        pdf.cell(w= 0, h= 10, txt= 'Data Report', align= 'C') 
        #Print the data sample
        pdf.ln(15)
        #Resetting the font color back to black
        pdf.set_text_color(r= 0, g= 0, b = 0)  
        pdf.set_font('Arial','B', 15)
        pdf.cell(w= 0, h= 10, txt= 'Data Preview', align= 'L') 
        pdf.ln(15)
        #Getting head elements
        pdf.set_font('Arial','B', 10)
        no_of_rows = 5
        self.print_table_elements(file_contents=file_contents ,no_of_rows=no_of_rows,pdf=pdf)
        pdf.ln()
        #Get the column Description and analysis
        pdf.set_font('Arial','B', 15)
        pdf.cell(w= 0, h= 10, txt= 'Column Description', align= 'L') 
        pdf.ln(15)
        self.print_column_description_and_analysis(file_contents=file_contents,pdf=pdf)
        output_file = '.\\pdf_files\\'+self.input_file_name.split('\\')[-1].split('.')[0]+'.pdf'
        print(output_file)
        pdf.output(output_file, 'F')

     


def fontFormater(style = 'normal',text_color = 'white', bg_color= 'black'):
    """This function will help us style our command line output
    The text is formatted with the help of ANSI code"""
    switch_style = {
        'normal': '0',
        'bold' : '1',
        'light' : '2',
        'italic' : '3',
        'underline' : '4',
        'blink' : '5'
    }

    switch_text_color = {
        'black' : '30',
        'red' : '31',
        'green' : '32',
        'yellow' : '33',
        'blue' : '34',
        'purple' : '35',
        'cyan' : '36',
        'white' : '37'
    }

    switch_bg_color ={
        'black' : '40',
        'red' : '41',
        'green' : '42',
        'yellow' : '43',
        'blue' : '44',
        'purple' : '45',
        'cyan' : '46',
        'white' : '47'
    }

    assert style in switch_style.keys(), 'ASSERT FAIL: An error occured when formatting the text. Unexpected style argument encountered'
    assert text_color in switch_text_color.keys(), 'ASSERT FAIL: An error occured when formatting the text. Unexpected text_color argument encountered'
    assert bg_color in switch_bg_color.keys(), 'ASSERT FAIL: An error occured when formatting the text. Unexpected bg_color argument encountered'

    style_code = switch_style.get(style)
    text_color_code = switch_text_color.get(text_color)
    bg_color_code = switch_bg_color.get(bg_color)
    ansi_code = '\033[{};{};{}m'.format(style_code,text_color_code,bg_color_code)
    return ansi_code
