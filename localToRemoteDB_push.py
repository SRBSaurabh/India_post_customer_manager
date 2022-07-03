import psycopg2, sqlite3

host_DB = "ec2-52-70-166-10.compute-1.amazonaws.com"
name_DB = "dem4e8kaaf14pq"
user_DB = "cfpcamkwtqywes"
pass_DB = "b5d7b25f839337eec19373c5209be043ad574f018a5c07b71e62dec36a442f4a"


def localToRemoteDB():
    """ This Will Sink Our India Post Portal Data with Portal_2 data :) :)"""
    
    # Original DB-1
    conn1 = sqlite3.connect('Portal_Data.sqlite')  
    cur1 = conn1.cursor()
    Orig_data = cur1.execute('SELECT Account_No, Account_Name, Denomination, Opening_Date, Closing_Date, Month_Paid_Upto, '
                        'Total_Return, Pending_Installment, Advance_Installment, Next_Installment_Due_Date FROM Portal')
    
    # New DB-2
    conn2 = psycopg2.connect(database=name_DB, user=user_DB, password=pass_DB, host=host_DB)    
    conn2.autocommit = True
    cur2 = conn2.cursor()

    cur2.execute('DROP TABLE IF EXISTS Portal_2')
    cur2.execute('CREATE TABLE Portal_2 (Account_No VARCHAR(255), Account_Name VARCHAR(255), Denomination INTEGER, Opening_Date VARCHAR(255), '
                    'Closing_Date VARCHAR(255), Month_Paid_Upto INTEGER, Total_Return INTEGER, Pending_Installment VARCHAR(255), '
                    'Advance_Installment VARCHAR(255), Next_Installment_Due_Date VARCHAR(255))')
    conn2.commit()

    args = ','.join(cur2.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", i).decode('utf-8')for i in Orig_data)

    cur2.execute("INSERT INTO Portal_2 VALUES " + (args))
    # cur1.execute(f'''INSERT INTO Portal_2(Account_No, Account_Name, Denomination, Opening_Date, Closing_Date,Month_Paid_Upto, Total_Return, Pending_Installment, Advance_Installment, Next_Installment_Due_Date) VALUES ('{i[0]}','{i[1]}',{i[2]},'{i[3]}','{i[4]}',{i[5]},{i[6]},'{i[7]}','{i[8]}','{i[9]}')''')

    conn2.commit()
    cur1.close()
    cur1.close()

    return("Remotly Portal_2 Updated Successfully..!")


if __name__=="__main__":
    print(localToRemoteDB())
    input()