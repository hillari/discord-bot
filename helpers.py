import os
from dotenv import load_dotenv
from discord.ext import commands
import mysql.connector

load_dotenv()
owner = os.getenv('owner')


def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == owner)

def db_connect():
    db = mysql.connector.connect(
        host='localhost',
        database='cs_discord_bot',
        user='hillari',
        # charset='utf8mb4',
        password='password',
    )
    # print("Connection ID:", db.connection_id)
    # print(db)
    return db


def init_all_users(ctx):
    for guild in ctx.guilds:
        for member in guild.members:
            print(member.name)
            print(member.id)
            add_user_to_db(member,guild)


def add_user_to_db(member, guild):
    db = db_connect()
    mycursor = db.cursor()
    # with db.cursor() as cursor:
    # id = (str(guild.id) + str(member.id))
    sql = "INSERT INTO members(discord_id, username, role, " \
          "experience, level, reputation, warnings) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s);"
    mycursor.execute(sql, (member.id, str(member.name), "member", 0, 0, 0, 0))




# mysql> show columns in members;
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | id         | int(11)      | NO   | PRI | NULL    | auto_increment |
# | discord_id | int(11)      | NO   |     | NULL    |                |
# | username   | varchar(255) | YES  |     | NULL    |                |
# | role       | varchar(255) | YES  |     | NULL    |                |
# | experience | int(11)      | YES  |     | NULL    |                |
# | level      | int(11)      | YES  |     | NULL    |                |
# | reputation | int(11)      | YES  |     | NULL    |                |
# | warnings   | varchar(255) | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+

