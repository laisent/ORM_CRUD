-----Copyright-----


使用用法：

    实例化一个对象 
        例如:user = User(uid=12345, name='laisent', email='laisent@163.com', password='root')
        1.Create    调用实例化对象.save() 将实例化对象中的属性保存到数据表中
        2.Retrieve  调用实例化对象.find() 读取数据表里的所有数据
        3.Update    调用实例化对象.update((更改的列名的元组,), (修改成的目标的元组,), 主键id)     例如user.update(("username", "password"), ("root", "1234"), 12345)
        4.Delete    调用实例化对象.delete(主键id)    例如user.delete(12345)

author:laisent

date:2019-10-16:20::53

version:V1.0