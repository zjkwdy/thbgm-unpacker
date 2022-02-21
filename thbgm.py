#!/usr/bin/env python3
from os.path import exists, getsize, splitext
from io import BufferedReader
from configparser import RawConfigParser
from argparse import ArgumentParser
import wave

T_Bgm = dict[str, int]



# 将字节数转为MB等单位
def hum_convert(value):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size



# 单首bgm的类型
class thbgm:
    # 定义见#45
    # bgm: T_Bgm
    name: str
    startTime: int
    duration: int
    loopSart: int
    loopDuration: int
    channels: int
    sample: int
    bits: int
    format: str

    def __init__(self, bgm: T_Bgm) -> None:
        self.name = bgm['name']
        self.format = splitext(self.name)[-1]
        self.duration = bgm['duration']
        self.startTime = bgm['startTime']
        self.loopSart = bgm['loopStart']
        self.loopDuration = bgm['loopDuration']
        self.channels = bgm['channels']
        self.sample = bgm['sample']
        self.bits = bgm['bits']



# thbgm.fmt处理类
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
                channles = int.from_bytes(bgm[34:36], 'little')  # 声道数
                sample = int.from_bytes(bgm[36:40], 'little')  # 采样率
                bits = int.from_bytes(bgm[46:48], 'little')  # 采样位数
                bgm = {
                    'name': fileName,
                    'duration': duration,
                    'startTime': startTime,
                    'loopStart': loopStart,
                    'loopDuration': loopDuration,
                    'channels': channles,
                    'sample': sample,
                    'bits': bits
                }
                bgmList.append(thbgm(bgm))
        self.bgmList = bgmList

    def close(self) -> None:
        self.fmt.close()



# thbgm.dat处理类
class bgmdat:

    dat: BufferedReader
    name: str

    def __init__(self, fileName='thbgm.dat') -> None:
        if not exists(fileName):
            raise FileNotFoundError(f'找不到{fileName},退出...')
        self.name = fileName
        self.dat = open(fileName, 'rb')

    def close(self) -> None:
        self.dat.close()

    def seek(self, postion: int) -> int:
        return self.dat.seek(postion, 0)

    def read(self, size) -> bytes:
        return self.dat.read(size)

