from flask import Flask, render_template, request, redirect, url_for, flash , session
import psycopg2 #pip install psycopg2  
import psycopg2.extras 
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
import mysql.connector
from decimal import Decimal
from flask_login import LoginManager, current_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__) 
app.secret_key = "cairocoders-ednalan" 
 
app.config['MYSQL_HOST'] = 'sql6.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql6635405'
app.config['MYSQL_PASSWORD'] = 'PEDI875j2V'
app.config['MYSQL_DB'] = 'sql6635405'
connect_timeout=10

mysql = MySQL(app)

 

@app.route('/banhangmk')
def banhangmk():
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT id, name, image_url, intro, price FROM mattron")
    mattron = cur.fetchall()

    cur.execute("SELECT id, name, image_url, intro, price FROM matdai")
    matdai = cur.fetchall()

    cur.execute("SELECT id, name, image_url, intro, price FROM matvuong")
    matvuong = cur.fetchall()

    cur.execute("SELECT id, name, image_url, intro, price FROM matxoang")
    matxoang = cur.fetchall()

    cur.execute("SELECT id, name, image_url, intro, price FROM mattim")
    mattim = cur.fetchall()
    cur.execute("SELECT id, name, image_url, intro, price FROM kinhhot")
    kinhhot = cur.fetchall()


    cur.close()
    cur.close()
    return render_template('banhangmk.html', mattron=mattron, matdai=matdai, matvuong=matvuong, matxoang=matxoang, mattim=mattim, kinhhot=kinhhot)



# @app.teardown_request
# def teardown_db(exception):
#     if hasattr(mysql, 'connection'):
#         mysql.connection.close()

@app.route('/product/<product_type>/<int:id>')
def product_detail(product_type, id):
    cur = mysql.connection.cursor()

    if product_type == 'mattron':
        cur.execute("SELECT id, name, image_url, intro, price FROM mattron WHERE id=%s", (id,))
        product = cur.fetchone()
    elif product_type == 'matdai':
        cur.execute("SELECT id, name, image_url, intro, price FROM matdai WHERE id=%s", (id,))
        product = cur.fetchone()
    elif product_type == 'matvuong':
        cur.execute("SELECT id, name, image_url, intro, price FROM matvuong WHERE id=%s", (id,))
        product = cur.fetchone()
    elif product_type == 'matxoang':
        cur.execute("SELECT id, name, image_url, intro, price FROM matxoang WHERE id=%s", (id,))
        product = cur.fetchone()
    elif product_type == 'mattim':
        cur.execute("SELECT id, name, image_url, intro, price FROM mattim WHERE id=%s", (id,))
        product = cur.fetchone()
    elif product_type == 'kinhhot':
        cur.execute("SELECT id, name, image_url, intro, price FROM kinhhot WHERE id=%s", (id,))
        product = cur.fetchone()
    else:
        # handle invalid product type here
        pass
  # Retrieve some recommended products based on the user's viewing history
    cur.execute("SELECT id, name, image_url FROM {} WHERE id != %s ORDER BY RAND() LIMIT 4".format(product_type), (id,))
    see_also = cur.fetchall()

    cur.close()

    return render_template('product_detail.html', product=product, product_type=product_type, see_also=see_also)
#======================================
@app.route('/signup')
def signup():
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        # Lấy thông tin đăng ký từ form
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = 'kh'
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if user:
            flash("Tài khoản đã tồn tại")
            return redirect('/register')
        if password != confirm_password:
            flash("Mật khẩu không trùng khớp")
            return redirect('/register')
        # Thêm thông tin đăng ký vào cơ sở dữ liệu
        sql = "INSERT INTO users (username, password, confirm_password, role) VALUES (%s, %s, %s, %s)"
        val = (username, password, confirm_password, role)
        cur.execute(sql, val)
        mysql.connection.commit()
        # Chuyển hướng đến trang đăng nhập
        return redirect('/login')

    return render_template('register.html')












#==========================================================




@app.route('/matdai')
def matdai():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM matdai")
    data = cur.fetchall()
    cur.close()
    return render_template('matdai.html', matdai=data)
