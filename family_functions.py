from datetime import datetime, date
from secret import host_DB, name_DB, user_DB, pass_DB
import pandas as pd
import time
import psycopg2


cal = {"01":"Jan",
        "02":"Feb",
        "03":"Mar",
        "04":"Apr",
        "05":"May",
        "06":"Jun",
        "07":"Jul",
        "08":"Aug",
        "09":"Sep",
        "10":"Oct",
        "11":"Nov",
        "12":"Dec"}
MM = cal[datetime.now().strftime("%m")]
YYYY = datetime.now().strftime("%Y")


class CustomersDB():
    """ Customers is our Collections Recorder DB"""
    MM = datetime.now().strftime("%m")
    YYYY = datetime.now().strftime("%Y")

    global host_DB, name_DB, user_DB, pass_DB

    conn = psycopg2.connect(database=name_DB, user=user_DB, password=pass_DB, host=host_DB)    
    conn.autocommit = True
    cur = conn.cursor()

    def insert(fname, regAmt, monthUpto, pendAmt, extraAmt, Note, cur=cur, conn=conn):
        cur.execute(f'''INSERT INTO customers (fname, regAmt, monthUpto, pendAmt, extraAmt, Note, date_created) VALUES ('{fname}', '{regAmt}', '{monthUpto}', '{pendAmt}', '{extraAmt}', '{Note}', '{date.today()}')''')
        conn.commit()
        return "Inserted Successfully..!!"

    def delete(sno, cur=cur, conn=conn):
        cur.execute(f'DELETE FROM customers WHERE sno = {sno}')
        conn.commit()
        return "Deleted Successfully..!!"

    def update(sno, regAmt, monthUpto, pendAmt, extraAmt, Note, cur=cur, conn=conn):
        cur.execute(f'''UPDATE customers SET (regAmt, monthUpto, pendAmt, extraAmt, Note) = ('{regAmt}', '{monthUpto}', '{pendAmt}', '{extraAmt}', '{Note}') WHERE sno = {sno};''')
        conn.commit()
        return "Updated Successfully..!!"

    def filter(sno, cur=cur):
        cur.execute(f'SELECT fname, regAmt, monthUpto, pendAmt, extraAmt, Note FROM customers WHERE sno = {sno}')
        result = cur.fetchone()
        return result

    def showThisMonth(mm=datetime.now().strftime("%m"), cur=cur):   
        cur.execute(f"SELECT fname, regAmt, monthUpto, pendAmt, extraAmt, Note, date_created, sno FROM customers WHERE substring(date_created,1,4)='{YYYY}' and substring(date_created,6,2)='{mm}' ORDER BY sno DESC")
        data = cur.fetchall()
        return data

    def retrieving_Past_rec(family_name, limit=5, cur=cur):
        # Retrieving History
        lis = []
        cur.execute(f'''SELECT fname, regAmt, monthUpto, pendAmt, extraAmt, Note, date_created as date, sno FROM customers WHERE fname='{family_name}' ORDER BY sno DESC LIMIT {limit}''')
        last_paidUpto = 0
        for i in cur.fetchall():
            if not last_paidUpto:
                last_paidUpto = i[2]
            lis.append(i)
        return lis, last_paidUpto

    
    def past_months_collection_hist(month=datetime.now().strftime("%m"), cur=cur):
        cash_IN, cash_PEND, cash_EXTR = 0, 0, 0
        cur.execute(f"SELECT Regamt, Pendamt, Extraamt FROM customers WHERE date_created LIKE '{YYYY}_{month}___'")
        for x,y,z in cur.fetchall():
            cash_IN += int(x)
            cash_PEND += int(y)
            cash_EXTR += int(z)
        return cash_IN, cash_PEND, cash_EXTR, cal.get(month)


# # creating dataBase connection & storing its cursor
# connection = sqlite3.connect('Family_Wise.sqlite')
# cursor = connection.cursor()


