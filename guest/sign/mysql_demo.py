from pymysql import cursors, connect

# 链接数据库
coon = connect(
    host="12.0.0.1",
    user="admin",
    db="guest",
    charset="utf8mb4",
    cursorclass=cursors.DictCursor
)

try:
    with coon.cursor() as cursor:
        # 创建嘉宾数据
        sql = 'INSERT INTO sign_guest (realname, phone, email, sign, event_id, create_time) VALUES ("tome", 15311859286, "tom@qq.com", 0,1,NOW());'
        cursor.execute(sql)
        # 提交事务
    coon.commit()

finally:
    coon.close()