@app.route('/insertmd', methods = ['POST'])
def insertmd():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO matdai (name, image_url, intro, link,price ) VALUES (%s, %s, %s, %s,%s)", (name, image_url,intro,link,price))
        mysql.connection.commit()
        return redirect(url_for('matdai'))

@app.route('/deletemd/<string:id_data>', methods = ['GET'])
def deletemd(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM matdai WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('matdai'))

@app.route('/updatemd', methods= ['POST', 'GET'])
def updatemd():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE matdai SET name=%s, image_url=%s, intro=%s, link=%s, price=%s
        WHERE id=%s
        """, (name, image_url, intro, link, price, id))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('matdai'))
#=======================================================================

@app.route('/kinhhot')
def kinhhot():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM kinhhot")
    data = cur.fetchall()
    cur.close()
    return render_template('kinhhot.html', kinhhot=data)
@app.route('/insertkk', methods = ['POST'])
def insertkk():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO kinhhot (name, image_url, intro, link,price ) VALUES (%s, %s, %s, %s,%s)", (name, image_url,intro,link,price))
        mysql.connection.commit()
        return redirect(url_for('kinhhot'))

@app.route('/deletekk/<string:id_data>', methods = ['GET'])
def deletekk(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM kinhhot WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('kinhhot'))

@app.route('/updatekk', methods= ['POST', 'GET'])
def updatekk():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE kinhhot SET name=%s, image_url=%s, intro=%s, link=%s, price=%s
        WHERE id=%s
        """, (name, image_url, intro, link, price, id))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('kinhhot'))
#=======================================================================
@app.route('/mattron')
def mattron():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mattron")
    data = cur.fetchall()
    cur.close()
    return render_template('mattron.html', mattron=data)
@app.route('/insertmt', methods = ['POST'])
def insertmt():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mattron (name, image_url, intro, link,price ) VALUES (%s, %s, %s, %s,%s)", (name, image_url,intro,link,price))
        mysql.connection.commit()
        return redirect(url_for('mattron'))

@app.route('/deletemt/<string:id_data>', methods = ['GET'])
def deletemt(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM mattron WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('mattron'))

@app.route('/updatemt', methods= ['POST', 'GET'])
def updatemt():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE mattron SET name=%s, image_url=%s, intro=%s, link=%s, price=%s
        WHERE id=%s
        """, (name, image_url, intro, link, price, id))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('mattron'))

#=============================================================================
@app.route('/mattim')
def mattim():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mattim")
    data = cur.fetchall()
    cur.close()
    return render_template('mattim.html', mattim=data)
@app.route('/insertmtm', methods = ['POST'])
def insertmtm():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mattim (name, image_url, intro, link,price ) VALUES (%s, %s, %s, %s,%s)", (name, image_url,intro,link,price))
        mysql.connection.commit()
        return redirect(url_for('mattim'))

@app.route('/deletemtm/<string:id_data>', methods = ['GET'])
def deletemtm(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM mattim WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('mattim'))

@app.route('/updatemtm', methods= ['POST', 'GET'])
def updatemtm():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE mattim SET name=%s, image_url=%s, intro=%s, link=%s, price=%s
        WHERE id=%s
        """, (name, image_url, intro, link, price, id))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('mattim'))

#==============================================================================================
@app.route('/matvuong')
def matvuong():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM matvuong")
    data = cur.fetchall()
    cur.close()
    return render_template('matvuong.html', matvuong=data)
@app.route('/insertmv', methods = ['POST'])
def insertmv():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO matvuong (name, image_url, intro, link,price ) VALUES (%s, %s, %s, %s,%s)", (name, image_url,intro,link,price))
        mysql.connection.commit()
        return redirect(url_for('matvuong'))

@app.route('/deletemv/<string:id_data>', methods = ['GET'])
def deletemv(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM matvuong WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('matvuong'))

