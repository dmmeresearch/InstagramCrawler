import mysql.connector as mysql

db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
db = mysql.connect(
    host = db_hostname,
    user = "root",
    passwd = "Success123",
    database = "scamdb"
)

cursor = db.cursor()
cursor.execute("use scamdb")

# creating a table called 'users' in the 'datacamp' database
cursor.execute("CREATE TABLE INVESTORS_TAG (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, user_name VARCHAR(50),\
               Account_Creation_date VARCHAR(255),Post_Caption VARCHAR(1000),full_name VARCHAR(255), id_on_platform varchar(100), num_followers VARCHAR(30), num_following VARCHAR(30), \
         account_type INT, account_desc VARCHAR(1000),first_crawl_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, is_alive TINYINT(1) DEFAULT(1) , died_on_date TIMESTAMP,num_of_posts VARCHAR(255)")

#"INSERT INTO INVESTORS_TAG (id,user_name,full_name,id_on_platform,num_followers,num_following,account_desc) \
    #values(1,p,record[p]['full_name'],record[p]['id'],record[p]['num_of_followers'],record[p]['num_of_following'],record[p]['content'])"


#cursor.execute("DROP TABLE users")




