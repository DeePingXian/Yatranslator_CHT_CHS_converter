import os
import shutil
from opencc import OpenCC
print('本程式基於OpenCC開放中文轉換 v1.1.1 https://github.com/BYVoid/OpenCC\n請將要轉換的文本置於「before」資料夾下\n轉換完成的文本會置於「after」資料夾下 開始轉換時會自動刪除原有的「after」資料夾及其內的檔案 請記得備份\n')
mode = ''
while mode not in ('1','2','3','4'):
    mode = input('請輸入轉換模式\n1：簡轉繁 2：繁轉簡 3：簡轉繁（包含慣用語） 4：繁轉簡（包含慣用語）')
if mode == '1':
    mode = 's2t'
elif mode == '2':
    mode = 't2s'
elif mode == '3':
    mode = 's2twp'
else:
    mode = 'tw2sp'
if os.path.isdir('after'):
    shutil.rmtree('after' , ignore_errors = True)
for dirs , subdirs , files in os.walk('before' , topdown=True):
    if not os.path.isdir('after'+dirs.lstrip('before')):
        os.makedirs('after'+dirs.lstrip('before'))
    for file in files:
        print((dirs+'\\'+file).lstrip('before\\'))
        with open(dirs+'\\'+file , 'r' , encoding='UTF-8') as input_text_file:
            for line in input_text_file:
                with open((dirs+'\\'+file).replace('before\\' , 'after\\') , 'a' , encoding='UTF-8') as output_text_file:
                    try:
                        output_text_file.write((line.split('\t'))[0]+'\t'+OpenCC(mode).convert(line.split('\t')[1]))
                    except:
                        output_text_file.write(line)
print('轉換完成')