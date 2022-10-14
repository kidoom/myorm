# ORM思想和框架实现

## 一》ORM思想

[ORM](https://so.csdn.net/so/search?q=ORM&spm=1001.2101.3001.7020)全称“Object Relational Mapping”，即对象-关系映射，就是把关系数据库的一行映射为一个对象，也就是一个类对应一个表，这样，写代码更简单，不用直接操作SQL语句。在**面向对象编程思想下的语言**涉及的核心概念就是**对象、类和属性**。我们回头再看关系数据库，它操作的是对象吗？它能否直接存储对象到数据库或者从数据库直接获取对象？显然不能，如果可以那就不叫关系数据库，而应该叫对象数据库。我们可以说，在关系数据库的世界里，万物皆关系，玩的就是二维表，涉及的核心概念是**表、记录和字段**。

**ORM 作用是为对象与关系数据库之间搭建桥梁，以解决对象与关系数据库之间不协调的问题。**

\#**什么是O，R，M？**

**O(对象模型)**：实体对象，即我们在程序中根据数据库表结构建立的一个个实体Entity。 

------

**R(关系型数据库的数据结构)**：即我们建立的数据库表。

------

**M(映射)**：从R（数据库）到O（对象模型）的映射，可通过XML文件映射。

**O and R**  :两个层面   中间的桥梁  **Map映射**

**[对象关系映射**]https://www.361shipin.com/blog/1523722783631081472



## 一》前置知识

[元类mataclass：作为python中非常强大的功能，但也要谨慎使用](https://www.liaoxuefeng.com/wiki/1016959663602400/1017592449371072)

[深入理解 Python 中的元类 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/269012792)

**mataclass 是用来解决继承没有办法解决的问题**

*我们需要牢记的一点是*  **Python中所有的东西，注意，我是指所有的东西——都是对象。这包括整数、字符串、函数以及类。它们全部都是对象，而且它们都是从一个类创建而来。这个类就是type 而这个type就可以理解为是一个元类**

```python
>>> a = 1
>>> b = 'hello'
>>> a.__class__
<type 'int'>
>>> b.__class__
<type 'str'>

>>> a.__class__.__class__
<type 'type'>
>>> b.__class__.__class__ 
<type 'type'>
```

**元类(type)就是类的类**

**mataclass本身就是为更灵活的掌握建立类中间的这个逻辑** *当继承无法解决的时候，就可以尝试要去用元类来解决*

```python
    print(h.__class__)  # h 是一个hello类
    print(h.__base__)  # h是一个实例，不是类
    print(type(hello))  # <class 'type'> hello 是types生成的一个拥有可以创建对象功能的对象object（类）
    print(type(h))  # <class '__main__.hello'> h是hello这个类实例化的对象

    

# 我们说class的定义是运行时动态创建的，而创建class的方法就是使用type()函数。，利用type来创建一个class对象 注意是对象 但是这个对象具有实例化的功能 那么这不就是类吗？

# 通过type()函数创建的类和直接写class是完全一样的，因为Python解释器遇到class定义时，仅仅是扫描一下class定义的语法，然后调用type()函数创建出class。
```



[Python 元类详解 __new__、__init__、__call__、__metacalss__ - 简书 (jianshu.com)](https://www.jianshu.com/p/2e2ee316cfd0)

*元类是为了修改类的创建逻辑  修改类的创建逻辑是为自定义实例*   我不太确定

**python class的机制 python是如何创建类的？**：

**我们能用元类做什么？**：

*它可以对类内部的定义（包括类属性和类方法）进行动态的修改。可以这么说，使用元类的主要目的就是为了实现在创建类时，能够动态地改变类中定义的属性或者方法。*

```python
#定义一个元类
class FirstMetaClass(type):
    # cls代表动态修改的类
    # name代表动态修改的类名
    # bases代表被动态修改的类的所有父类
    # attr代表被动态修改的类的所有属性、方法组成的字典
    def __new__(cls, name, bases, attrs):
        # 动态为该类添加一个name属性
        attrs['name'] = "kidoom"
        attrs['say'] = lambda self: print("hello world") #这里引用了一个匿名函数
        return super().__new__(cls, name, bases, attrs)

    # 必须显式继承自
    # type
    # 类；
    # 类中需要定义并实现
    # __new__()
    # 方法，该方法一定要返回该类的一个实例对象，因为在使用元类创建类时，该
    # __new__()
    # 方法会自动被执行，用来修改新建的类。

class Language(object,metaclass=FirstMetaClass):
    pass

lang = Language() #实例化一个对象


if __name__ == "__main__":
    print(lang.name) # 我们自定义的给Language类的所有实例化对象添加了一个name属性，还有个一个say()函数
    lang.say()
    
    
    
>>> kidoom
>>> hello world
```

## 一》编写orm框架（python实现）

**我们来看一下在flask的sqlachemy中我们是怎样使用orm框架**：

```python
from exts import db

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)
# 我们定义了这样一个类  可以以输入id等等我们需要写的字段
# colum  后面是属性描述符 通过定义属性描述符 来实现对字段的限制

#以表单输入添加为例：
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():  # 如果表单验证成功 则重定向进入登陆页面
            email = form.email.data
            username = form.username.data
            password = form.password.data

            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)  # 同时储存用户信息
            db.session.commit()
            return redirect(url_for("user.login"))  # 重定向url路由
        else:
            return redirect(url_for("user.register"))
   # 我们希望完成一个什么事情呢？通过属性描述符的限制，我们希望我们定义的类User的实例可以被创建qie能够通过映射被储存在数据库中  所以orm的基本机制已经浮现了 但是同时别人的框架还是有许多更加复杂的业务逻辑的。



```

**代码实现**:

```python
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
                raise ValueError("min_value must be int")
            elif min_value < 0:
                raise ValueError("min_value must be positive int")

        if max_value is not None:
            if not isinstance(max_value, numbers.Integral):
                raise ValueError("max_value must be int")
            elif max_value < 0:
                raise ValueError("max_value must be positive int")

        if min_value and max_value is not None:
            if min_value > max_value:
                raise ValueError("min_value must be smaller than max_value")

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError("int value need")
        if value < self.min_value or value > self.max_value:
            raise ValueError("value must between min_value and max_value")

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
            raise ValueError("String value need")
        if len(value) > self.max_length:
            return ValueError("value length excess len of max_length")

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
                db_table = table  # 如果不是空 那我就替换掉table空值
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

```

