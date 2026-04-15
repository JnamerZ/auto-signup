# 自动签到脚本

## 使用说明

### Linux

可以使用以下指令，在当前目录下创建一个`password.txt`的文件，里面一行，是你账号的密码：

```bash
echo -n '密码' > password.txt
chmod 600 password.txt
```

运行以下指令可以完成一次签到：

```bash
python3 main.py -u 学号 -p $(cat password.txt)
```

如果你不希望产生任何输出，可以加上`--no-output`：

```bash
python3 main.py -u 学号 -p $(cat ./password.txt) --no-output
```

可以用`crontab`等方法定时运行脚本。

### Windows

建议自行研究。
