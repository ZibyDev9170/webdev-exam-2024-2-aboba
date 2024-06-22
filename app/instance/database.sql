PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('0f0d0eaab60f');
CREATE TABLE cover (
	id INTEGER NOT NULL, 
	filename VARCHAR NOT NULL, 
	mime_type VARCHAR NOT NULL, 
	md5_hash VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO cover VALUES(1,'qwerty.jpg','image/jpeg','2e9ac8b46bc55121d03e4d178693b97f');
INSERT INTO cover VALUES(2,'qwerty.jpg','image/jpeg','2e9ac8b46bc55121d03e4d178693b97f');
INSERT INTO cover VALUES(3,'qwerty.jpg','image/jpeg','2e9ac8b46bc55121d03e4d178693b97f');
INSERT INTO cover VALUES(4,'qwerty.png','image/png','8d36b86abd635aae289bdbd90647c96f');
INSERT INTO cover VALUES(5,'qwerty.png','image/png','8d36b86abd635aae289bdbd90647c96f');
INSERT INTO cover VALUES(6,'qwerty.jpg','image/jpeg','2e9ac8b46bc55121d03e4d178693b97f');
INSERT INTO cover VALUES(7,'qwerty.jpg','image/jpeg','2e9ac8b46bc55121d03e4d178693b97f');
INSERT INTO cover VALUES(8,'qwerty.png','image/png','8d36b86abd635aae289bdbd90647c96f');
INSERT INTO cover VALUES(9,'qwerty.png','image/png','8d36b86abd635aae289bdbd90647c96f');
INSERT INTO cover VALUES(10,'qwerty.png','image/png','8d36b86abd635aae289bdbd90647c96f');
INSERT INTO cover VALUES(11,'qwerty.jpg','image/jpeg','2e9ac8b46bc55121d03e4d178693b97f');
INSERT INTO cover VALUES(12,'qwerty.jpg','image/jpeg','2e9ac8b46bc55121d03e4d178693b97f');
INSERT INTO cover VALUES(13,'qwerty.jpg','image/jpeg','2e9ac8b46bc55121d03e4d178693b97f');
INSERT INTO cover VALUES(14,'qwerty.jpg','image/jpeg','2e9ac8b46bc55121d03e4d178693b97f');
INSERT INTO cover VALUES(15,'qwerty.png','image/png','8d36b86abd635aae289bdbd90647c96f');
INSERT INTO cover VALUES(16,'qwerty.jpg','image/jpeg','2e9ac8b46bc55121d03e4d178693b97f');
INSERT INTO cover VALUES(17,'warandpeace.jpg','image/jpeg','bc7106252594fe401d0e91588d9085a3');
INSERT INTO cover VALUES(18,'111.jpg','image/jpeg','e86e27af66ca98ca50f87cc8268fca21');
CREATE TABLE genre (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO genre VALUES(1,'Романтика');
INSERT INTO genre VALUES(2,'Комедия');
INSERT INTO genre VALUES(3,'Детектив');
INSERT INTO genre VALUES(4,'Приключение');
CREATE TABLE role (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	description TEXT NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO role VALUES(1,'Администратор','Суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг');
INSERT INTO role VALUES(2,'Модератор','Может редактировать данные книг и производить модерацию рецензий');
INSERT INTO role VALUES(3,'Пользователь','Может оставлять рецензии');
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
INSERT INTO book VALUES(1,'Альманах политеха','Альманах политеха',2024,'Политех','Я',200,16,2,9);
INSERT INTO book VALUES(2,'Ленин',replace(replace('Натан Альтман в первые послереволюционные годы стал одной из главных фигур в строительстве нового искусства. Он был одним из первых художников, откликнувшихся на призыв советской власти к сотрудничеству с художниками и писателями вместе с В.Мейерхольдом, А.Блоком, В.Маяковским, Р.Ивневым. Н.Альтман работал в Петроградской коллегии по делам искусств, занимал руководящие посты в петроградском и московском отделах ИЗО Наркомпроса, редактировал газету «Искусство коммуны» и журнал «Пламя», сотрудничал в Институте художественной культуры, руководил созданием Музея художественной культуры, устраивал выставки. Альтман был также одним из организаторов, а также автором скульптурных работ по плану монументальной пропаганды, который подразумевал появление на улицах и площадях множества памятников новым героям. Кроме того, художник работал над агитационным фарфором, расписывая посуду советской символикой, лозунгами, сюжетами из новой жизни. Наиболее грандиозным агитационно-массовым проектом Н.Альтмана было оформление главной площади Петрограда к первой годовщине Октябрьской революции.\r\n\r\nНеслучайно Н.Альтман был приглашен в ленинский кабинет для создания бюста В.И.Ленина. Первой его работой в таком роде было создание барельефа и бюста первого наркома культуры А.В.Луначарского в гипсе (1920 г.). Наркому понравилась получившаяся скульптура и он поручил Н.Альтману изготовить портрет В.И.Ленина. Заочно Ленин был уже знаком с художником. Сделанный им эскиз флага РСФСР был одобрен вождем как лучший. Н.Альтман работал в кремлевском кабинете шесть недель, так как В.И.Ленин отказался выделить отдельное время для позирования. К июню 1920 г. бюст был готов.','\r',char(13)),'\n',char(10)),1990,'Российские книги','Натан Альтман',150,15,1,5);
INSERT INTO book VALUES(3,'Война и Мир',replace(replace('«Война и мир» — роман Льва Толстого, в котором автор описывает человеческие жизни на фоне грандиозного исторического события — вторжения французской армии во главе с Наполеоном.\r\n\r\nМирная жизнь со всеми её прелестями в виде балов, светских правил и приёмов противопоставляется жизни военной и поиску смысла существования. На примере нескольких семей автор показывает любовь и предательство, интриги и честь, попытки жить только для себя или на благо общества.\r\n\r\nВ романе-эпопее «Война и мир» два исторических плана: начало века и его середина. Это позволяет сравнить, как менялись надежды, проблемы и чаяния целого народа под влиянием времени.\r\n\r\nТолстого волновали вопросы общественной роли дворянства, а также истинного и ложного патриотизма, предназначения женщины и даже эмансипации.','\r',char(13)),'\n',char(10)),2010,'Эксмо','Лев Николаевич Толстой',1472,17,1,3);
INSERT INTO book VALUES(4,'Преступление и наказание',replace(replace('"Преступление и наказание" (1866) — одно из самых значительных произведений в истории мировой литературы. Это и глубокий филососфский роман, и тонкая психологическая драма, и захватывающий детектив, и величественная картина мрачного города, в недрах которого герои грешат и ищут прощения, жертвуют собой и отрекаются от себя ради ближних и находят успокоение в смирении, покаянии, вере. Главный герой романа Родион Раскольников решается на убийство, чтобы доказать себе и миру, что он не "тварь дрожащая", а "право имеет". Главным предметом исследования писателя становится процесс превращения добропорядочного, умного и доброго юноши в убийцу, а также то, как совершивший преступление Раскольников может искупить свою вину. \r\nТеги: Преступление и наказание, Достоевский, Федор Достоевский, Преступление и наказание Достоевский, Достоевский Преступление и наказание, Идиот Достоевский, Бесы Достоевский, Достоевский Идиот, Белые ночи Достоевский, Достоевский Бесы, книги, книга, книги классика, книги художественная литература, книжка, книжки, книги романы, романы, роман, книга роман, художественная литература, книги художественная литература, литература, классическая литература, всемирная литература, художественная литература классика, классическая литература книги, классика, мировая классика, книги классика русская, художественная литература для детей, книги для подростков, книга для подростков.','\r',char(13)),'\n',char(10)),2012,'АСТ','Федор Михайлович Достоевский',672,18,0,0);
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
INSERT INTO user VALUES(1,'admin','scrypt:32768:8:1$prFq8X7JUKy1nsIR$deef5b9ecf883efbf91f4cb335061a3fda792e81df1493694496924b7df9f60fe6282efe9800cf2ea6f7e7c1ee67488269321987a5ee4559c4ae6722ad17dc43','Иванов','Иван','Иванович',1);
INSERT INTO user VALUES(2,'moderator','scrypt:32768:8:1$wPiJ3DQ75ddbUflR$3435f0c7eef1b6f3e5f79eb4ba88ef4fb7236043423003a9524ed24da5f0995b3d4214b9dc9e19707759075b729e27ad9a08053584c8c7ebba8affcbe89cb005','Петров','Петр','Петрович',2);
INSERT INTO user VALUES(3,'user','scrypt:32768:8:1$ZAPtNDCcgllGhidI$1f09becde9b0dc1fff098c21a06d0acb21722040bb1a9a71c5f513e5bb6c7e01c109881b2c6f07cae9beaeb79f23be513408ab05a07e76846c1758554feee785','Сидоров','Сидор','Сидорович',3);
CREATE TABLE book_genre (
	book_id INTEGER NOT NULL, 
	genre_id INTEGER NOT NULL, 
	PRIMARY KEY (book_id, genre_id), 
	FOREIGN KEY(book_id) REFERENCES book (id), 
	FOREIGN KEY(genre_id) REFERENCES genre (id)
);
INSERT INTO book_genre VALUES(1,1);
INSERT INTO book_genre VALUES(1,2);
INSERT INTO book_genre VALUES(2,4);
INSERT INTO book_genre VALUES(3,1);
INSERT INTO book_genre VALUES(3,4);
INSERT INTO book_genre VALUES(4,1);
INSERT INTO book_genre VALUES(4,3);
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
INSERT INTO review VALUES(1,1,3,4,'Хороший альманах','2024-06-15 12:30:54');
INSERT INTO review VALUES(2,1,2,5,'Отличный альманах','2024-06-15 13:32:26');
INSERT INTO review VALUES(3,2,3,5,'Мне очень понравилась книга и я бы хотел сказать, что это достойное приключение!','2024-06-15 19:25:02');
INSERT INTO review VALUES(4,3,1,3,'Многа букав. Не хочеца букавы читать.','2024-06-16 11:45:52');
COMMIT;
