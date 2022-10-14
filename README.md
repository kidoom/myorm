**写在前面**

**功能实现：**

**可以自定义表，需要自己先创建表**

```python
#例子：
 class User(BaseModel):
        name = CharField(db_colum="name", max_length=100)
        age = IntField(db_colum="age", min_value=1, max_value=100)
        
#定义类必须继承BaseModel类
#CharField 实现字符串列属性  内置 max_length 限制最大长度
#IntField  实现整型列属性    内置  min_value max_value 实现范围控制

#赋值操作
xxx = User(name=,age=)

#添加
xxx.save()
```
[ORM介绍](https://github.com/kidoom/myorm/blob/main/orm%E4%BB%8B%E7%BB%8D)
[实现思路](https://github.com/kidoom/myorm/blob/main/%E5%AE%9E%E7%8E%B0%E6%B5%81%E7%A8%8B)
