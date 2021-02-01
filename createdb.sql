CREATE TABLE groups(
    name VARCHAR(30) PRIMARY KEY
    
);

CREATE TABLE members(
    id INTEGER PRIMARY KEY,
    name VARCHAR(50)
    
);

CREATE TABLE category(
    codename VARCHAR(255),
    category_name VARCHAR(255),
    aliases TEXT
    
    
);

CREATE TABLE member_group(
    member_id INTEGER NOT NULL,
    group_name VARCHAR(30) NOT NULL,
    headman BOOLEAN DEFAULT 0,
    FOREIGN KEY (member_id) REFERENCES members(id)
    FOREIGN KEY (group_name) REFERENCES groups(name)

);

 
CREATE TABLE homework(
    id integer primary key,
    created datetime,
    category_codename integer,
    subgroup varchar(50),
    theme text,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

-- CREATE TABLE attached_file();