# def initial_dataBase_making_from_excel(df=pd.read_excel("Book123.xlsx")):
    # conn = sqlite3.connect('Family_Wise.sqlite')
    # cur = conn.cursor()

    # global host_DB, name_DB, user_DB, pass_DB
    # conn = psycopg2.connect(database=name_DB, user=user_DB, password=pass_DB, host=host_DB)    
    # conn.autocommit = True
    # cur = conn.cursor()

    # cur.execute(f'DROP TABLE IF EXISTS customers')
    # conn.commit()
    # cur.execute('''CREATE TABLE customers ( sno serial PRIMARY KEY NOT NULL, fname VARCHAR(255) NOT NULL, regAmt VARCHAR(255) NOT NULL, monthUpto VARCHAR(255) NOT NULL, pendAmt VARCHAR(255) NOT NULL, extraAmt VARCHAR(255) NOT NULL, Note TEXT, date_created VARCHAR(255) )''')

    # family_names = []
    # for i in df["Family Name"]:
    #     if not isinstance(i, float):
    #         name = i.title().replace(" ", "_")
    #         print(name)
    #         cur.execute(f'DROP TABLE IF EXISTS {name}')
    #         cur.execute(f'CREATE TABLE {name} (Account_No VARCHAR(255))')
    #         conn.commit()
    #         family_names.append(name)
    # # print(len(family_names))
    # time.sleep(1)

    # no = 0
    # for i in df["Account_No"][1:]:
    #     if i > 1:
    #         ac = str(int(i))
    #         if ac[:3]=='200':
    #             ac = '0'+ac
    #         else:
    #             ac = str(ac)
    #         print(ac)
    #         cur.execute(
    #             f'INSERT INTO {family_names[no]} (Account_No) VALUES ({ac})')
    #         conn.commit()
    #     else:
    #         print(f'{no + 1}) ----{family_names[no]}-----')
    #         no += 1

    # time.sleep(1)
    # conn.commit()
    # cur.close()




