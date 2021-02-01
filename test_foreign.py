import sqlite3




conn = sqlite3.connect("db.db")
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()


cursor.execute('''CREATE TABLE group_list(
    codename varchar(255) primary key, 
    amount_sub integer,
    
    
    
    );''')


cursor.execute('''CREATE TABLE member(
    member_id varchar(50) primary key,
    subgroup varchar(50),
    headman boolean,
    group_codename integer,
    FOREIGN KEY(group_codename) REFERENCES group_list(codename)
);
 ''')



cursor.execute('INSERT INTO member VALUES ("5вы4323","2",true,)')

conn.commit()