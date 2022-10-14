# 需求
import pymysql
import numbers

db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='dbtest1',
                     port=3306,
                     autocommit=True)

# 使用cursor()方法获取操作游标
cursor = db.cursor()





class Field:
    pass


class IntField(Field):
    # 数据描述符
    def __init__(self, db_colum, min_value=None, max_value=None):
        self._value = None
        self.min_value = min_value
        self.max_value = max_value
        self.db_colum = db_colum
        if min_value is not None:
            if not isinstance(min_value, numbers.Integral):
                raise ValueError("最小值必须是int")
            elif min_value < 0:
                raise ValueError("最小值不能为负数")

        if max_value is not None:
            if not isinstance(max_value, numbers.Integral):
                raise ValueError("最大值必须为int")
            elif max_value < 0:
                raise ValueError("最大值必须为正数")

        if min_value and max_value is not None:
            if min_value > max_value:
                raise ValueError("最小值必须要大于最大值")

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError("需要int型数据")
        if value < self.min_value or value > self.max_value:
            raise ValueError("必须在最大值和最小值之间")

        self.value = value


class CharField(Field):
    def __init__(self, db_colum, max_length=None):
        self._value = None
        self.db_colum = db_colum
        self.max_length = max_length

    def __get__(self, instance, owner):
        return self.value  # 返回一个实例

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("应为string类型")
        if len(value) > self.max_length:
            return ValueError("数据长度超过最大长度")

        self.value = value


# 元创建元类来拦截初始类的创建
class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        if name == "BaseModel":
            return super().__new__(cls, name, bases, attrs, **kwargs)
        fields = {}  # 让fields记录所有数据表相关的列
        for key, value in attrs.items():  # 创建field类型
            if isinstance(value, Field):
                fields[key] = value  # value赋值给fields
        attrs_meta = attrs.get("Meta", None)
        _meta = {}
        db_table = name.lower()
        if attrs_meta is not None:
            table = getattr(attrs_meta, "db_table", None)
            if table is not None:
                db_table = table  # 如果不是空 那就替换掉table空值
        _meta["db_table"] = db_table  # db_table 来储存表名
        attrs["_meta"] = _meta
        attrs["fields"] = fields
        return super().__new__(cls, name, bases, attrs, **kwargs)


class BaseModel(metaclass=ModelMetaClass):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return super().__init__()

    def save(self):
        fields = []
        values = []
        for key, value in self.fields.items():
            db_colum = value.db_colum
            if db_colum is None:
                db_colum = key.lower()
            fields.append(db_colum)
            value = getattr(self, key)
            values.append(str(value))
        sql_save = """INSERT INTO {db_table}({fields}) VALUES({values})""".format(db_table=self._meta["db_table"],
                                                                                  fields=",".join(fields),
                                                                                  values=",".join(values))
        try:
            # 执行sql语句
            cursor.execute(sql_save)
            # 提交到数据库执行
            db.commit()
            print("执行成功")
        except:
            # 如果发生错误则回滚
            db.rollback()
            print("执行失败")
        pass


if __name__ == "__main__":
    class User(BaseModel):
        name = CharField(db_colum="name", max_length=100)
        age = IntField(db_colum="age", min_value=1, max_value=100)


    user = User(name="'lzh'", age=19)
    user.save()
