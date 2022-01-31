# THBGM

一个用来提取东方正作bgm的脚本，顺便可以生成`BgmForAll.ini`。懒得测试那么多了，目前就测试了

th07-妖妖梦、th12-星莲船、th14-辉针城

### Useage

首先使用`thtk`解压出`thbgm.fmt`，放在跟脚本同一个目录。
然后把正作文件夹内`thbgm.dat`也放到跟脚本同一个目录。

然后就可以运行这个脚本了```python3 thbgm.py```

不出意外的话会生成一大堆wav和一个`BgmForAll.ini`。

##### 可选参数：

```
usage: thbgm.py [-h] [-f FMT] [-d DAT]

options:
  -h, --help         show this help message and exit
  -f FMT, --fmt FMT  fmt文件名
  -d DAT, --dat DAT  dat文件名
```

注释都在`thbgm.py`，自己看吧。没什么技术含量。