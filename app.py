from time import sleep
from flask import Flask, render_template, request, redirect
from flask_httpauth import HTTPBasicAuth
from family_functions import CustomersDB, FamiliesDB, cal
from datetime import datetime
from babel.numbers import format_currency
from secret import USERDB


auth = HTTPBasicAuth()
app = Flask(__name__)


# PRIVATE Credentials:
database = USERDB


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return database.get(username) == password


@app.route('/')
def login():
    return redirect('/start')

# @app.route('/')
# def login():
#     return render_template('Login.html')


family_names = FamiliesDB.get_all_family_names()


# @app.route('/login_form', methods=['POST', 'GET'])
# def logging_and_Search():
#     username = request.form['username']
#     password = request.form['password']
#     # print(username, password)
#     if username not in database:
#         return render_template('invalid.html', info='Invalid User')
#     else:
#         if database[username] != password:
#             return render_template('Login.html', info='Invalid Password')
#         else:
#             return redirect('/start')

@app.route('/start', methods=['GET', 'POST'])
@auth.login_required
def hello_world():
    MM = datetime.now().strftime("%B")
    cash_IN, cash_PEND, cash_EXTR, mm = CustomersDB.past_months_collection_hist()
    return render_template('index.html', user_name=database.get("my_name"), MM=MM, thisMonth=CustomersDB.showThisMonth(), family_list=FamiliesDB.get_all_family_names(), cash_IN=cash_IN, cash_PEND=cash_PEND, cash_EXTR=cash_EXTR)


@app.route('/on_search', methods=['GET', 'POST'])
@auth.login_required
def on_search():
    if request.method == 'POST':
        name = request.form['family_name']
        if name not in family_names:
            return ":( :( :(  Invalid Family Name. \n\nPlease INSERT It First & Then Use"

        print(name)

    rec_history, last_paidUpto = CustomersDB.retrieving_Past_rec(name)
    print(rec_history)

    dictionary, regular_total = FamiliesDB.search_family(name)

    return render_template('search_table.html',  user_name=database.get("my_name"), name=name, dic=dictionary, regular_total=regular_total, rec=rec_history, last_paidUpto=last_paidUpto)


@app.route('/on_search_link/<string:name>')
@auth.login_required
def on_search_link(name):

    if name not in family_names:
        return ":( :( :(  Invalid Family Name. \n\nPlease INSERT It First & Then Use"

    print(name)

    rec_history, last_paidUpto = CustomersDB.retrieving_Past_rec(name)
    print(rec_history)

    dictionary, regular_total = FamiliesDB.search_family(name)

    return render_template('search_table.html',  user_name=database.get("my_name"), name=name, dic=dictionary, regular_total=regular_total, rec=rec_history, last_paidUpto=last_paidUpto)


@app.route('/submit/<string:name>', methods=['GET', 'POST'])
@auth.login_required
def submit(name):
    if request.method == 'POST':
        name = name
        reg = request.form['reg']
        month = request.form['month']
        pend = request.form['pend']
        ext = request.form['ext']
        note = request.form['note']
        print(name, reg, month, pend, ext, note)
        op = CustomersDB.insert(
            fname=name, regAmt=reg, monthUpto=month, pendAmt=pend, extraAmt=ext, Note=note)
        print(op, name)
        # len, acc = FamiliesDB.crossVarify_accounts_repeatation()
    return render_template('submit.html',  user_name=database.get("my_name"), name=name, len=' ', acc=' ')


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
@auth.login_required
def update(sno):
    if request.method == 'POST':
        reg = request.form['reg']
        month = request.form['month']
        pend = request.form['pend']
        ext = request.form['ext']
        note = request.form['note']
        op = CustomersDB.update(
            sno=sno, regAmt=reg, monthUpto=month, pendAmt=pend, extraAmt=ext, Note=note)
        print(op, sno)
        return render_template('submit.html',  user_name=database.get("my_name"))

    fname, regAmt, monthUpto, pendAmt, extraAmt, Note = CustomersDB.filter(
        sno=sno)
    return render_template('update.html', sno=sno, fname=fname, regAmt=regAmt, monthUpto=monthUpto, pendAmt=pendAmt, extraAmt=extraAmt, Note=Note,  user_name=database.get("my_name"))


@app.route('/delete/<int:sno>')
@auth.login_required
def delete(sno):
    CustomersDB.delete(sno=sno)
    sleep(1)
    return render_template('submit.html', user_name=database.get("my_name"))


@app.route('/add-remove', methods=['GET', 'POST'])
@auth.login_required
def add():
    if request.method == 'POST':
        fname = request.form['nm']
        account_ls = request.form['acc']
        print(fname, account_ls)
    sleep(.5)
    return render_template('add.html', family_list=FamiliesDB.get_all_family_names(), user_name=database.get("my_name"))


@app.route('/grUpdate/<string:nm>/<string:acc>', methods=['GET', 'POST'])
@auth.login_required
def grUp(nm, acc):
    if(len(nm.split()) > 1):
        nm = nm.title().replace(" ", "_")
    print(nm, acc)
    """create a function to add family nm if new & assign accs to it in DB"""
    summary = FamiliesDB.add_family_table(familyList=family_names, fname=nm, accounts_str=acc)
    dictionary, regular_total = FamiliesDB.search_family(nm)
    sleep(.5)

    return render_template('showNewT.html', name=nm, dic=dictionary, regular_total=regular_total, summary=summary, user_name=database.get("my_name"))


@app.route('/grDelete/<string:nm>/<string:acc>', methods=['GET', 'POST'])
@auth.login_required
def grDel(nm, acc):
    if(len(nm.split()) > 1):
        nm = nm.title().replace(" ", "_")
    print(nm, acc)
    """create a function to Remove family nm-> assigned selected accs to it in DB"""
    """for directly droping family Write 0 in AccountsBox"""
    a = FamiliesDB.del_family_table(
        familyList=family_names, fname=nm, accounts_str=acc)
    if a == -1:
        return f"ERROE..!!!  @___Deleting NON existing table {nm}"
    try:
        FamiliesDB.search_family(nm)
    except:
        sleep(.5)
        return render_template('submit.html', name=nm, user_name=database.get("my_name"))
    dictionary, regular_total = FamiliesDB.search_family(nm)
    sleep(.5)

    return render_template('showNewT.html', name=nm, dic=dictionary, regular_total=regular_total, user_name=database.get("my_name"))


@app.route('/report')
@auth.login_required
def show_report():
    currPendList, records_remaining_families, Finance_list = FamiliesDB.report()
    return render_template('report.html', currPendList=currPendList, records_remaining_families=records_remaining_families, Finance_list=Finance_list, user_name=database.get("my_name"))


@app.route('/past_collections', methods=['GET', 'POST'])
@auth.login_required
def show_historyy():
    if request.method == 'POST':
        mm = request.form['mm']
        MM = cal.get(mm)
        cash_IN, cash_PEND, cash_EXTR, MM = CustomersDB.past_months_collection_hist(mm)
        return render_template('collection_history.html', thisMonth=sorted(CustomersDB.showThisMonth(mm)), cash_IN=cash_IN, cash_PEND=cash_PEND, cash_EXTR=cash_EXTR, mm=mm, MM=MM, user_name=database.get("my_name"))
    
    return render_template('pastmonthcatch.html', user_name=database.get("my_name"))
    


@app.context_processor
def utility_processor():
    def format_price(amount):
        return format_currency(amount, 'INR', locale='en_IN')[:-3]

    return dict(format_price=format_price)


if __name__ == "__main__":
    app.run(debug=False)
