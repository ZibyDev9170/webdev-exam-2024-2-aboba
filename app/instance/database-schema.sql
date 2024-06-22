CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE cover (
	id INTEGER NOT NULL, 
	filename VARCHAR NOT NULL, 
	mime_type VARCHAR NOT NULL, 
	md5_hash VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE genre (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE role (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	description TEXT NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE book (
	id INTEGER NOT NULL, 
	title VARCHAR NOT NULL, 
	description TEXT NOT NULL, 
	year INTEGER NOT NULL, 
	publisher VARCHAR NOT NULL, 
	author VARCHAR NOT NULL, 
	pages INTEGER NOT NULL, 
	cover_id INTEGER NOT NULL, rating_count INTEGER NOT NULL, rating_sum INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cover_id) REFERENCES cover (id)
);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR NOT NULL, 
	password_hash VARCHAR NOT NULL, 
	last_name VARCHAR NOT NULL, 
	first_name VARCHAR NOT NULL, 
	middle_name VARCHAR, 
	role_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(role_id) REFERENCES role (id)
);
CREATE TABLE book_genre (
	book_id INTEGER NOT NULL, 
	genre_id INTEGER NOT NULL, 
	PRIMARY KEY (book_id, genre_id), 
	FOREIGN KEY(book_id) REFERENCES book (id), 
	FOREIGN KEY(genre_id) REFERENCES genre (id)
);
CREATE TABLE review (
	id INTEGER NOT NULL, 
	book_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	rating INTEGER NOT NULL, 
	text TEXT NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(book_id) REFERENCES book (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
