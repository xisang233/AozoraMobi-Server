import config
import zipfile
import pickle
import csv
import os
import shutil
import time

t0 = time.time()
# 记录初始时间
class Book:
    def __init__(self, dict):
        def findMobiFile():
            zipFileName = self.zipfile
            mobiFileName = zipFileName.replace('.zip', '.mobi').replace('.txt', '.mobi')
            if mobiFileName in mobiFileList:
                return mobiFileName, True
            else:
                return None, False

        def findEpubFile():
            zipFileName = self.zipfile
            epubFileName = zipFileName.replace('.zip', '.epub').replace('.txt', '.epub')
            if epubFileName in epubFileList:
                return epubFileName, True
            else:
                return None, False
        self.id = dict['\ufeff作品ID']
        self.dict = dict
        self.name = dict['作品名']
        self.name_accent = dict['作品名読み']
        self.subhead = dict['副題']
        self.subhead_accent = dict['副題読み']
        self.oraginal_name = dict['原題']
        self.classfy = dict['分類番号']
        self.moji = dict['文字遣い種別']
        self.copyflag = dict['作品著作権フラグ'] == 'なし'
        self.writer = dict['姓'] + dict['名']
        self.address = dict['テキストファイルURL']
        self.source = self.address.replace('http://www.aozora.gr.jp', '')
        self.zipfile = self.source.split('/')[-1]
        self.transflag = False
        self.epubfile, self.epubflag = findEpubFile()
        self.mobifile, self.mobiflag = findMobiFile()
    def __str__(self):
        return self.id + '\t' + self.name + '\t' + self.subhead + '\t' + self.oraginal_name + '\t' + self.classfy + '\t' + str(
            self.moji) + '\t' + str(self.copyflag) + '\t' + self.writer

if __name__ == '__main__':
    # 详细说明见 https://github.com/aozorahack/hackathon2016/blob/master/doc/csv.md
    CsvFile_Name = 'list_person_all_extended_utf8.csv'
    booksDict = dict()

    print('正在打开csv文件')

    Books = dict()

    print('正在获取epub和mobi文件列表')
    epubFileList = os.listdir(config.EPUBPATH)
    print('共获取到%d个epub文件' %len(epubFileList))
    mobiFileList = os.listdir(config.MOBIPATH)
    print('共获取到%d个mobi文件' %len(mobiFileList))
    with open(CsvFile_Name, encoding='utf-8') as CsvFile:
        reader = list(csv.DictReader(CsvFile))
        print('成功打开csv文件，共有%d条信息，正在读取...' %len(reader))
        for line in reader:
            line = dict(line)
            id = line['\ufeff作品ID']
            book = Book(line)
            if 'http://www.aozora.gr.jp' not in book.address or book.copyflag is False or book.mobiflag is False:
                continue
            Books[id] = book
        print('成功读取csv信息，正在关闭csv文件')

    with open('books.pkl', 'wb') as pklfile:
        pickle.dump(Books, pklfile)
    print('文件写入完成，共用时%f秒' %(time.time() - t0))
