from aifc import Error
from os.path import exists
from io import BufferedReader
from configparser import RawConfigParser


T_Bgm = dict[str, int]


class thbgm:
    # 定义见#45
    bgm: T_Bgm
    name: str
    startTime: int
    duration: int
    loopSart: int
    loopDuration: int

    def __init__(self, bgm: T_Bgm) -> None:
        self.name = bgm['name']
        self.duration = bgm['duration']
        self.startTime = bgm['startTime']
        self.loopSart = bgm['loopStart']
        self.loopDuration = bgm['loopDuration']


class thfmt:

    fmt: BufferedReader
    bgmList: list[thbgm]
    fileName: str

    def __init__(self, fmt: str = 'thbgm.fmt') -> None:
        if not exists(fmt):
            raise FileNotFoundError(f'File {fmt} Not Found,exiting..')
        self.fileName = fmt
        f = open(fmt, 'rb')
        bgmList = []
        self.fmt = f
        f.seek(0, 2)  # 指针移到末尾
        size = f.tell()
        f.seek(0)
        # 循环读取直到结束，每首52字节（十六进制编辑器数出来的，也不知道是不是字节）
        while f.tell() < size:
            bgm = f.read(52)
            if len(bgm) == 52:
                fileName = bgm[:16].replace(b'\x00', b'').decode('utf-8')
                # 文档来自网络，都要小端序排列
                startTime = int.from_bytes(bgm[16:20], 'little')  # bgm开始偏移量
                duration = int.from_bytes(
                    bgm[20:24], 'little')  # bgm时长（大——概——吧——）
                loopStart = int.from_bytes(bgm[24:28], 'little')  # 循环节开始
                loopDuration = int.from_bytes(bgm[28:32], 'little')  # 循环长度
                bgm = {
                    'name': fileName,
                    'duration': duration,
                    'startTime': startTime,
                    'loopStart': loopStart,
                    'loopDuration': loopDuration
                }
                bgmList.append(thbgm(bgm))
        self.bgmList = bgmList

    def close(self) -> None:
        self.fmt.close()

# 继承重写配置文件类，使其支持大写。。


class myconf(RawConfigParser):
    def __init__(self, defaults=None):
        RawConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


config = myconf()
# 铁打的原作参数
config.add_section('THBGM')
# thbgm.dat文件位置
config.set('THBGM', 'PATH', 'thbgm.dat')
# 采样率，正作祖传44100
config.set('THBGM', 'SAMPLE', '44100')
# 双声道
config.set('THBGM', 'CHANNEL', '2')
# 16bit位宽
config.set('THBGM', 'BIT', '16')

# 打开bgm.fmt,初始化
fmt = thfmt('thbgm.fmt')
with open('BgmForAll.ini', 'w+') as ini:
    # 写入死参数
    config.write(ini)
    for bgm in fmt.bgmList:
        nE = bgm.name
        sT = hex(bgm.startTime)
        lS = hex(bgm.loopSart)
        x1 = hex(bgm.startTime+bgm.loopSart)
        x2 = hex(bgm.loopDuration-bgm.loopSart)
        bgm = 'BGM = %s,%s,%s,%s,%s\n' % (nE, sT, lS, x1, x2)

        bgm = bgm.upper().replace('0X', '0x')
        print(bgm)
        ini.write(bgm)

# 经典无用代码
fmt.close()