@app.route('/updatemv', methods= ['POST', 'GET'])
def updatemv():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE matvuong SET name=%s, image_url=%s, intro=%s, link=%s, price=%s
        WHERE id=%s
        """, (name, image_url, intro, link, price, id))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('matvuong'))

#==============================================================================================
@app.route('/matxoang')
def matxoang():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM matxoang")
    data = cur.fetchall()
    cur.close()
    return render_template('matxoang.html', matxoang=data)
@app.route('/insertmx', methods = ['POST'])
def insertmx():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO matxoang (name, image_url, intro, link,price ) VALUES (%s, %s, %s, %s,%s)", (name, image_url,intro,link,price))
        mysql.connection.commit()
        return redirect(url_for('matxoang'))

@app.route('/deletemx/<string:id_data>', methods = ['GET'])
def deletemx(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM matxoang WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('matxoang'))

@app.route('/updatemx', methods= ['POST', 'GET'])
def updatemx():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        image_url = request.form['image_url']
        intro = request.form['intro']
        link = request.form['link']
        price = request.form['price']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE matxoang SET name=%s, image_url=%s, intro=%s, link=%s, price=%s
        WHERE id=%s
        """, (name, image_url, intro, link, price, id))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('matxoang'))







































































#===========================================================================================================================================================================


#hienthisanpham
@app.route('/banhang')
def banhang():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    products = cur.fetchall()
    return render_template('banhang.html', products=products)

@app.route('/product_add')
def product_add():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    cur.close()
    return render_template('product_add.html', products=data)
@app.route('/insertsp', methods = ['POST'])
def insertsp():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form['image_url']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (name, description, price, image_url) VALUES (%s, %s, %s, %s)", (name, description,price,image_url))
        mysql.connection.commit()
        return redirect(url_for('product_add'))

@app.route('/deletesp/<string:id_data>', methods = ['GET'])
def deletesp(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('product_add'))

@app.route('/updatesp', methods= ['POST', 'GET'])
def updatesp():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form['image_url']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE products SET name=%s, description=%s,price=%s, image_url=%s
        WHERE id=%s
        """, (name, description, price, image_url, id))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('product_add'))


#baiviet

@app.route('/blog_add')
def blog_add():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts")
    data = cur.fetchall()
    cur.close()
    return render_template('blog_add.html', posts=data)
@app.route('/insertbl', methods = ['POST'])
def insertbl():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        title = request.form['title']
        content = request.form['content']
        image = request.form['image']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts (title, content, image) VALUES (%s, %s, %s)", (title, content, image))
        mysql.connection.commit()
        return redirect(url_for('blog_add'))

@app.route('/deletebl/<string:id_data>', methods = ['GET'])
def deletebl(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('blog_add'))

@app.route('/updatebl', methods= ['POST', 'GET'])
def updatebl():
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        content = request.form['content']
        image = request.form['image']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE posts SET title=%s, content=%s,image=%s
        WHERE id=%s
        """, (title, content, image, id))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('blog_add'))


#=========================================================================



@app.route('/lienhe', methods=['POST'])

def submit_contact_form():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    # name = request.form['name']
    # email = request.form['email']
    # message = request.form['message']
    # # Xử lý biểu mẫu ở đây
    # # ...
    # # Sau khi xử lý xong, chuyển hướng người dùng đến trang cảm ơn
    # return redirect(url_for('thank_you'))
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # sender_email = 'nguyendangbdu@gmail.com'
    # sender_password = 'iwqwezrauthwxvjr'

    # message = f"Subject: New message\n\nName: {name}\nEmail: {email}\nmessage: {message}"

    # recipient_email = 'nguyendangbdu@gmail.com'
    # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    #     smtp.login(sender_email, sender_password)
    # smtp.sendmail(sender_email, [recipient_email], message.as_string())

    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')







# @app.route('/product/<int:product_id>')
# def product_detail(product_id):
#     cur = mysql.connection.cursor()
#     # cur = conn.cursor()

#     # Query the database for product information based on product_id
#     query = "SELECT * FROM products WHERE id=%s"
#     cur.execute(query, (product_id,))
#     product = cur.fetchone()

#     # Query the database for related products (4 products with similar price)
#     query = "SELECT * FROM products WHERE price BETWEEN %s AND %s AND id != %s LIMIT 4"
#     cur.execute(query, (Decimal(product[3])*Decimal('0.9'), Decimal(product[3])*Decimal('1.1'), product_id))
#     related_products = cur.fetchall()

