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


class User(metaclass=ModelMetaclass):
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
    uid = ('uid', "int unsigned")
    name = ('username', "varchar(30)")
    email = ('email', "varchar(30)")
    password = ('password', "varchar(30)")

    def __init__(self, **kwargs):
        for name, values in kwargs.items():
            setattr(self, name, values)

    def save(self):
        # 数据表关键字 fields
        fields = []
        # 传入参数 args
        args = []
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
        print("SQL: %s" % sql)


if __name__ == "__main__":
    user = User(uid=12345, name='laisent', email='laisent@163.com', password='root')
    user.save()

