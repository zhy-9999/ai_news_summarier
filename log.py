import datetime
LOG_FILE = 'log.txt'
def make_log(level:int,info:str)->str: # err0 warn1 log2
    write_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_level = ['Error','Warn','Log'][level]
    write_info = info
    write = f'[{write_level}][{write_time}]{write_info}\n'
    return write
def write_log(write:str)->int:
    try:
        with open(LOG_FILE,'a',encoding='utf-8') as f: # 追加模式默认创建不存在文件
            f.write(write)
    except Exception as e:
        print(make_log(1,f'Failed logging:{e}\n\t{write}'))
        return 1
    else:
        return 0
def read_log(*lines:int)->dict:
    text = []
    try:
        with open(LOG_FILE,'r',encoding='utf-8') as f:
            text = list(f)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(make_log(1,f'Failed reading:{e}\n'))
        raise
    output = {}
    if lines:
        for i in lines:
            try:
                output[i] = text[i].strip() # just 0-based im mean
            except IndexError:
                output[i] = ''
    else:
        for i in range(len(text)):
            output[i] = text[i]
    return output
def log(level:int,info:str)->int:
    return write_log(make_log(level,info))
if __name__ == '__main__':
    log(2,'test:opening')
    log(0,'test:cannot open')
    log(1,'test:change way')
    log(0,'test:cannot open again')
    log(1,'test:change a dangerous way')
    log(2,'test:opened')
    log(1,'test:theres danger')
    print(read_log(-1,-2,-3,-4,-5))
    print(read_log())
