import MySQLdb


db = MySQLdb.connect("localhost", "root", "", "trimm-api")

cursor = db.cursor()

create_tables = """
                DROP TABLE IF EXISTS [spending];
                DROP TABLE IF EXISTS [categories];
                DROP TABLE IF EXISTS [users];

                CREATE TABLE [users] (
                    [user_id]       INT NOT NULL,
                    [user_uuid]     NVARCHAR(MAX) NOT NULL,
                    [user_name]     NVARCHAR(MAX) NOT NULL,
                    [user_email]    NVARCHAR(MAX) NOT NULL,
                    [user_password] NVARCHAR(MAX) NOT NULL,
                    CONSTRAINT [PK_Users] PRIMARY KEY CLUSTERED ([user_uuid] ASC, [user_id] ASC)
                );
                
                CREATE TABLE [categories] (
                    [cat_name]   NVARCHAR(MAX) NOT NULL,
                    [cat_id]     INT NOT NULL,
                    [cat_budget] NVARCHAR(MAX) NULL,
                    [user_uuid]  NVARCHAR(MAX) NOT NULL,
                    [user_id]    INT NOT NULL,

                    CONSTRAINT [PK_Categories] PRIMARY KEY CLUSTERED ([cat_name] ASC, [cat_id] ASC),
                    CONSTRAINT [FK_126] FOREIGN KEY ([user_uuid], [user_id])
                    REFERENCES [users]([user_uuid], [user_id])
                );
                
                CREATE TABLE [spending] (
                    [item_id]     INT NOT NULL,
                    [item_name]   NVARCHAR(MAX) NOT NULL,
                    [item_price]  FLOAT NOT NULL,
                    [create_dttm] DATETIME NOT NULL,
                    [cat_name]    NVARCHAR(MAX) NOT NULL,
                    [cat_id]      INT NOT NULL,
                    [user_uuid]   NVARCHAR(MAX) NOT NULL,
                    [user_id]     INT NOT NULL,

                    CONSTRAINT [PK_Spending] PRIMARY KEY CLUSTERED ([item_id] ASC),
                    CONSTRAINT [FK_100] FOREIGN KEY ([cat_name], [cat_id])
                    REFERENCES [categories]([cat_name], [cat_id]),
                    CONSTRAINT [FK_112] FOREIGN KEY ([user_uuid], [user_id])
                    REFERENCES [users]([user_uuid], [user_id])
                );"""

cursor.execute(create_tables)

db.close()
