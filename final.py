# pip install PyMuPDF
import fitz

def extract_statement_info(pdf_file_path, password=None):
    MyFile = fitz.open(pdf_file_path)

    if MyFile.metadata is None and password:
        # password = input()
        MyFile.authenticate(password)

    page = MyFile.load_page(0)

    account_details = extract_account_info(page)
    transection_table = extract_table_info(page)
    account_summary = extract_account_summary(page)

    # print(search_key_in_table(transection_table, 'DATE'))
    
    statement = {
        'Account details' : account_details,
        'Transection table': transection_table,
        'Account Summery': account_summary
    }

    return statement

def extract_table_info(data):
    table = data.find_tables()
    if table.tables:
        tableData = table[0].extract()
        return tableData
    return []

def extract_account_info(data):
    text = data.get_text()
    array = text.split('\n')
    account_details = []

    for i in range(len(array)):
        if ('DATE' or 'Date') in array[i]:
            break 
        if ':' in array[i]:
            account_details.append(array[i-1]+' '+array[i])
    return account_details

def extract_account_summary(data):
    text = data.get_text()
    array = text.split('\n')
    flag = False
    account_summary = []

    for i in range(len(array)):
        if 'End' in array[i]:
            break
        if ('DATE' or 'Date') in array[i]:
            flag = True
        if ':' in array[i] and flag:
            account_summary.append(array[i])
    return account_summary

# If need any searching
def search_key_in_table(table, key):
    # Iterate through each row in the table
    for row in table:
        if key in row:
            return row
    return None

if __name__ == '__main__':
    pdf_file_path = '1781XXXXXX179.pdf'
    password = '1781500115179' 
    result = extract_statement_info(pdf_file_path, password)
    print(result)