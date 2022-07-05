import os
import msvcrt
from alive_progress import alive_bar
from alive_progress.animations import scrolling_spinner_factory
from opencc import OpenCC
print('本程式基於OpenCC開放中文轉換 v1.1.1 https://github.com/BYVoid/OpenCC\n請將要轉換的文本置於「before」資料夾下（沒有就創建一個），可包含資料夾，但不支援zip，請先解壓縮\n轉換完成的文本會存於「after」資料夾，若有同名資料夾則存於往後編號的資料夾\n')
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
targetFolder = 'after'      #決定after資料夾編號
if targetFolder in os.listdir():
    targetFolder = 'after_2'
while targetFolder in os.listdir():
    targetFolder = f'after_{int((targetFolder.partition("_"))[2])+1}'
print()     #換行
spinner = scrolling_spinner_factory('轉換行數', length=20 , background='-', right=True, hide=True, wrap=True, overlay=False)        #自訂進度條動畫
fileSum = 0
for dirs , subdirs , files in os.walk('before' , topdown=True):
    if files:
        for file in files:
            if file.endswith('.txt'):
                fileSum += 1       #數檔案總數
fileNum = 0
for dirs , subdirs , files in os.walk('before' , topdown=True):
    if not os.path.isdir(targetFolder+dirs.lstrip('before')):
        os.makedirs(targetFolder+dirs.lstrip('before'))     #產生目標資料夾
    for file in files:
        if file.endswith('.txt'):
            fileNum += 1
            print('目前檔案：'+(dirs+'\\'+file).lstrip('before\\'))
            with open(dirs+'\\'+file , 'r' , encoding='UTF-8') as input_text_file:
                lineSum = list(enumerate(open(dirs+'\\'+file , 'r' , encoding='UTF-8') , start=1))[-1][0]       #數此txt檔的行數
                with alive_bar(lineSum , title=f'檔案{fileNum}/{fileSum}' , spinner=spinner , bar='smooth') as bar:
                    for line in input_text_file:
                        with open(targetFolder+((dirs+'\\'+file).lstrip('before')) , 'a' , encoding='UTF-8') as output_text_file:
                            try:
                                output_text_file.write((line.partition('\t'))[0]+'\t'+OpenCC(mode).convert(line.partition('\t')[2]))
                            except:
                                output_text_file.write(line)
                                print('\t轉換錯誤「'+line+'」，將直接整段複製不轉換')
                        bar()
        else:
            print('非txt檔，跳過：'+(dirs+'\\'+file).lstrip('before\\'))
print('轉換完成 請按任意鍵退出...')
while True:
    if msvcrt.getch():
        break