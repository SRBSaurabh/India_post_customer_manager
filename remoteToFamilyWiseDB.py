import psycopg2, sqlite3

host_DB = "ec2-52-70-166-10.compute-1.amazonaws.com"
name_DB = "dem4e8kaaf14pq"
user_DB = "cfpcamkwtqywes"
pass_DB = "b5d7b25f839337eec19373c5209be043ad574f018a5c07b71e62dec36a442f4a"


def remoteToFamilyWiseDB():
    """ This Will Sink Our India Post Portal Data with Portal_2 data :) :)"""
    
    ## Original DB-1
    conn1 = psycopg2.connect(database=name_DB, user=user_DB, password=pass_DB, host=host_DB) 
    conn1.autocommit = True
    cur1 = conn1.cursor()
    cur1.execute('''SELECT * from Portal_2''')
    Orig_data = cur1.fetchall()
    
    
    ## New DB-2
    conn2 = sqlite3.connect('Family_Wise.sqlite')
    cur2 = conn2.cursor()
    cur2.execute('DROP TABLE IF EXISTS Portal_2')
    cur2.execute('CREATE TABLE Portal_2 (Account_No TEXT, Account_Name TEXT, Denomination INTEGER, Opening_Date TEXT, '
                 'Closing_Date TEXT, Month_Paid_Upto INTEGER, Total_Return INTEGER, Pending_Installment TEXT, '
                 'Advance_Installment TEXT, Next_Installment_Due_Date TEXT)')
    conn2.commit()
    
    for i in Orig_data:
        cur2.execute('INSERT INTO Portal_2 (Account_No, Account_Name, Denomination, Opening_Date, Closing_Date, '
                     'Month_Paid_Upto, Total_Return, Pending_Installment, Advance_Installment, '
                     'Next_Installment_Due_Date) VALUES (?,?,?,?,?,?,?,?,?,?)', i)
        # print(i)

    conn2.commit()
    cur2.close()
    cur1.close()

    print("Server-Seated Portal_2 Updated Successfully..!")
    return "Server-Seated Portal_2 Updated Successfully..!"


if __name__ == "__main__":
    print('inside remoteToFamilyWiseDB')
    # remoteToFamilyWiseDB()
