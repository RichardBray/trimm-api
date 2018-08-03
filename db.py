import MySQLdb
from tornado.options import define, options, parse_config_file

define("db_user", default="root2")
define("db_host", default="localhost")
define("db_password", default="localhost")
define("db_name", default="trimm-api")

parse_config_file("./config/local.conf")

db = MySQLdb.connect(options.db_host, options.db_user,
                     options.db_password, options.db_name)

cursor = db.cursor()

create_tables = """                
                DROP TABLE IF EXISTS users;

                CREATE TABLE users (
                    user_id       INT AUTO_INCREMENT,
                    user_uuid     VARCHAR(36) NOT NULL,
                    user_name     VARCHAR(255) NOT NULL,
                    user_email    VARCHAR(255) NOT NULL,
                    user_password VARCHAR(255) NOT NULL,
                    user_currency VARCHAR(36)  NOT NULL,
                    PRIMARY KEY (user_id)
                );
                
                DROP TABLE IF EXISTS categories;
                
                CREATE TABLE categories (
                    cat_id     INT AUTO_INCREMENT,
                    cat_uuid   VARCHAR(36) NOT NULL,
                    cat_name   VARCHAR(255) NOT NULL,
                    cat_total  INT NULL,
                    cat_budget INT NULL,
                    user_id    INT NOT NULL,

                    PRIMARY KEY (cat_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );                
                
                DROP TABLE IF EXISTS spending;

                CREATE TABLE spending (
                    item_id     INT AUTO_INCREMENT,
                    item_uuid   VARCHAR(36) NOT NULL,
                    item_name   VARCHAR(255) NOT NULL,
                    item_price  FLOAT NOT NULL,
                    create_dttm DATETIME NOT NULL,
                    cat_id      INT NOT NULL,
                    user_id     INT NOT NULL,

                    PRIMARY KEY (item_id),
                    FOREIGN KEY (cat_id) REFERENCES categories(cat_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );"""

cursor.execute(create_tables)

db.close()