#     # Query the database for 8 more related products
#     query = "SELECT * FROM products WHERE price BETWEEN %s AND %s AND id != %s LIMIT 8"
#     cur.execute(query, (Decimal(product[3])*Decimal('0.8'), Decimal(product[3])*Decimal('1.2'), product_id))
#     more_related_products = cur.fetchall()

#     cur.close()
#     return render_template('product_detail.html', product=product, related_products=related_products, more_related_products=more_related_products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Lấy thông tin username và password từ form đăng nhập
        username = request.form['username']
        password = request.form['password']

        # Kết nối tới MySQL Workbench
        cur = mysql.connection.cursor()

# Thực hiện truy vấn để kiểm tra thông tin đăng nhập
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user_data = cur.fetchone()

        # Đóng kết nối tới MySQL Workbench
        cur.close()

        # Nếu thông tin đăng nhập chính xác, lưu thông tin user vào session và chuyển hướng tới trang chủ
        if user_data:
            user = {
                'id': user_data[0],
                'username': user_data[1],
                'password': user_data[2],
                'role': user_data[3]
            }
            session['user'] = user
            if user['role'] == 'admin':
                return redirect(url_for('sukien'))
            elif user['role'] == 'kh':
                return redirect(url_for('banhangmk'))
        else:
            error = "Đăng nhập không thành công. Vui lòng kiểm tra lại thông tin đăng nhập!"

    # Nếu không phải là phương thức POST hoặc thông tin đăng nhập không chính xác, hiển thị lại trang đăng nhập
    return render_template('login.html', error=error)

# Định nghĩa route cho trang đăng xuất
@app.route('/logout')
def logout():
    # Xóa thông tin user trong session và chuyển hướng tới trang đăng nhập
    session.pop('user', None)
    return redirect(url_for('trangchu'))

# Xóa thông tin người dùng khỏi session và chuyển hướng tới trang đăng nhập

@app.route('/')
def trangchu():
    cur = mysql.connection.cursor()
    cur.execute("SELECT title, content, image FROM posts")
    posts = cur.fetchall()
    return render_template('trangchu.html', posts=posts)
@app.route('/post/<int:post_id>')
def post_detail(post_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT title, content, image FROM posts WHERE id=%s", (post_id,))
    post = cur.fetchone()
    cur.close()
    return render_template('post_detail.html', post=post)



@app.route('/lienhe')
def lienhe():

    return render_template('lienhe.html')
@app.route('/sukien')
def sukien():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM su_kien")
    data = cur.fetchall()
    cur.close()

    return render_template('sukien.html', su_kien=data)



from datetime import datetime
import csv
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib.font_manager as font_manager
import base64
from collections import Counter
import os
from flask import render_template, request


# @app.route('/sodo', methods=['GET', 'POST'])
# def sodo():
#     # Lấy ngày từ biểu mẫu hoặc sử dụng ngày hiện tại
#     date_str = request.args.get('date', str(datetime.now().date()))

#     # Chuyển đổi chuỗi ngày thành đối tượng datetime
#     date = datetime.strptime(date_str, '%Y-%m-%d').date()

#     # Đọc dữ liệu từ file text và lọc theo ngày
#     values = []
#     data_dir = r'D:\test_rasa\Customdata'

#     path = os.path.join(data_dir, date.strftime('%d-%m-%Y.csv'))
#     if os.path.exists(path):
#         with open(path, 'r', encoding='utf-8') as file:
#             reader = csv.reader(file)
#             next(reader)  # Bỏ qua tiêu đề
#             for row in reader:
#                 # Chuyển đổi chuỗi ngày trong file thành đối tượng datetime
#                 row_date = datetime.strptime(row[1], '%Y-%m-%d').date()

#                 # Nếu dòng trong file có ngày bằng với ngày cần lọc, thêm giá trị vào danh sách
#                 if row_date == date:
#                     values.append(row[0])

#     # Đếm số lần xuất hiện của mỗi giá trị
#     counter = Counter(values)

#     # Tạo biểu đồ
#     labels = list(counter.keys())
#     sizes = list(counter.values())
#     fig, ax = plt.subplots()
#     ax.pie(sizes, labels=labels, autopct='%1.1f%%')
#     ax.axis('equal')
#     fig.set_size_inches(8, 6)

#     # Lưu biểu đồ vào buffer
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)

