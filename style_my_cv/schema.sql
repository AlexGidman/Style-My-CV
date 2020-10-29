DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS education;
DROP TABLE IF EXISTS employment;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS details;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE education (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
    user_id integer, 
    qualification varchar(255), 
    provider varchar(255), 
    grade varchar(255), 
    datestart varchar(8), 
    dateend varchar(8), 
    tag varchar(25),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE employment (
    id integer PRIMARY KEY NOT NULL, 
    user_id integer NOT NULL, 
    position varchar(255), 
    company varchar(255), 
    location varchar(255), 
    datestart varchar(8), 
    dateend varchar(8), 
    description text, 
    tag varchar(20),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE skills (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
    user_id integer NOT NULL, 
    skill varchar(255), 
    tag varchar(255),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE details (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
    user_id integer NOT NULL, 
    name text, 
    address text, 
    phone varchar(11), 
    email text, 
    linkedin text, 
    website text, 
    summary text,
    FOREIGN KEY (user_id) REFERENCES users (id)
);