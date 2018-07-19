import MySQLdb


db = MySQLdb.connect("localhost", "root", "", "trimm-api")

cursor = db.cursor()

create_tables = """
                DROP TABLE IF EXISTS users;

                CREATE TABLE users (
                    user_id       INT auto_increment not null,
                    user_uuid     VARCHAR(36) NOT NULL,
                    user_name     VARCHAR(255) NOT NULL,
                    user_email    VARCHAR(255) NOT NULL,
                    user_password VARCHAR(255) NOT NULL,
                    PRIMARY KEY CLUSTERED (user_uuid ASC, user_id ASC)
                );

                DROP TABLE IF EXISTS categories;
                
                CREATE TABLE categories (
                    cat_name   NVARCHAR(255) NOT NULL,
                    cat_id     INT auto_increment NOT NULL,
                    cat_budget NVARCHAR(255) NULL,
                    user_uuid  NVARCHAR(255) NOT NULL,
                    user_id    INT NOT NULL,

                    PRIMARY KEY CLUSTERED (cat_name ASC, cat_id ASC),
                    FOREIGN KEY (user_uuid, user_id)
                    REFERENCES users(user_uuid, user_id)
                );
                
                DROP TABLE IF EXISTS spending;

                CREATE TABLE spending (
                    item_id     INT auto_increment NOT NULL,
                    item_name   NVARCHAR(255) NOT NULL,
                    item_price  FLOAT NOT NULL,
                    create_dttm DATETIME NOT NULL,
                    cat_name    NVARCHAR(255) NOT NULL,
                    cat_id      INT NOT NULL,
                    user_uuid   NVARCHAR(255) NOT NULL,
                    user_id     INT NOT NULL,

                    PRIMARY KEY CLUSTERED (item_id ASC),
                    FOREIGN KEY (cat_name, cat_id)
                    REFERENCES categories(cat_name, cat_id),
                    FOREIGN KEY (user_uuid, user_id)
                    REFERENCES users(user_uuid, user_id)
                );"""

cursor.execute(create_tables)

db.close()
