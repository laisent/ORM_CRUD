from pymysql import connect
"""将原本的User类中的功能抽取到基类中"""


class ModelMetaclass(type):
    """元类 继承type 将类属性转化成映射"""

    def __new__(cls, name, bases, attrs):
        mappings = dict()
        for key, values in attrs.items():
            # 判断是否是指定的StringField or IntegerField的实例对象
            if isinstance(values, tuple):
                print("Found mapping: %s ==> %s" % (key, values))
                mappings[key] = values

        # 删除这些已经在字典中存储的属性
        for k in mappings.keys():
            attrs.pop(k)

        # 将之前的uid/name/email/password以及对应的对象引用、类名字
        attrs["__mappings__"] = mappings  # 保存属性和列的映射关系
        attrs["__tablename__"] = name  # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)


class Model(object, metaclass=ModelMetaclass):
    """
        通过元类ModelMetaclass 创建User类
        下列类属性不在新建的类中 在__mappings__里有保存属性和列的映射关系
        __mappings__ = {
          "udi":('uid', "int unsigned"),
          "name":('username', "varchar(30)")
          "email":('email', "varchar(30)")
          "password":('password', "varchar(30)")
        }
        还有个属性保存表名 __tablename__ = "User"
        """
    def __init__(self, **kwargs):
        for name, values in kwargs.items():
            setattr(self, name, values)

    def save(self):
        """Create"""
        # 数据表关键字 fields
        fields = list()
        # 传入参数 args
        args = list()
        # 从__mappings__映射中读取数据表列关键字 传入参数
        for key, values in self.__mappings__.items():
            # values  ('uid', "int unsigned")
            fields.append(values[0])
            args.append(getattr(self, key, None))
        # 数据类型校验 int类型转成字符串 字符串加一层引号 方便后面join可以去除引号
        args_temp = list()
        for temp in args:
            if isinstance(temp, int):
                args_temp.append(str(temp))
            elif isinstance(temp, str):
                args_temp.append("""'%s'""" % temp)

        sql = "insert into %s (%s) values (%s);" % \
              (self.__tablename__, ",".join(fields), ",".join(args_temp))
        print("*" * 50)
        print("Create SQL: %s" % sql)

    def find(self):
        """Retrieve"""
        fields = list()
        # 从__mappings__映射中读取数据表列关键字 传入参数
        for key, values in self.__mappings__.items():
            # values  ('uid', "int unsigned")
            fields.append(values[0])

        sql = "select (%s) from %s;" % (",".join(fields), self.__tablename__)
        print("*" * 50)
        print("Retrieve SQL: %s" % sql)

    def update(self, keywords, values, id):
        """Update"""
        # 接受参数:
        #   1.要更改的列名 以tuple方式 ("name", "password")
        #   2.修改成的目标 以tuple方式 ("root", "1234")
        #   3.主键id    12345
        args = list()
        for i in range(len(keywords)):
            args.append("%s='%s'" % (keywords[i], values[i]))  # ["name"="root", "password"="1234"]

        sql = "update %s set %s where uid=%s;" % (self.__tablename__, ",".join(args), id)
        print("*" * 50)
        print("Update SQL: %s" % sql)

    def delete(self, uid):
        """Delete"""
        sql = "delete from %s where uid=%s;" % (self.__tablename__, uid)
        print("*" * 50)
        print("Delete SQL: %s" % sql)


class User(Model):
    uid = ('uid', "int unsigned")
    name = ('username', "varchar(30)")
    email = ('email', "varchar(30)")
    password = ('password', "varchar(30)")


if __name__ == "__main__":
    user = User(uid=12345, name='laisent', email='laisent@163.com', password='root')
    user.save()
    user.find()
    user.update(("name", "password"), ("root", "1234"), 12345)
    user.delete(1245)
