# THBGM-UNPack


![license](https://img.shields.io/github/license/zjkwdy/thbgm-unpack)    ![pyver](https://img.shields.io/badge/python-3.7+-green)


一个用来提取东方正作bgm的脚本，顺便可以生成`BgmForAll.ini`。懒得测试那么多了，目前就测试了

th07-妖妖梦、th12-星莲船、th14-辉针城

### Useage

首先使用`thtk`解压出`thbgm.fmt`，放在跟脚本同一个目录。
然后把正作文件夹内`thbgm.dat`也放到跟脚本同一个目录。

然后就可以运行这个脚本了

```shell
python3 thbgm.py -W
```

不出意外的话会生成一大堆wav。

##### 可选参数：

```
usage: thbgm.py [-h] [-f FMT] [-d DAT] [-l] [-W] [-I]

options:
  -h, --help         显示这个帮助页然后退出
  -f FMT, --fmt FMT  thbgm.fmt文件名(路径)
  -d DAT, --dat DAT  thbgm.dat文件名(路径)
  -l, --ls           列出fmt内所有bgm
  -W, --wav          解压wav
  -I, --ini          生成BgmForAll.ini
```

注释都在`thbgm.py`，自己看吧。没什么技术含量。

### FAQ:

##### 什么？你都会上github了还找不到thtk?

https://github.com/thpatch/thtk

#### 什么？你都看到这里了还不会用thtk解压thxx.dat?

```
Usage: thdat [-V] [[-c | -l | -x] 正作版本号] [dat文件 [文件名...]]
Options:
  -c  生成dat
  -l  列出dat文件内容
  -x  解压dat
  -V  显示这个帮助页然后退出
正作版本号可以是:
  1, 2, 3, 4, 5, 6, 7, 8, 9, 95, 10, 103 (for Uwabami Breakers), 105, 11, 12, 123, 125, 128, 13, 14, 143, 15, 16, 165, 17 或 18
```

例如解压妖妖梦的`th12.dat`

```shell
thdat -x 12 th12.dat
```

会解压出包括`thbgm.fmt`等一系列资源文件。
