import os
import sqlite3  
import operator  
from collections import OrderedDict 
import argparse
import win32crypt

def get_path(path=None):
    if path == None:
        data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        files = os.listdir(data_path)
        history_path = os.path.join(data_path, 'history')
        return history_path
    else:
        return path

#querying the db
def get_data(db_path, statement):
    c = sqlite3.connect(db_path)
    cursor = c.cursor()
    cursor.execute(statement)
    results = cursor.fetchall()
    c.close()
    return results

def get_passwd(path=None):
    if path == None:
        data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        files = os.listdir(data_path)
        passwd_path = os.path.join(data_path, 'Login Data')
    else:
        passwd_path = path
    
    # fetch data
    statement = 'select username_value, password_value, origin_url from logins;'
    datas = get_data(passwd_path, statement)
    print("Username|Password|Site")
    for data in datas:
        name = data[0]
        site = data[2]
        password_hash = data[1]
        try:
            password = win32crypt.CryptUnprotectData(password_hash, None, None, None, 0)
            password = password[1].decode("gbk")
        except:
            print('[*]One hash failed -- try next> Site: {} User: {}'.format(site, name))
            password = ""
        print("{}|{}|{}".format(name, password, site))


def get_keyword(path):
    db_path = get_path(path)
    statement = "SELECT keyword_search_terms.term, urls.url FROM keyword_search_terms, urls WHERE urls.id = keyword_search_terms.url_id;"
    results = get_data(db_path, statement)
    print("Terms|Url ")
    for result in results:
        print("{}|{}".format(result[0], result[1]))


def get_url(path, time=None):
    db_path = get_path(path)
    statement = "SELECT urls.url, urls.title, urls.last_visit_time FROM urls, visits WHERE urls.id = visits.url;"
    results = get_data(db_path, statement)
    print("Url|Title|Time ")
    for result in results:
        print("{}|{}|{}".format(result[0], result[1], result[2]))


def get_downloads(path, time=None):
    db_path = get_path(path)
    statement = "SELECT downloads.target_path, downloads.tab_url, downloads.state, downloads.start_time, downloads.end_time FROM downloads"
    results = get_data(db_path, statement)
    print("Target Path|Url|State|Start|End")
    if time == None:
        for result in results:
            print("{}|{}|{}|{}|{}".format(result[0], result[1], result[2], result[3], result[4]))
    else:
        print("not imeplement")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url','-u', action='store_true',help=" Show Urls", required=False)
    parser.add_argument('--downloads','-d', action='store_true', help=" Show downloads ", required=False)
    parser.add_argument('--passwd', '-p', action='store_true',help=" Show password ", required=False)
    parser.add_argument('--keyword', '-k', action='store_true',help=" Show Search Term ", required=False)
    parser.add_argument('--path', help="set history/downloads/keyword path", required=False)
    parser.add_argument('--passwdpath', help="set password file path", required=False)


    args = parser.parse_args()
    if args.path:
        history_path = args.path
    else:
        history_path = None

    if args.passwdpath:
        passwd_path = args.passwdpath
    else:
        passwd_path = None

    if args.url:
        get_url(history_path)
    if args.downloads:
        get_downloads(history_path)
    if args.keyword:
        get_keyword(history_path)
    if args.passwd:
        get_passwd(passwd_path)
