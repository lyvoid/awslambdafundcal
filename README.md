## awslambdafundcal

重写了一遍fundcal，主要用来每天拉去大盘数据，简单分析后把结果发送到自己邮箱。
这次使用了aws的lambda服务，并采用dynamodb作为数据存储，通过fabric自动打包并部署到aws上。

### dynamodb_tool
dynamodb_tool里实现了一个较为通用的对象型数据库工具。
新的Table可以参考tables.py里的定义方式。
__table__名字定义好之后，会自动的和dynamodb里的表关联好（通过metaclass）。
AssistCloumnClass用于定义一些可能需要的列，为了方便写代码的时候能有代码提示，
在生成类对象的时候，这些定义会被删除。

### local
local里是一些本地的操作，主要是对原始的数据进行预处理，并插入到dynamodb中。
需要额外安装pandas环境。


### fabfile.py
用于自动部署lambda服务，这里采用了一个中转的服务器，主要是因为本地直接传aws太慢了。
使用了aws-cli工具，先把代码和环境打成zip包上传到s3，然后从s3传到lambda服务中。

