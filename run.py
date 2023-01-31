from flask import Flask, render_template, request
import pikepdf
import sqlite3

app = Flask(__name__)

filemetadata = None
def get_db():
    db = sqlite3.connect('metadata.db')
    db.execute(
        """CREATE TABLE IF NOT EXISTS metadata (
                    id integer primary key autoincrement
                );"""
    )
    db.close()
    return db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metadata', methods=['POST'])
def metadata():
    global filemetadata
    file = request.files['file']
    pdf = pikepdf.Pdf.open(file)
    pdf_info = pdf.docinfo
    filemetadata = {}
    for key, value in pdf_info.items():
        formatted_key = key.replace("/", "")
        filemetadata[formatted_key] = value
    return render_template('metadata.html',metadata=filemetadata)





@app.route('/addtobdd',methods=['POST'])
def addtodb():
    global filemetadata 
    message = "Values have been added to the database!"  
    get_db()
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    keys_list = []
    values_list = []

    for key, value in filemetadata.items():
        print("here ", value)
        keys_list.append(key)
        values_list.append(str(value))
        cursor.execute("SELECT sql FROM sqlite_master WHERE name='metadata' AND type='table'")
        table_query = cursor.fetchone()[0]
        
        if key not in table_query:
            print("The column 'key' does not exist in the table 'metadata'.")
            cursor.execute(f"ALTER TABLE metadata ADD COLUMN {key} text")
            conn.commit()
    
    print("--------- Start adding data ------------")
    print("Added keys : ", keys_list)
    print("Added values : ", values_list)
    
    query = f"INSERT INTO metadata  ({','.join(keys_list)}) VALUES ({','.join(['?' for v in values_list])})"
    cursor.execute(query, values_list)
    conn.commit()   
    conn.close()
    return render_template('index.html',message=message)

@app.route('/list',methods=['GET'])
def display_table():
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM metadata")
    rows = cursor.fetchall()
    
    cursor.execute("PRAGMA table_info(metadata)")
    table_info = cursor.fetchall()
    column_names = [info[1] for info in table_info]

    table_data = []
    for row in rows:
        table_data.append(list(row))

    return render_template('list.html', table_data=table_data,column_names=column_names)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        id = request.form['id']
        conn = sqlite3.connect('metadata.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM metadata WHERE id=?", (id,))
        result = cursor.fetchone()
        
        cursor.execute("PRAGMA table_info(metadata)")
        table_info = cursor.fetchall()
        column_names = [info[1] for info in table_info]
        
        conn.close()
        data_table ={}
        if result:
            print(result)
            data_table = dict(zip(column_names, result))
            print(data_table)
            return render_template('search.html', result=result, data_table=data_table)
        else:
            message = "No such metadata found with the given id."
            return render_template('search.html', message=message)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
