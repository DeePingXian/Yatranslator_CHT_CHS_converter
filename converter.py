import os
import msvcrt
import json
import multiprocessing
from alive_progress import alive_bar
from alive_progress.animations import scrolling_spinner_factory
from opencc import OpenCC

with open('strings.json' , 'r' , encoding = 'utf8') as json_file:
    json_data = json.load(json_file)
with open('settings.json' , 'r' , encoding = 'utf8') as language:
    language = json.load(language)
language = language['defaultLanguage']

def converter(line , mode , lineNum , lineQueue):
    try:
        lineQueue.put((lineNum , line.split('\t')[0]+'\t'+OpenCC(mode).convert(line.split('\t')[1]) , False))
    except:
        lineQueue.put((lineNum , line , True))
    return 0

def writer(file , lineQueue , lineSum , fileNum , fileSum):
    #lineDict = {第幾行int:(文字str,是否出錯bool)}      用字典讓各行輸出的順序維持原檔案的樣子，不會被並行處理打亂
    lineDict = {}
    lineNum = 1
    lineReceived = 0
    spinner = scrolling_spinner_factory(json_data[language]['convertedLines'], length=20 , background='-', right=True, hide=True, wrap=True, overlay=False)        #自訂進度條動畫
    with open(file , 'a' , encoding='UTF-8') as output_text_file:
        with alive_bar(lineSum , title=f'{json_data[language]["file"]}{fileNum}/{fileSum}' , spinner=spinner , bar='smooth') as bar:
            while True:
                if lineReceived < lineSum:
                    line = lineQueue.get()
                    lineReceived += 1
                while lineNum in lineDict:
                    output_text_file.write(lineDict[lineNum][0])
                    output_text_file.flush()
                    if lineDict[lineNum][1] == True:
                        if lineDict[lineNum][0] != '\n':
                            print('\t'+json_data[language]['convertErrorFormer']+'「'+lineDict[lineNum][0].rstrip('\n')+'」，'+json_data[language]['convertErrorLatter'])
                    del lineDict[lineNum]
                    lineNum += 1
                if line[0] == lineNum:
                    output_text_file.write(line[1])
                    output_text_file.flush()
                    if line[2] == True:
                        if line[1] != '\n':
                            print('\t'+json_data[language]['convertErrorFormer']+'「'+line[1].rstrip('\n')+'」，'+json_data[language]['convertErrorLatter'])
                    lineNum += 1
                    bar()
                elif line[0] > 0 and lineNum <= lineSum:
                    lineDict[line[0]] = (line[1] , line[2])
                    bar()
                else:
                    return 0

if __name__ == '__main__':
    CPUThreads = multiprocessing.cpu_count()        #一開始先抓CPU執行緒數，之後就不用再抓
    if CPUThreads < 2:
        CPUThreads = 2
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
            mode = 's2twp'
        elif mode == '2':
            mode = 'tw2sp'
        elif mode == '3':
            mode = 's2t'
        else:
            mode = 't2s'
        targetFolder = 'after'      #決定after資料夾編號
        if targetFolder in os.listdir():
            targetFolder = 'after_2'
        while targetFolder in os.listdir():
            targetFolder = f'after_{int((targetFolder.partition("_"))[2])+1}'

        print()     #換行
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
                            if lineSum <= 50:
                                spinner = scrolling_spinner_factory(json_data[language]['convertedLines'], length=20 , background='-', right=True, hide=True, wrap=True, overlay=False)        #自訂進度條動畫
                                with alive_bar(lineSum , title=f'{json_data[language]["file"]}{fileNum}/{fileSum}' , spinner=spinner , bar='smooth') as bar:
                                    for line in input_text_file:
                                        with open(targetFolder+((dirs+'\\'+file).lstrip('before')) , 'a' , encoding='UTF-8') as output_text_file:
                                            try:
                                                output_text_file.write((line.split('\t'))[0]+'\t'+OpenCC(mode).convert(line.split('\t')[1]))
                                                output_text_file.flush()
                                            except:
                                                output_text_file.write(line)
                                                output_text_file.flush()
                                                if line != '\n':
                                                    print('\t'+json_data[language]['convertErrorFormer']+'「'+line.rstrip('\n')+'」，'+json_data[language]['convertErrorLatter'])
                                        bar()
                            else:
                                lineNum = 1
                                lineQueue = multiprocessing.Manager().Queue()
                                taskPool = multiprocessing.Pool(processes = CPUThreads)
                                taskList = []
                                writer_ = taskPool.apply_async(writer , (targetFolder+((dirs+'\\'+file).lstrip('before')) , lineQueue , lineSum , fileNum , fileSum))
                                for line in input_text_file:
                                    task = taskPool.apply_async(converter , (line , mode , lineNum , lineQueue))
                                    taskList.append(task)
                                    lineNum += 1
                                for task in taskList:
                                    task.get()
                                writer_.get()
                                taskPool.close()
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