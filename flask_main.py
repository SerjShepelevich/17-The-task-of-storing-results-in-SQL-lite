from flask import Flask, render_template
from hh_pars_API import Lab12 as hh_parser
from sql_modul import Sql_modul as sql_modul
import pprint

list_of_skills = ['python', 'sql', 'git', 'linux', 'javascript', 'django', 'hive', 'sas', 'scrum',
                 'aosp', 'unix', 'ruby', 'php', 'nodejs', 'matlab', 'frontend', 'backend', 'web',
                 'office', 'qt', 'pyqt', 'java', 'c+', 'c#', 'experience', 'r', 'pandas', 'numpy']


app = Flask(__name__)

@app.route('/')
@app.route('/main.html')
def main_page():
    return render_template('main.html')

@app.route('/contact.html')
def contact_page():
    return render_template('contact.html')

@app.route('/search.html')
def search_page():
    config_db = 'id INT, name TEXT, mid_salary INT, max_salary INT, min_salary INT, common_skills TEXT'
    name_db = "test.db"
    key_words = "python"
    sql = sql_modul(name_db, config_db)
    records = sql.read_data(key_words)
    if len(records) == 0 or records == None:
        temp = hh_parser('Python', list_of_skills)
        result = temp.number_pages
        dic_ = temp.harvest_vac()
        list_salary = temp.calculate_mid_salary_list()
        dict_skills = temp.top_skills()
        data = {'mid_salary': sum(list_salary)/len(list_salary),
                'max_salary': max(list_salary),
                'min_salary': min(list_salary),
                'common_skills':pprint.pformat(dict_skills)}
        sql_data = [key_words,
                sum(list_salary)/len(list_salary),
                max(list_salary),
                min(list_salary),
                pprint.pformat(dict_skills)]
        sql.insert_record(sql_data)
    else:
        data = {'mid_salary': records[0][2],
                'max_salary': records[0][3],
                'min_salary': records[0][4],
                'common_skills': records[0][5]}

    return render_template('search.html', **data)

if __name__ == '__main__':
    #app.run(debug = True)
    app.run()
