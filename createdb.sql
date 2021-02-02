CREATE TABLE groups(
    name VARCHAR(30) PRIMARY KEY
);

CREATE TABLE members(
    id INTEGER PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE member_group(
    member_id INTEGER NOT NULL,
    group_name VARCHAR(30) NOT NULL,
    headman BOOLEAN DEFAULT 0,
    FOREIGN KEY (member_id) REFERENCES members(id)
    FOREIGN KEY (group_name) REFERENCES groups(name)
);

CREATE TABLE category(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50),
    aliases TEXT,
    group_name VARCHAR(30),
    FOREIGN KEY (group_name) REFERENCES groups(name)
);

CREATE TABLE homework(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category INTEGER,
    created_date DATETIME,
    FOREIGN KEY(category) REFERENCES category(id)
);



-- CREATE TABLE attached_file();