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
            raise FileNotFoundError(f'找不到{fmt}，退出...')
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
                duration = int.from_bytes(bgm[20:24], 'little')  # bgm时长
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


class bgmdat:

    dat: BufferedReader

    def __init__(self, fileName='thbgm.dat') -> None:
        if not exists(fileName):
            raise FileNotFoundError(f'找不到{fileName},退出...')
        self.dat = open(fileName, 'rb')

    def close(self) -> None:
        self.dat.close()

    def seek(self, postion: int) -> int:
        return self.dat.seek(postion,0)

    def read(self, size) -> bytes:
        return self.dat.read(size)


class riff:
    # riff header
    RIFF_HEADER = b'\x52\x49\x46\x46'  # RIFF
    riff_size = b'\x00\x00\x00\x00'  # 4字节的数据长度
    WAVE = b'\x57\x41\x56\x45'

    # fmt chunk start
    FMT = b'\x66\x6d\x74\x20'  # fmt
    PCM_FMT = b'\x10\x00\x00\x00'
    COMPRESS = b'\x01\x00'
    CHANNELS = b'\x02\x00'
    SAMPLE = b'\x44\xac\x00\x00'  # 44100采样率
    BYTE_RATE = b'\x10\xb1\x02\x00'
    BLOCK_ALIGN = b'\x04\x00'
    SAMPLE_DEPTH = b'\x10\x00'

    # data chunk start
    DATA_HEADER = b'\x64\x61\x74\x61'  # 'data'
    DATA_SIZE = b'\x00\x00\x00\x00'
    DATA = b'\x00\x00\x00\x00'

    BYTESDATA = [
        RIFF_HEADER, riff_size, WAVE,  # RIFF CHUNK
        FMT, PCM_FMT, COMPRESS, CHANNELS, SAMPLE, BYTE_RATE, BLOCK_ALIGN, SAMPLE_DEPTH,  # FMT CHUNK
        DATA_HEADER, DATA_SIZE, DATA  # DATA CHUNK
    ]

    def __init__(self, data: bytes) -> None:
        duration = len(data)
        self.DATA_SIZE = duration.to_bytes(4, 'little')
        self.riff_size = (0x24+duration).to_bytes(4, 'little')
        self.DATA = data
        self.BYTESDATA[1] = self.riff_size
        self.BYTESDATA[12] = self.DATA_SIZE
        self.BYTESDATA[13] = self.DATA

    def getBytes(self) -> bytes:
        return b''.join(self.BYTESDATA)

    def save(self, fileName: str) -> None:
        with open(fileName, 'wb') as fp:
            fp.write(self.getBytes())


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
dat = bgmdat('thbgm.dat')
with open('BgmForAll.ini', 'w+') as ini:
    # 写入死参数
    config.write(ini)
    for bgm in fmt.bgmList:
        nE = bgm.name
        sT = hex(bgm.startTime)
        lS = hex(bgm.loopSart)
        x1 = hex(bgm.startTime+bgm.loopSart)
        x2 = hex(bgm.loopDuration-bgm.loopSart)
        print(nE)
        dat.seek(bgm.startTime)
        byte=dat.read(bgm.loopDuration)
        wav=riff(byte)
        wav.save(nE)
        bgm = 'BGM = %s,%s,%s,%s,%s\n' % (nE, sT, lS, x1, x2)

        bgm = bgm.upper().replace('0X', '0x')
        # print(bgm)

        ini.write(bgm)

# 经典无用代码
fmt.close()
