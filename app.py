import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


def database_connecting():
    conn = sqlite3.connect("douban_data.db")
    return conn


def data_selecting():
    try:
        conn = database_connecting()
        c = conn.cursor()  # get cursor 获取光标
        sql = ''' 
                select * from movie250
            '''
        data_list = c.execute(sql)  # execute sql statement 执行sql语句
    except:
        pass
    finally:
        # conn.close()
        return data_list


def scores_data():
    try:
        conn = database_connecting()
        c = conn.cursor()
        sql = '''
                select score, count(score) from movie250 group by score order by score
            '''
        data_list = c.execute(sql)
    except:
        pass
    finally:
        # conn.close()
        return data_list

@app.route('/movie250')
def movie250():
    data_list = list(data_selecting())
    return render_template('index.html', data_list=data_list)


@app.route('/scores')
def scores():
    data_list = list(scores_data())
    return render_template('scores.html', scores_list=data_list)



if __name__ == '__main__':
    app.run()
