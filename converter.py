import os
import msvcrt
import json
from alive_progress import alive_bar
from alive_progress.animations import scrolling_spinner_factory
from opencc import OpenCC
from pyparsing import empty

with open('strings.json' , 'r' , encoding = 'utf8') as json_file:
    json_data = json.load(json_file)
with open('settings.json' , 'r' , encoding = 'utf8') as language:
    language = json.load(language)
language = language['defaultLanguage']

print(json_data[language]['intro']+'\n')
mode = ''
while mode not in ('1','2','3','4'):
    mode = input(json_data[language]['inputMessage']+'\n')
    if mode == '5':
        if language == 'CHT':
            language = 'CHS'
            with open('settings.json' , 'w' , encoding = 'utf8') as f:
                json.dump({'defaultLanguage': 'CHS'}, f, ensure_ascii=False)
        elif language == 'CHS':
            language = 'CHT'
            with open('settings.json' , 'w' , encoding = 'utf8') as f:
                json.dump({'defaultLanguage': 'CHT'}, f, ensure_ascii=False)

if 'before' in os.listdir():
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
    spinner = scrolling_spinner_factory(json_data[language]['convertedLines'], length=20 , background='-', right=True, hide=True, wrap=True, overlay=False)        #自訂進度條動畫
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
                isEmptyFile = False
                with open(dirs+'\\'+file , 'r' , encoding='UTF-8') as input_text_file_:
                    if input_text_file_.readlines() == []:
                        isEmptyFile = True
                with open(dirs+'\\'+file , 'r' , encoding='UTF-8') as input_text_file:
                    if not isEmptyFile:
                        print('目前'+json_data[language]['file']+'：'+(dirs+'\\'+file).lstrip('before\\'))
                        lineSum = list(enumerate(open(dirs+'\\'+file , 'r' , encoding='UTF-8') , start=1))[-1][0]       #數此txt檔的行數
                        with alive_bar(lineSum , title=f'{json_data[language]["file"]}{fileNum}/{fileSum}' , spinner=spinner , bar='smooth') as bar:
                            for line in input_text_file:
                                with open(targetFolder+((dirs+'\\'+file).lstrip('before')) , 'a' , encoding='UTF-8') as output_text_file:
                                    try:
                                        output_text_file.write((line.split('\t'))[0]+'\t'+OpenCC(mode).convert(line.split('\t')[1]))
                                    except:
                                        output_text_file.write(line)
                                        print('\t'+json_data[language]['convertErrorFormer']+'「'+line.rstrip('\n')+'」，'+json_data[language]['convertErrorLatter'])
                                bar()
                    else:
                        print('「'+(dirs+'\\'+file).lstrip('before\\')+'」'+json_data[language]['emptyFile'])
                        with open(targetFolder+((dirs+'\\'+file).lstrip('before')) , 'a' , encoding='UTF-8') as output_text_file:
                            output_text_file.write('')
            else:
                print(json_data[language]['nonTxtError']+'：'+(dirs+'\\'+file).lstrip('before\\'))
    print(json_data[language]['completed'])
    while True:
        if msvcrt.getch():
            break
else:
    print(json_data[language]['nonBeforeFolderError'])
    while True:
        if msvcrt.getch():
            break