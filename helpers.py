import os
from dotenv import load_dotenv
from discord.ext import commands
import mysql.connector

load_dotenv()
owner = os.getenv('owner')
dbpw = os.getenv('dbpw')


def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == owner)


def db_connect():
    connection = mysql.connector.connect(
        host='localhost',
        database='cs_bot',
        user='cs-bot',
        charset='utf8mb4',
        collation='utf8mb4_general_ci',
        password=dbpw,
        get_warnings=True
    )
    return connection


def init_all_users(ctx):
    for guild in ctx.guilds:
        for member in guild.members:
            add_user_to_db(member, guild)
            # print(member.name)
            # print(member.id)


def add_user_to_db(member, guild):
    # TODO test the user already exists code
    connection = db_connect()
    mycursor = connection.cursor()

    # This needs to be tested!
    getmembersql = "SELECT * FROM members WHERE discord_id=%s"
    mycursor.execute(getmembersql, (member.id,))
    res = mycursor.fetchone()
    if not res:
        print("New user, adding to db...")
        sql = "INSERT INTO members(discord_id, username, role, " \
              "experience, level, reputation, warnings) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s);"
        data = (member.id, str(member.name), 'role', 0, 0, 0, 0)
        mycursor.execute(sql, data)  # NOTE: execute needs same number of parameters as query
        connection.commit()
    elif res:
        print(str(member.id), "already in db")
    else:
        print("Not sure how we got here...some kinda bad thing happened")
    mycursor.close()
    connection.close()


def get_member(member, guild):
    connection = db_connect()
    mycursor = connection.cursor()
    sql = "SELECT * FROM members WHERE discord_id=%s"
    mycursor.execute(sql, (member.id,))
    result = mycursor.fetchone()
    if not result:
        print("New user, adding to db...")
        add_user_to_db(member, guild)
    else:
        return result

# INSERT  INTO members (discord_id, username, role, experience, level, reputation, warnings)  VALUES (12345, 'tuname', 'trole', 0, 0, 0, 'twarning');
# Query OK, 1 row affected (0.01 sec)


# mysql> show columns in members;
# +------------+--------------+------+-----+---------+-------+
# | Field      | Type         | Null | Key | Default | Extra |
# +------------+--------------+------+-----+---------+-------+
# | discord_id | bigint(20)   | NO   | PRI | NULL    |       |
# | username   | varchar(255) | YES  |     | NULL    |       |
# | role       | varchar(255) | YES  |     | NULL    |       |
# | experience | int(11)      | YES  |     | NULL    |       |
# | level      | int(11)      | YES  |     | NULL    |       |
# | reputation | int(11)      | YES  |     | NULL    |       |
# | warnings   | varchar(255) | YES  |     | NULL    |       |
# +------------+--------------+------+-----+---------+-------+
# 7 rows in set (0.00 sec)


# ** Fix for fucky encoding issue: (define collation/charset on creation) 
# CREATE DATABASE mydb
#   CHARACTER SET utf8
#   COLLATE utf8_general_ci;

# Creating the members table: 
# create table members (discord_id BIGINT(20), username VARCHAR(255), role VARCHAR(255), experience│
# INT(11), level INT(11), reputation INT(11), warnings VARCHAR(255), PRIMARY KEY(discord_id));
