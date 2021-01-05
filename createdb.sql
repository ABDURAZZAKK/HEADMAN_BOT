CREATE TABLE group_list(
    codename varchar(255) primary key
    
);

CREATE TABLE member(
    member_id varchar(50) primary key,
    subgroup varchar(50),
    headman boolean,
    group_codename integer,
    FOREIGN KEY(group_codename) REFERENCES group_list(codename)
);

CREATE TABLE category(
    codename varchar(255),
    name varchar(255),
    aliases text
    
);
 
CREATE TABLE homework(
    id integer primary key,
    created datetime,
    category_codename integer,
    theme text,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

-- CREATE TABLE attached_file();