#     # Chuyển đổi biểu đồ thành chuỗi base64
#     chart = base64.b64encode(buffer.read()).decode('utf-8')

#     # Trả về template HTML với biểu đồ được chèn vào, và cho phép người dùng chọn ngày để lọc dữ liệu
#     return render_template('sodo.html', chart=chart, date=date_str)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        ten_su_kien = request.form['ten_su_kien']
        thong_tin_su_kien = request.form['thong_tin_su_kien']
        ngay_bat_dau = request.form['ngay_bat_dau']
        ngay_ket_thuc = request.form['ngay_ket_thuc']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO su_kien (ten_su_kien, thong_tin_su_kien, ngay_bat_dau, ngay_ket_thuc) VALUES (%s, %s, %s, %s)", (ten_su_kien, thong_tin_su_kien, ngay_bat_dau, ngay_ket_thuc))
        mysql.connection.commit()
        return redirect(url_for('sukien'))

@app.route('/deletesk/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM su_kien WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('sukien'))



@app.route('/updatesk', methods= ['POST', 'GET'])
def updatesk():
    if request.method == 'POST':
        id_data = request.form['id']
        ten_su_kien = request.form['ten_su_kien']
        thong_tin_su_kien = request.form['thong_tin_su_kien']
        ngay_bat_dau = request.form['ngay_bat_dau']
        ngay_ket_thuc = request.form['ngay_ket_thuc']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE su_kien SET ten_su_kien=%s, thong_tin_su_kien=%s, ngay_bat_dau=%s, ngay_ket_thuc=%s
        WHERE id=%s
        """, (ten_su_kien, thong_tin_su_kien, ngay_bat_dau,ngay_ket_thuc, id_data))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('sukien'))
    

#chinhanh

@app.route('/chinhanh')
def chinhanh():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customer")
    data = cur.fetchall()
    cur.close()

    return render_template('chinhanh.html', customer=data)


@app.route('/insertcn', methods = ['POST'])
def insertcn():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        chi_nhanh = request.form['chi_nhanh']
        dia_chi = request.form['dia_chi']
        link = request.form['link']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer (chi_nhanh, dia_chi, link) VALUES (%s, %s, %s)", (chi_nhanh, dia_chi, link))
        mysql.connection.commit()
        return redirect(url_for('chinhanh'))


@app.route('/deletecn/<string:id_data>', methods = ['GET'])
def deletecn(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customer WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('chinhanh'))
    # return render_template('chinhanh.html')

@app.route('/updatecn', methods= ['POST', 'GET'])
def updatecn():
    if request.method == 'POST':
        id_data = request.form['id']
        chi_nhanh = request.form['chi_nhanh']
        dia_chi = request.form['dia_chi']
        link = request.form['link']
        # phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE customer SET chi_nhanh=%s, dia_chi=%s, link=%s
        WHERE id=%s
        """, (chi_nhanh, dia_chi,link, id_data))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('chinhanh'))
#khachhang
@app.route('/khachhang')
def khachhang():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM thong_tin_khach_hang_2")
    data = cur.fetchall()
    cur.close()
    return render_template('khachhang.html', thong_tin_khach_hang_2=data)
@app.route('/insertkh', methods = ['POST'])
def insertkh():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        ten = request.form['ten']
        sdt = request.form['sdt']
        # link = request.form['link']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO thong_tin_khach_hang_2 (ten, sdt) VALUES (%s, %s)", (ten, sdt))
        mysql.connection.commit()
        return redirect(url_for('khachhang'))

@app.route('/deletekh/<string:id_data>', methods = ['GET'])
def deletekh(id_data):
    flash("Xóa thành công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM thong_tin_khach_hang_2 WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('khachhang'))

@app.route('/updatekh', methods= ['POST', 'GET'])
def updatekh():
    if request.method == 'POST':
        id = request.form['id']
        ten = request.form['ten']
        sdt = request.form['sdt']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE thong_tin_khach_hang_2 SET ten=%s, sdt=%s
        WHERE id=%s
        """, (ten, sdt, id))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('khachhang'))

if __name__ == "__main__":
    app.run(debug=True)
