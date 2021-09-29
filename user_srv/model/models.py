from peewee import *
from user_srv.settings import settings


class BaseModel(Model):
    class Meta:
        database = settings.db


class User(BaseModel):

    GENDER_CHOICE = (
        ("female", "女"),
        ("male", "男")
    )

    ROLE_CHOICE = (
        (1, "普通用户"),
        (2, "管理员")
    )

    # 用户模型
    mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号码")
    password = CharField(max_length=100, verbose_name="密码")  # 1.密码密文 2.密文不可反解
    nick_name = CharField(max_length=20, null=True, verbose_name="昵称")
    head_url = CharField(max_length=200, null=True, verbose_name="头像")
    birthday = DateField(null=True, verbose_name="生日")
    address = CharField(max_length=200, null=True, verbose_name="住址")
    desc = TextField(null=True, verbose_name="个人简介")
    gender = CharField(max_length=6, choices=GENDER_CHOICE, null=True, verbose_name="性别")
    role = IntegerField(default=1, choices=ROLE_CHOICE, verbose_name="用户角色")


if __name__ == '__main__':
    settings.db.create_tables([User])
    # 1.对称加密 2.非对称加密 无法知道原始密码可以提供url给用户用于改密码
    from passlib.hash import pbkdf2_sha256
    # for i in range(10):
    #     user = User()
    #     user.nick_name = f"yuan{i}"
    #     user.mobile = f"187822222{i}"
    #     user.password = pbkdf2_sha256.hash("admin123")
    #     user.save()

    for user in User.select():
        print(pbkdf2_sha256.verify("admin123", user.password))