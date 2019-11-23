import os
from dotenv import load_dotenv
from discord.ext import commands
import mysql.connector

load_dotenv()
owner = os.getenv('owner')


def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == owner)


def db_connect():
    connection = mysql.connector.connect(
        host='localhost',
        database='cs_discord_bot',
        user='hillari',
        # charset='utf8mb4',
        password='password',
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
    connection = db_connect()
    mycursor = connection.cursor()
    # with db.cursor() as cursor:
    # id = (str(guild.id) + str(member.id))
    sql = "INSERT INTO members(discord_id, username, role, " \
          "experience, level, reputation, warnings) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s);"
    data = (member.id, str(member.name), 'role', 0, 0, 0, 0)
    mycursor.execute(sql, data)
    connection.commit()
    mycursor.close()
    connection.close()


def get_member(member, guild):
    connection = db_connect()
    mycursor = connection.cursor()
    sql = "SELECT discord_id, username,role,experience,level" \
          "reputation, warnings FROM members WHERE id=%s"
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
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | id         | int(11)      | NO   | PRI | NULL    | auto_increment |
# | discord_id | bigint(20)   | YES  |     | NULL    |                |
# | username   | varchar(255) | YES  |     | NULL    |                |
# | role       | varchar(255) | YES  |     | NULL    |                |
# | experience | int(11)      | YES  |     | NULL    |                |
# | level      | int(11)      | YES  |     | NULL    |                |
# | reputation | int(11)      | YES  |     | NULL    |                |
# | warnings   | varchar(255) | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+

