from flask import Flask, request, Response, abort, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from collections import defaultdict
import sqlite3

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

# ログイン用ユーザー作成
users = {
    1: User(1, "user01", "password"),
    2: User(2, "user02", "password")
}

# ユーザーチェックに使用する辞書作成
nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.name]["password"] = i.password
    user_check[i.name]["id"] = i.id

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route('/')
def home():
    return Response("home: <a href='/login/'>Login</a> <a href='/protected/'>Protected</a> <a href='/logout/'>Logout</a>")

# ログインしないと表示されないパス
@app.route('/protected/')
@login_required
def protected():
    return render_template('base.html')

# ログインパス
@app.route('/login/', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        # ユーザーチェック
        if(request.form["username"] in user_check and request.form["password"] == user_check[request.form["username"]]["password"]):
            # ユーザーが存在した場合はログイン
            login_user(users.get(user_check[request.form["username"]]["id"]))
            return Response('''
            login success!<br />
            <a href="/protected/">protected</a><br />
            <a href="/logout/">logout</a><br />
            <a href"/database/">Database</a>
            ''')
        else:
            return abort(401)
    else:
        return render_template("login.html")

# ログアウトパス
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return Response('''
    logout success!<br />
    <a href="/login/">login</a>
    ''')


'''
メモ計算機
'''
num_of_sum=0
num_of_false=0
num_of_add=0
@app.route('/add_c/')
@login_required
def add():
    global num_of_add
    global num_of_sum
    num_of_add=num_of_add+1
    num_of_sum=num_of_sum+1
    return render_template('base.html',num_of_correct=num_of_add,num_of_false=num_of_false,num_of_sum=num_of_sum)

@app.route('/add_f/')
@login_required
def flur():
    global num_of_false
    global num_of_sum
    num_of_false = num_of_false+1
    num_of_sum = num_of_sum+1
    return render_template('base.html',num_of_correct=num_of_add,num_of_false=num_of_false,num_of_sum=num_of_sum)




'''
add画面
'''
@app.route('/add_data')
@login_required
def adder():
    return render_template('add.html')


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    title = "こんにちは"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        name = request.form.get('name')
        # リクエストフォームから「教科」を取得して
        subject = request.form.get('subject')
        unit = request.form.get('unit')
        correct = request.form['correct']
        num = request.form['num']

        print(name)
        print(subject)

        #データベースに送信
        # データベースに接続する
        conn = sqlite3.connect('example1128.db')
        c = conn.cursor()
        # テーブルの作成
        #c.execute('''CREATE TABLE test_table1128(name text, subject text,unit text,correct real,num real)''')

        #データの更新
        if(unit=='be動詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list01 = cc.fetchone()
            cor01=list01[3]+float(correct)
            num01=list01[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor01,num01,unit,name))


            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()
            
                
            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit01=unit,cor01=cor01,num01=num01)

        #データの更新
        if(unit=='一般動詞'):
            cc=conn.execute(u"select * from test_table1128 where unit='be動詞' and name=?",(name,))

            list02 = cc.fetchone()
            cor02=list02[3]
            num02=list02[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list02 = list(cc.fetchone())
            cor02=list02[3]+float(correct)
            num02=list02[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor02,num02,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit02=unit,cor02=cor02,num02=num02)

        #データの更新
        if(unit=='疑問文・否定文'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list03 = cc.fetchone()
            cor03=list03[3]
            num03=list03[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list03 = list(cc.fetchone())
            cor03=list03[3]+float(correct)
            num03=list03[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor03,num03,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit03=unit,cor03=cor03,num03=num03)

        if(unit=='疑問詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list04 = cc.fetchone()
            cor04=list04[3]
            num04=list04[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list04 = list(cc.fetchone())
            cor04=list04[3]+float(correct)
            num04=list04[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor04,num04,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit04=unit,cor04=cor04,num04=num04)

        if(unit=='命令文'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list05 = cc.fetchone()
            cor05=list05[3]
            num05=list05[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list05 = list(cc.fetchone())
            cor05=list05[3]+float(correct)
            num05=list05[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor05,num05,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit05=unit,cor05=cor05,num05=num05)
        
        if(unit=='三人称'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list06 = cc.fetchone()
            cor06=list06[3]
            num06=list06[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list06 = list(cc.fetchone())
            cor06=list06[3]+float(correct)
            num06=list06[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor06,num06,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit06=unit,cor06=cor06,num06=num06)

        if(unit=='現在進行形'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list07 = cc.fetchone()
            cor07=list07[3]
            num07=list07[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list07 = list(cc.fetchone())
            cor07=list07[3]+float(correct)
            num07=list07[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor07,num07,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit07=unit,cor07=cor07,num07=num07)

        if(unit=='canできる'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list08 = cc.fetchone()
            cor08=list08[3]
            num08=list08[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list08 = list(cc.fetchone())
            cor08=list08[3]+float(correct)
            num08=list08[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor08,num08,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit08=unit,cor08=cor08,num08=num08)

        if(unit=='過去形'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list09 = cc.fetchone()
            cor039=list09[3]
            num09=list09[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list09 = list(cc.fetchone())
            cor09=list09[3]+float(correct)
            num09=list09[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor09,num09,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit09=unit,cor09=cor09,num09=num09)
        
        if(unit=='名詞の複数形'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list10 = cc.fetchone()
            cor10=list10[3]
            num10=list10[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list10 = list(cc.fetchone())
            cor10=list10[3]+float(correct)
            num10=list10[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor10,num10,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit10=unit,cor10=cor10,num10=num10)

        if(unit=='代名詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list11 = cc.fetchone()
            cor11=list11[3]
            num11=list11[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list11 = list(cc.fetchone())
            cor11=list11[3]+float(correct)
            num11=list11[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor11,num11,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit11=unit,cor11=cor11,num11=num11)

        if(unit=='be動詞の過去形'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list12 = cc.fetchone()
            cor12=list12[3]
            num12=list12[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list12 = list(cc.fetchone())
            cor12=list12[3]+float(correct)
            num12=list12[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor12,num12,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit12=unit,cor12=cor12,num12=num12)
        
        if(unit=='過去進行形'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list13 = cc.fetchone()
            cor13=list13[3]
            num13=list13[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list13 = list(cc.fetchone())
            cor13=list13[3]+float(correct)
            num13=list13[4]+float(num)
            conn.execute(u"update test_table1138 SET correct=?,num=? WHERE unit=? and name=?",(cor13,num13,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit13=unit,cor13=cor13,num13=num13)
        
        if(unit=='未来'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list14 = cc.fetchone()
            cor14=list14[3]
            num14=list14[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list14 = list(cc.fetchone())
            cor14=list14[3]+float(correct)
            num14=list14[4]+float(num)
            conn.execute(u"update test_table1148 SET correct=?,num=? WHERE unit=? and name=?",(cor14,num14,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit14=unit,cor14=cor14,num14=num14)
        
        if(unit=='動名詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list15 = cc.fetchone()
            cor15=list15[3]
            num15=list15[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list15 = list(cc.fetchone())
            cor15=list15[3]+float(correct)
            num15=list15[4]+float(num)
            conn.execute(u"update test_table1158 SET correct=?,num=? WHERE unit=? and name=?",(cor15,num15,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit15=unit,cor15=cor15,num15=num15)
        
        if(unit=='不定詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list16 = cc.fetchone()
            cor16=list16[3]
            num16=list16[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list16 = list(cc.fetchone())
            cor16=list16[3]+float(correct)
            num16=list16[4]+float(num)
            conn.execute(u"update test_table1168 SET correct=?,num=? WHERE unit=? and name=?",(cor16,num16,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit16=unit,cor16=cor16,num16=num16)
        
        if(unit=='助動詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list17 = cc.fetchone()
            cor17=list17[3]
            num17=list17[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list17 = list(cc.fetchone())
            cor17=list17[3]+float(correct)
            num17=list17[4]+float(num)
            conn.execute(u"update test_table1178 SET correct=?,num=? WHERE unit=? and name=?",(cor17,num17,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit17=unit,cor17=cor17,num17=num17)
        
        if(unit=='比較'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list18 = cc.fetchone()
            cor18=list18[3]
            num18=list18[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list18 = list(cc.fetchone())
            cor18=list18[3]+float(correct)
            num18=list18[4]+float(num)
            conn.execute(u"update test_table1188 SET correct=?,num=? WHERE unit=? and name=?",(cor18,num18,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit18=unit,cor18=cor18,num18=num18)

        if(unit=='there is(are)'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list19 = cc.fetchone()
            cor19=list19[3]
            num19=list19[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list19 = list(cc.fetchone())
            cor19=list19[3]+float(correct)
            num19=list19[4]+float(num)
            conn.execute(u"update test_table1208 SET correct=?,num=? WHERE unit=? and name=?",(cor19,num19,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit19=unit,cor19=cor19,num19=num19)

        if(unit=='接続詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list20 = cc.fetchone()
            cor20=list20[3]
            num20=list20[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list20 = list(cc.fetchone())
            cor20=list20[3]+float(correct)
            num20=list20[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor20,num20,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit20=unit,cor20=cor20,num20=num20)
        
        if(unit=='受け身(基本)'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list21 = cc.fetchone()
            cor21=list21[3]
            num21=list21[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list21 = list(cc.fetchone())
            cor21=list21[3]+float(correct)
            num21=list21[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor21,num21,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit21=unit,cor21=cor21,num21=num21)

        if(unit=='受け身(発展)'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list22 = cc.fetchone()
            cor22=list22[3]
            num22=list22[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list22 = list(cc.fetchone())
            cor22=list22[3]+float(correct)
            num22=list22[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor22,num22,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit22=unit,cor22=cor22,num22=num22)

        if(unit=='現在完了'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list23 = cc.fetchone()
            cor23=list23[3]
            num23=list23[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list23 = list(cc.fetchone())
            cor23=list23[3]+float(correct)
            num23=list23[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor23,num23,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit23=unit,cor23=cor23,num23=num23)
        
        if(unit=='不定詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list24 = cc.fetchone()
            cor24=list24[3]
            num24=list24[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list24 = list(cc.fetchone())
            cor24=list24[3]+float(correct)
            num24=list24[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor24,num24,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit24=unit,cor24=cor24,num24=num24)
        
        if(unit=='分詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list25 = cc.fetchone()
            cor25=list25[3]
            num25=list25[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list25 = list(cc.fetchone())
            cor25=list25[3]+float(correct)
            num25=list25[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor25,num25,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit25=unit,cor25=cor25,num25=num25)
        
        if(unit=='間接疑問'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list26 = cc.fetchone()
            cor26=list26[3]
            num26=list26[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list26 = list(cc.fetchone())
            cor26=list26[3]+float(correct)
            num26=list26[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor26,num26,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit26=unit,cor26=cor26,num26=num26)
        
        if(unit=='関係代名詞(主格)'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list27 = cc.fetchone()
            cor27=list27[3]
            num27=list27[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list27 = list(cc.fetchone())
            cor27=list27[3]+float(correct)
            num27=list27[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor27,num27,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit27=unit,cor27=cor27,num27=num27)
        
        if(unit=='関係代名詞(目的格)'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list28 = cc.fetchone()
            cor28=list28[3]
            num28=list28[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list28 = list(cc.fetchone())
            cor28=list28[3]+float(correct)
            num28=list28[4]+float(num)
            conn.execute(u"update test_table1128 SET correct=?,num=? WHERE unit=? and name=?",(cor28,num28,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit28=unit,cor28=cor28,num28=num28)
        
        if(unit=='形容詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list29 = cc.fetchone()
            cor29=list29[3]
            num29=list29[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list29 = list(cc.fetchone())
            cor29=list29[3]+float(correct)
            num29=list29[4]+float(num)
            conn.execute(u"update test_table1130 SET correct=?,num=? WHERE unit=? and name=?",(cor29,num29,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit29=unit,cor29=cor29,num29=num29)
        
        if(unit=='副詞'):
            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))

            list30 = cc.fetchone()
            cor30=list30[3]
            num30=list30[4]


            cc=conn.execute(u"select * from test_table1128 where unit=? and name=?",(unit,name))
            list30 = list(cc.fetchone())
            cor30=list30[3]+float(correct)
            num30=list30[4]+float(num)
            conn.execute(u"update test_table1130 SET correct=?,num=? WHERE unit=? and name=?",(cor30,num30,unit,name))

            # 挿入した結果を保存（コミット）する
            conn.commit()

            # データベースへのアクセスが終わったら close する
            conn.close()

            user_name=name
            # index.html をレンダリングする
            return render_template('base.html',user_name=name,unit30=unit,cor30=cor30,num30=num30)

@app.route('/press', methods=['GET', 'POST'])
@login_required
def press():
    if request.method == 'POST':
        conn = sqlite3.connect('example1128.db')
        c = conn.cursor()
        name = request.form.get('name')

        c01=conn.execute(u"select * from test_table1128 where unit='be動詞' and name=?",(name,))
        list01 = list(c01.fetchone())
        
        c02=conn.execute(u"select * from test_table1128 where unit='一般動詞' and name=?",(name,))
        list02 = list(c02.fetchone())

        c03=conn.execute(u"select * from test_table1128 where unit='疑問文・否定文' and name=?",(name,))
        list03 = list(c03.fetchone())

        c04=conn.execute(u"select * from test_table1128 where unit='疑問詞' and name=?",(name,))
        list04 = list(c04.fetchone())

        c05=conn.execute(u"select * from test_table1128 where unit='命令文' and name=?",(name,))
        list05 = list(c05.fetchone())
        
        c06=conn.execute(u"select * from test_table1128 where unit='三人称' and name=?",(name,))
        list06 = list(c06.fetchone())

        c07=conn.execute(u"select * from test_table1128 where unit='現在進行形' and name=?",(name,))
        list07 = list(c07.fetchone())

        c08=conn.execute(u"select * from test_table1128 where unit='canできる' and name=?",(name,))
        list08 = list(c08.fetchone())

        c09=conn.execute(u"select * from test_table1128 where unit='過去形' and name=?",(name,))
        list09 = list(c09.fetchone())

        c10=conn.execute(u"select * from test_table1128 where unit='名詞の複数形' and name=?",(name,))
        list10 = list(c10.fetchone())

        c11=conn.execute(u"select * from test_table1128 where unit='代名詞' and name=?",(name,))
        list11 = list(c11.fetchone())

        c12=conn.execute(u"select * from test_table1128 where unit='be動詞の過去形' and name=?",(name,))
        list12 = list(c12.fetchone())

        c13=conn.execute(u"select * from test_table1128 where unit='過去進行形' and name=?",(name,))
        list13 = list(c13.fetchone())

        c14=conn.execute(u"select * from test_table1128 where unit='未来' and name=?",(name,))
        list14 = list(c14.fetchone())

        c15=conn.execute(u"select * from test_table1128 where unit='動名詞' and name=?",(name,))
        list15 = list(c15.fetchone())

        c16=conn.execute(u"select * from test_table1128 where unit='不定詞' and name=?",(name,))
        list16 = list(c16.fetchone())

        c17=conn.execute(u"select * from test_table1128 where unit='助動詞' and name=?",(name,))
        list17 = list(c17.fetchone())

        c18=conn.execute(u"select * from test_table1128 where unit='比較' and name=?",(name,))
        list18 = list(c18.fetchone())

        c19=conn.execute(u"select * from test_table1128 where unit='there is(are)' and name=?",(name,))
        list19 = list(c19.fetchone())

        c20=conn.execute(u"select * from test_table1128 where unit='接続詞' and name=?",(name,))
        list20 = list(c20.fetchone())

        c21=conn.execute(u"select * from test_table1128 where unit='受け身(基本)' and name=?",(name,))
        list21 = list(c21.fetchone())

        c22=conn.execute(u"select * from test_table1128 where unit='受け身(発展)' and name=?",(name,))
        list22 = list(c22.fetchone())

        c23=conn.execute(u"select * from test_table1128 where unit='現在完了' and name=?",(name,))
        list23 = list(c23.fetchone())

        c24=conn.execute(u"select * from test_table1128 where unit='不定詞(発展)' and name=?",(name,))
        list24 = list(c24.fetchone())

        c25=conn.execute(u"select * from test_table1128 where unit='分詞' and name=?",(name,))
        list25 = list(c25.fetchone())

        c26=conn.execute(u"select * from test_table1128 where unit='間接疑問' and name=?",(name,))
        list26 = list(c26.fetchone())

        c27=conn.execute(u"select * from test_table1128 where unit='関係代名詞(主格)' and name=?",(name,))
        list27 = list(c27.fetchone())

        c28=conn.execute(u"select * from test_table1128 where unit='関係代名詞(目的格)' and name=?",(name,))
        list28 = list(c28.fetchone())

        c29=conn.execute(u"select * from test_table1128 where unit='形容詞' and name=?",(name,))
        list29 = list(c29.fetchone())

        c30=conn.execute(u"select * from test_table1128 where unit='副詞' and name=?",(name,))
        list30 = list(c30.fetchone())

        # 挿入した結果を保存（コミット）する
        conn.commit()
        # データベースへのアクセスが終わったら close する
        conn.close()
        return render_template('base.html',name=name,
                                unit01='be動詞',cor01=list01[3],num01=list01[4],
                                unit02='一般動詞',cor02=list02[3],num02=list02[4],
                                unit03='疑問文・否定文',cor03=list03[3],num03=list03[4],
                                unit04='疑問詞',cor04=list04[3],num04=list04[4],
                                unit05='命令文',cor05=list05[3],num05=list05[4],
                                unit06='三人称',cor06=list06[3],num06=list06[4],
                                unit07='現在進行形',cor07=list07[3],num07=list07[4],
                                unit08='canできる',cor08=list08[3],num08=list08[4],
                                unit09='過去形',cor09=list09[3],num09=list09[4],
                                unit10='名詞の複数形',cor10=list10[3],num10=list10[4],
                                unit11='代名詞',cor11=list11[3],num11=list11[4],
                                unit12='be動詞の過去形',cor12=list12[3],num12=list12[4],
                                unit13='過去進行形',cor13=list13[3],num13=list13[4],
                                unit14='未来',cor14=list14[3],num14=list14[4],
                                unit15='動名詞',cor15=list15[3],num15=list15[4],
                                unit16='不定詞',cor16=list16[3],num16=list16[4],
                                unit17='助動詞',cor17=list17[3],num17=list17[4],
                                unit18='比較',cor18=list18[3],num18=list18[4],
                                unit19='there is(are)',cor19=list19[3],num19=list19[4],
                                unit20='接続詞',cor20=list20[3],num20=list20[4],
                                unit21='受け身(基本)',cor21=list21[3],num21=list21[4],
                                unit22='受け身(一般)',cor22=list22[3],num22=list22[4],
                                unit23='現在完了',cor23=list23[3],num23=list23[4],
                                unit24='不定詞(発展)',cor24=list24[3],num24=list24[4],
                                unit25='分詞',cor25=list25[3],num25=list25[4],
                                unit26='間接疑問',cor26=list26[3],num26=list26[4],
                                unit27='関係代名詞(主語)',cor27=list27[3],num27=list27[4],
                                unit28='関係代名詞(目的格)',cor28=list28[3],num28=list28[4],
                                unit29='形容詞',cor29=list29[3],num29=list29[4],
                                unit30='副詞',cor30=list30[3],num30=list30[4],
                                )

@app.route('/prpr')
@login_required
def printf():
    conn = sqlite3.connect('example1128.db')
    c = conn.cursor()

    #all delete
    c.execute(u"DELETE FROM test_table1128")

    #test_user
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','be動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','一般動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','疑問文・否定文',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','疑問詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','命令文',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','三人称',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','現在進行形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','canできる',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','過去形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','名詞の複数形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','代名詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','be動詞の過去形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','過去進行形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','未来',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','動名詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','不定詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','助動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','比較',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','there is(are)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','接続詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','受け身(基本)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','受け身(発展)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','現在完了',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','不定詞(発展)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','分詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','間接疑問',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','関係代名詞(主格)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','関係代名詞(目的格)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','形容詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('test_user','英語','副詞',0,0)")
    #user01
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','be動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','一般動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','疑問文・否定文',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','疑問詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','命令文',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','三人称',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','現在進行形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','canできる',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','過去形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','名詞の複数形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','代名詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','be動詞の過去形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','過去進行形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','未来',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','動名詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','不定詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','助動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','比較',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','there is(are)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','接続詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','受け身(基本)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','受け身(発展)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','現在完了',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','不定詞(発展)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','分詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','間接疑問',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','関係代名詞(主格)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','関係代名詞(目的格)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','形容詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user01','英語','副詞',0,0)")
    #user02
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','be動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','一般動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','疑問文・否定文',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','疑問詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','命令文',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','三人称',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','現在進行形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','canできる',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','過去形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','名詞の複数形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','代名詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','be動詞の過去形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','過去進行形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','未来',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','動名詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','不定詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','助動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','比較',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','there is(are)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','接続詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','受け身(基本)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','受け身(発展)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','現在完了',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','不定詞(発展)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','分詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','間接疑問',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','関係代名詞(主格)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','関係代名詞(目的格)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','形容詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user02','英語','副詞',0,0)")
    #user03
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','be動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','一般動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','疑問文・否定文',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','疑問詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','命令文',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','三人称',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','現在進行形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','canできる',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','過去形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','名詞の複数形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','代名詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','be動詞の過去形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','過去進行形',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','未来',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','動名詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','不定詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','助動詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','比較',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','there is(are)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','接続詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','受け身(基本)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','受け身(発展)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','現在完了',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','不定詞(発展)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','分詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','間接疑問',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','関係代名詞(主格)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','関係代名詞(目的格)',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','形容詞',0,0)")
    c.execute("INSERT INTO test_table1128 VALUES ('user03','英語','副詞',0,0)")
    # 挿入した結果を保存（コミット）する
    conn.commit()
    # データベースへのアクセスが終わったら close する
    conn.close()
    return render_template('base.html',msg='削除しました')

'''
run app
'''

if __name__ == '__main__':
    app.run()