class FamiliesDB():
    """ Customers is our Collections Recorder DB"""
    MM = datetime.now().strftime("%m")
    YYYY = datetime.now().strftime("%Y")

    global host_DB, name_DB, user_DB, pass_DB
    
    conn = psycopg2.connect(database=name_DB, user=user_DB, password=pass_DB, host=host_DB)    
    conn.autocommit = True
    cur = conn.cursor()


    def get_all_family_names(cur=cur):
        # get all tables: 
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
        family_names = [i[0].title() for i in cur.fetchall() if i[0] not in ['portal_2', 'customers']]
        return family_names


    def search_family(family_name, cdatabase=name_DB, user=user_DB, password=pass_DB, host=host_DB):
        conn = psycopg2.connect(database=cdatabase, user=user, password=password, host=host)    
        conn.autocommit = True
        cur = conn.cursor()
        table_name = family_name.title().replace(" ", "_")
        cur.execute(f"SELECT Account_Name, Portal_2.Account_No, Denomination, Opening_Date, Closing_Date, Month_Paid_Upto, Next_Installment_Due_Date, Total_Return FROM {table_name} INNER JOIN portal_2 ON right({table_name}.account_no, 11) = right(portal_2.account_no, 11) ORDER BY Month_Paid_Upto DESC;")
        total_regular = 0
        lis = []
        for row in cur.fetchall():
            lis.append(row)
            total_regular += row[2]
        conn.close()
        return lis, total_regular


    def ifPresentEarlier(fname, acc_list_common, familyList, conn=conn, cur=cur):
        # familyList = FamiliesDB.get_all_family_names()
        sumry = []
        nos = len(acc_list_common.split())
        for table_name in familyList:
            if table_name in (fname, 'portal_2', 'customers'):
                continue
            for acc in acc_list_common.split():
                cur.execute(f"SELECT Account_No FROM {table_name}")
                if(int(acc) in [int(ac[0]) for ac in cur.fetchall()]):
                    print(table_name, acc)
                    cur.execute(f"DELETE FROM {table_name} WHERE right(Account_No,11) = right('{acc}', 11);")
                    print(table_name, acc, "is Deleted Successfully")
                    nos -= 1
                    print(nos)
                    sumry += [table_name, acc]
                    conn.commit()
                    time.sleep(0.5)

            # ## dropping vaccant tables:
            cur.execute(f"SELECT count(Account_No) FROM {table_name}")
            if(cur.fetchone()[0]==0):
                sumry += [f"$$-{table_name} is Vacant, So Dropped..!!"]
                cur.execute(f'DROP TABLE IF EXISTS {table_name}')
                print(f"$$-{table_name} is Vacant, So Dropped..!!")
                conn.commit()

            if nos==0:
                break
        return sumry


    def add_family_table(familyList, fname, accounts_str, conn=conn, cur=cur):
        name = fname.title().replace(" ", "_")
        # print(name)
        if(name not in familyList):
            cur.execute(f'DROP TABLE IF EXISTS {name}')
            cur.execute(f'CREATE TABLE {name} (Account_No VARCHAR(16))')
            print(name, "Created Successfully")
            conn.commit()

        no = 0
        if len(accounts_str.split())>0:
            for ac in accounts_str.split():
                print('Inserted', ac)
                no += 1
                cur.execute(f"INSERT INTO {name} (Account_No) VALUES ('{ac}')")
                conn.commit()

        time.sleep(0.5)
        conn.commit()

        if no == len(accounts_str.split()):
            # print(no, len(accounts_str.split()))
            return FamiliesDB.ifPresentEarlier(fname=fname, acc_list_common=accounts_str, familyList=familyList)

        return ["No Earlier A/c Present !!"]


    def del_family_table(familyList, fname, accounts_str, conn=conn, cur=cur):
        if(len(accounts_str) == 1):
            accBox = int(accounts_str)
        else:
            accBox = 11

        name = fname.title().replace(" ", "_")
        # print(name) // Pass 0-in accounts box to drop table
        if(name in familyList and accBox == 0):
            cur.execute(f'DROP TABLE IF EXISTS {name}')
            print(name, "Dropped Successfully")
            conn.commit()
        elif(name not in familyList):
            print("Deleting NON existing table")
            return -1
        else:
            no = 0
            if len(accounts_str.split())>0:
                for ac in accounts_str.split():
                    print(f'{no + 1}) ----{name}-----')
                    cur.execute(f"DELETE FROM {name} WHERE right(Account_No,11) = right('{ac}', 11);")
                    print(ac, "Deleted Successfully")
                    conn.commit()
                    time.sleep(0.5)

        time.sleep(0.3)
        conn.commit()
   


    def report(cur=cur):
        lis = []
        # totalDenomination = 
        cur.execute("SELECT sum(Denomination) as total FROM Portal_2;")
        lis += [i[0] for i in cur.fetchall()]
        # morePending = 
        cur.execute("SELECT sum(Denomination) as total FROM Portal_2 WHERE Pending_Installment>'1';")
        lis += [i[0] for i in cur.fetchall()]
        # onePendig = 
        cur.execute("SELECT sum(Denomination) as total FROM Portal_2 WHERE Pending_Installment='1';")
        lis += [i[0] for i in cur.fetchall()]
        # regAmt = 
        cur.execute("SELECT sum(Denomination) as total FROM Portal_2 WHERE Pending_Installment is NULL and Advance_Installment is NULL;")
        lis += [i[0] for i in cur.fetchall()]
        # moreAdvance = 
        cur.execute("SELECT sum(Denomination) as total FROM Portal_2 WHERE Advance_Installment>'1';")
        lis += [i[0] for i in cur.fetchall()]
        # oneAdvance = 
        cur.execute("SELECT sum(Denomination) as total FROM Portal_2 WHERE Advance_Installment='1';")
        lis += [i[0] for i in cur.fetchall()]

        # print(lis)

        familyList = FamiliesDB.get_all_family_names()
        thisMonts = CustomersDB.showThisMonth()
        records_rem_families = set(familyList).difference(set([i[0] for i in thisMonts]))

        # query1 = 
        cur.execute(f"SELECT Account_Name, Account_No, Denomination, Month_Paid_Upto, Next_Installment_Due_Date FROM Portal_2 WHERE substr(Next_Installment_Due_Date, 8,4) = '{YYYY}' and substr(Next_Installment_Due_Date, 4,3) = '{MM}' ORDER by substr(Next_Installment_Due_Date, 1,2) LIMIT 20;")
        currPendList = cur.fetchall()
        # print(currPendList)
        nearest_due_dt = []
        regular_amt = []
        records_rem_families = list(records_rem_families)
        # for table_name in records_rem_families[:5]:
        #     # query2 = 
        #     cur.execute(f"SELECT Next_Installment_Due_Date FROM {table_name} INNER JOIN portal_2 ON {table_name}.account_no = right(portal_2.account_no, 11) WHERE Month_Paid_Upto not in (60,120);")
        #     nearest_due_dt += ([i for i in cur.fetchall()])
        #     regular_amt.append(FamiliesDB.search_family(family_name=table_name)[1])
        #     print(regular_amt)
        #     break
        # nearest_due_dt = [i[0] for i in nearest_due_dt]

        # print(len(regular_amt), len(nearest_due_dt), len(records_rem_families))
        # records_rem_families_data = [i for i in zip(records_rem_families, regular_amt, nearest_due_dt)]
        # records_rem_families_data = [i for i in records_rem_families_data if i[2]!='\xa0']
        # records_rem_families_data = sorted(records_rem_families_data, key= lambda x:x[2][:2])
        # records_rem_families_data = list(filter(lambda x:x[2][3:6]==MM, records_rem_families_data))
        return currPendList, sorted(records_rem_families), lis


    def crossVarify_accounts_repeatation(cur=cur):
        families = FamiliesDB.get_all_family_names()

        customer_box = []
        for family_table in families:
            cur.execute(f"SELECT Account_No FROM {family_table}")
            customer_box += [_[0] for _ in cur.fetchall()]
        cur.execute(f"SELECT Account_No FROM Portal_2")
        portal_box = [int(_[0]) for _ in cur.fetchall()]
        extra_accounts_found_in_groups = set(customer_box).difference(set(portal_box))
        return (len(extra_accounts_found_in_groups), extra_accounts_found_in_groups)

if __name__ == "__main__":
    print("inside family_functions")

    
