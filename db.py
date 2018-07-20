import MySQLdb


db = MySQLdb.connect("localhost", "root", "", "trimm-api")

cursor = db.cursor()

create_tables = """                
                DROP TABLE IF EXISTS spending;

                CREATE TABLE spending (
                    item_id     INT(11) AUTO_INCREMENT,
                    item_name   VARCHAR(255) NOT NULL,
                    item_price  FLOAT NOT NULL,
                    create_dttm DATETIME NOT NULL,
                    cat_id      INT(11) NOT NULL,
                    user_id     INT(11) NOT NULL,

                    PRIMARY KEY (item_id),
                    FOREIGN KEY (cat_id)
                    REFERENCES categories(cat_id),
                    FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                );
                
                DROP TABLE IF EXISTS categories;
                
                CREATE TABLE categories (
                    cat_id     INT(11) AUTO_INCREMENT,
                    cat_name   VARCHAR(255) NOT NULL,
                    cat_budget VARCHAR(255) NULL,
                    user_id    INT(11) NOT NULL,

                    PRIMARY KEY (cat_id),
                    FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                );                
                
                DROP TABLE IF EXISTS users;

                CREATE TABLE users (
                    user_id       INT(11) AUTO_INCREMENT,
                    user_uuid     VARCHAR(36) NOT NULL,
                    user_name     VARCHAR(255) NOT NULL,
                    user_email    VARCHAR(255) NOT NULL,
                    user_password VARCHAR(255) NOT NULL,
                    PRIMARY KEY (user_id)
                );"""

cursor.execute(create_tables)

db.close()
