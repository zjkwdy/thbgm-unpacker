# THBGM-UNPacker


![license](https://img.shields.io/github/license/zjkwdy/thbgm-unpack)	![pyver](https://img.shields.io/badge/python-3.7+-green)    [![State-of-the-art Shitcode](https://img.shields.io/static/v1?label=State-of-the-art&message=Shitcode&color=7B5804)](https://github.com/trekhleb/state-of-the-art-shitcode)


一个用来提取东方正作bgm的脚本，顺便可以生成`BgmForAll.ini`。懒得测试那么多了，目前就测试了

th07-妖妖梦、th08-永夜抄、th10-风神录、th12-星莲船、th13-神灵庙、th14-辉针城。

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
$> ./thbgm.py -h
usage: thbgm.py [-h] [-f File] [-d File] [-F File [File ...]] [-L Number] [-l] [-W] [-I]

options:
  -h, --help            show this help message and exit
  -f File, --fmt File   thbgm.fmt文件名(路径)
  -d File, --dat File   thbgm.dat文件名(路径)
  -F File [File ...], --file File [File ...] 
  						解包指定的文件
  -L Number, --loop Number
  						指定循环部分循环次数（WAV模式）
  -l, --ls              列出fmt内所有bgm
  -W, --wav             解包wav
  -I, --ini             生成BgmForAll.ini
```

指定`thbgm.dat`和`thbgm.fmt`文件名（默认为`thbgm.dat`和`thbgm.fmt`）

```shell
./thbgm.py -f th12bgm.fmt -d th12bgm.dat -W
```

列出`thbgm.fmt`和`thbgm.dat`内的文件

```shell
./thbgm.py -l
```

只解包（解析）某一（几）首bgm:

```shell
./thbgm.py -F th12_00.wav th12_01.wav -W
```

指定循环部分循环次数：

```shell
./thbgm.py -L 3
```

多个参数可以同时使用：

```shell
./thbgm.py -f th12bgm.fmt -d th12bgm.dat -lWI -F th12_01.wav -L 3
```

执行后将会显示fmt内指示的所有bgm，并且在本目录下解包出循环部分循环3次的`th12_01.wav`，同时生成`BgmForAll.ini`。

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