# wav生成和处理类
class riff:
    # # riff header
    # RIFF_HEADER = b'\x52\x49\x46\x46'  # RIFF
    # riff_size = b'\x00\x00\x00\x00'  # 4字节的数据长度
    # WAVE = b'\x57\x41\x56\x45'

    # # fmt chunk start
    # FMT = b'\x66\x6d\x74\x20'  # fmt
    # PCM_FMT = b'\x10\x00\x00\x00'
    # COMPRESS = b'\x01\x00'
    # CHANNELS = b'\x02\x00'
    # SAMPLE = b'\x44\xac\x00\x00'  # 44100采样率
    # BYTE_RATE = b'\x10\xb1\x02\x00'
    # BLOCK_ALIGN = b'\x04\x00'
    # SAMPLE_DEPTH = b'\x10\x00'

    # # data chunk start
    # DATA_HEADER = b'\x64\x61\x74\x61'  # 'data'
    # DATA_SIZE = b'\x00\x00\x00\x00'
    # DATA = b'\x00\x00\x00\x00'

    # BYTESDATA = [
    #     RIFF_HEADER, riff_size, WAVE,  # RIFF CHUNK
    #     FMT, PCM_FMT, COMPRESS, CHANNELS, SAMPLE, BYTE_RATE, BLOCK_ALIGN, SAMPLE_DEPTH,  # FMT CHUNK
    #     DATA_HEADER, DATA_SIZE, DATA  # DATA CHUNK
    # ]

    FILE_NAME: str
    # PCM_DATA: bytes
    CHANNELS: int
    BITS: int
    SAMPLE: int
    _WAV_FILE: wave.Wave_write

    def __init__(self, fileName: str, data: bytes, channels=2, sample=44100, bits=16) -> None:
        self.FILE_NAME = fileName
        # self.PCM_DATA = data
        self.CHANNELS = channels
        self.SAMPLE = sample
        self.BITS = bits
        self._WAV_FILE = wave.open(fileName, 'wb')
        self._WAV_FILE.setnchannels(channels)
        self._WAV_FILE.setsampwidth(bits//8)
        self._WAV_FILE.setframerate(sample)
        self._WAV_FILE.writeframes(data)
        
        # duration = len(data)
        # self.DATA_SIZE = duration.to_bytes(4, 'little')
        # self.riff_size = (0x24+duration).to_bytes(4, 'little')
        # self.DATA = data
        # self.BYTESDATA[1] = self.riff_size
        # self.BYTESDATA[12] = self.DATA_SIZE
        # self.BYTESDATA[13] = self.DATA

    def write(self,bytesData: bytes) -> None:
        self._WAV_FILE.writeframes(bytesData)

    def close(self) -> None:
        self._WAV_FILE.close()
    # def getBytes(self) -> bytes:
    #     return b''.join(self.BYTESDATA)

    # def save(self, fileName: str) -> None:
        
    #     wavfile.close()
        # with open(fileName, 'wb') as fp:
        #     fp.write(self.getBytes())

class bgmcmt:
    wav: str
    name: str
    desc: str

    def __init__(self, name: str, desc: str, wav: str) -> None:
        self.name = name
        self.desc = desc
        self.wav = wav


class musiccmt:

    encoding: str
    cmtList: dict[str,bgmcmt]
    _cmt_bytes: bytes

    def __init__(self, fileName: str,encoding: str) -> None:
        if not exists(fileName):
            raise FileNotFoundError(f'找不到{fileName},退出...')
        f = open(fileName, 'rb')
        cmt_bytes = f.read()
        self._cmt_bytes = cmt_bytes
        if encoding=='auto':
            encoding = self.get_encoding(cmt_bytes)
        try:
            cmtStr = cmt_bytes.decode(encoding)
        except Exception:
            raise Exception(f'尝试使用{encoding}解码{fileName}失败，请换一种编码方式或检查输入文件是否正确，然后重试。')
        self.cmtList=self.from_str(cmtStr)
        f.close()

    @staticmethod
    def get_encoding(byt: bytes) -> str:    #自动猜测文件编码
        encodings=['shift-jis','gb2312','gb18030','gbk','utf-8'] #常见编码，欢迎补充
        for encoding in encodings:
            try:
                byt.decode(encoding)
                return encoding
            except UnicodeDecodeError:
                pass
        raise Exception('尝试自动解码musiccmt失败，请使用--encoding手动指定cmt文件编码方式。')

    @staticmethod
    def from_str(cmtStr: str) -> dict[str,bgmcmt]:
        cmtStrList = cmtStr.split('@bgm/')[1:]  # 抛弃前段注释
        tmp: dict[str,bgmcmt]={}
        for bcmt in cmtStrList:
            bgm = bcmt.splitlines()
            bgm_wav = splitext(bgm[0])[0]
            bgm_name = bgm[1]
            bgm_desc = '\n'.join(bgm[4:])
            cmt = bgmcmt(bgm_name, bgm_desc, bgm_wav)
            tmp[bgm_wav]=cmt
        return tmp

    def getCmt(self,wavName: str) -> bgmcmt:
        wavName=splitext(wavName)[0]
        return self.cmtList[wavName] if wavName in self.cmtList else bgmcmt(wavName,'',wavName)

# 继承重写配置文件类，使其支持大写。。
class myconf(RawConfigParser):
    def __init__(self, defaults=None):
        RawConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


arg_parser = ArgumentParser()
arg_parser.add_argument('-f', '--fmt', help='thbgm.fmt文件名(路径)', metavar='File')
arg_parser.add_argument('-d', '--dat', help='thbgm.dat文件名(路径)', metavar='File')
arg_parser.add_argument('-c', '--cmt', help='musiccmt.txt文件名(路径)(可选)', metavar='File')
arg_parser.add_argument('--encoding', help='指定musiccmt.txt的编码(可选)', metavar='Encoding | auto')
arg_parser.add_argument('-F', '--file', help='解包指定的文件', nargs='+', metavar='File')
arg_parser.add_argument('-L', '--loop', help='指定循环部分循环次数（WAV模式）', type=int, metavar='Number')
arg_parser.add_argument('-l', '--ls', help='列出fmt内所有bgm', action='store_true')
arg_parser.add_argument('-W', '--wav', help='解包wav', action='store_true')
arg_parser.add_argument('-I', '--ini', help='生成BgmForAll.ini', action='store_true')

# 狗屎代码要来力！
args = arg_parser.parse_args()
fmtName = args.fmt if args.fmt else 'thbgm.fmt'
datName = args.dat if args.dat else 'thbgm.dat'
cmtMode = True if args.cmt else False
if cmtMode: cmtName=args.cmt
cmt_encoding = args.encoding if args.encoding else 'auto'
lsMode = True if args.ls else False
iniMode = True if args.ini else False
wavMode = True if args.wav else False
loopMode = True if args.loop else False
fileMode = True if args.file else False

print('THBGM-UNPacker v1.05.5')
print('Copyright © 2022 zjkwdy. All rights reserved.')
print()
# 打开bgm.fmt,初始化
fmt = thfmt(fmtName)
# 打开bgm.dat,初始化
dat = bgmdat(datName)
# 打开musiccmt文件，初始化
if cmtMode: cmt = musiccmt(cmtName,cmt_encoding)

if iniMode:
    # 初始化ini
    config = myconf()
    # 铁打的原作参数
    config.add_section('THBGM')
    # thbgm.dat文件位置
    config.set('THBGM', 'PATH', dat.name)
    # 采样率，正作祖传44100
    config.set('THBGM', 'SAMPLE', '44100')
    # 双声道
    config.set('THBGM', 'CHANNEL', '2')
    # 16bit位宽
    config.set('THBGM', 'BIT', '16')
    iniFile = open('BgmForAll.ini', 'w+',encoding='gbk',errors='ignore')
    # 写入死参数
    config.write(iniFile)

if lsMode:
    total = fmt.bgmList[0].startTime # 总量初始值为第一首bgm的起始点
    title='Title'.center(60, '-') if cmtMode else ''
    print(
        'Name'.center(15, '-')+
        title+
        'Size'.center(10, '-')+
        'Offset'.center(13, '-')
    )
for bgm in fmt.bgmList:
    if fileMode and (bgm.name not in args.file):
        continue
    name=cmt.getCmt(bgm.name).name.encode('utf-8').decode() if cmtMode else bgm.name
    if lsMode:
        title=cmt.getCmt(bgm.name).name.ljust(50) if cmtMode else ''
        print(
            bgm.name.ljust(15)+
            title+
            str(hum_convert(bgm.loopDuration)).ljust(10)+
            hex(bgm.startTime).upper().ljust(10).replace('0X', '0x')
        )
        total += bgm.loopDuration
    if wavMode:
        if not lsMode:
            print(name) # 如果还用了-l开关就不重复显示
        dat.seek(bgm.startTime) # 指针移动到bgm起始点
        byte = dat.read(bgm.loopDuration) # 读入整首bgm
        wav = riff(name+bgm.format, byte, bgm.channels, bgm.sample, bgm.bits)
        if loopMode and args.loop > 1:
            loopNum = args.loop-1
            dat.seek(bgm.startTime+bgm.loopSart)  # 指针移动到循环开始
            loopBytes = dat.read(bgm.loopDuration-bgm.loopSart)  # 读入整个循环
            for _ in range(loopNum):
                wav.write(loopBytes)
        wav.close()
    if iniMode:
        if not lsMode:
            print(name)
        sT = hex(bgm.startTime)
        lS = hex(bgm.loopSart)
        x1 = hex(bgm.startTime+bgm.loopSart)
        x2 = hex(bgm.loopDuration-bgm.loopSart)
        bgm_ini = 'BGM = %s,%s,%s,%s,%s\n' % (name, sT, lS, x1, x2)
        bgm_ini = bgm_ini.upper().replace('0X', '0x')
        iniFile.write(bgm_ini)

if lsMode:
    print(''.center(38+60 if cmtMode else 38, '-'))
    print(f'Total: {hum_convert(total)}, {hum_convert(getsize(dat.name)-total)} Not Used.')
if dat.dat.tell() > 0:
    print(f'Process {hum_convert(dat.dat.tell())}, {hum_convert(getsize(dat.name)-dat.dat.tell())} Remaining.')

# 经典无用代码
fmt.close()
dat.close()
if iniMode:
    iniFile.close()
