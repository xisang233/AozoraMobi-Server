import config
import zipfile
import pickle
import csv
import os
import shutil
import time

t0 = time.time()
# 记录初始时间

def GetCsvFile(origin = False):
# 返回CSV文件的名称，若origin为True则从网络获取CSV文件
    def GetZipFile(origin):
        # 获取存有CSV文件的ZIP压缩包的**所在地址**，若origin为True则从本地的clone中获取zip文件，否则使用本文件夹的zip文件
        if origin:
            print ('正在从 %s 获取包含csv文件的zip包' %config.CSV_PATH)
            shutil.copy(config.CSV_PATH, '.')
            zipFileName = os.path.basename(config.CSV_PATH)
            return zipFileName
        else:
            zipFileName = os.path.basename(config.CSV_PATH)
            return zipFileName
    print('正在从zip文件中解压csv文件')
    ZipPath = GetZipFile(origin)
    ZipFile = zipfile.ZipFile(ZipPath, 'r')
    CsvFile = ZipFile.namelist()[0]
    ZipFile.extract(CsvFile)
    print('已成功解压csv文件')
    return CsvFile


def checkfile(Books):
    print('经搜索，以下文件没有对应的mobi和epub文件')
    count = 0
    for BookID in Books:
        book = Books[BookID]
        if not(book.epubflag and book.mobiflag) and 'http://www.aozora.gr.jp' in book.address:
            count += 1
            shutil.copy(config.WEBLOCAL + book.source, 'zipNotFound')
            print('Num.%d\t' %count, book.name, book.zipfile, book.epubflag, book.mobiflag)
    print('搜索完毕，共发现%d个未转换的文件' %count)
    print('已将它们自动移动到zipNotFound目录下，请手动转换')

def checkfile2(Books):
    for BookID in Books:
        book = Books[BookID]


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



def filte(dicBooks):
    # 传入原书籍字典，处理后分成正常/著作权存续/文件不全 三种情况
    print('正在过滤书籍文件，共需要过滤%d本书籍' %len(dicBooks))
    books = {}
    copyright = {}
    nofile = {}
    for id in dicBooks:
        book = dicBooks[id]
        if book.copyflag is False:
            copyright[id] = book
        elif book.epubflag is False or book.mobiflag is False:
            nofile[id] = book
        else:
            books[id] = book
    print('过滤完成，共有%d本正常，%d本著作权未到期，%d本文件不存在' %(len(books), len(copyright), len(nofile)))
    print('正在删除著作权未到期的书籍')
    delete(copyright)
    print('正在删除文件不全的书籍')
    delete(nofile)
    return books

def delete(dicbooks):
    # 传入不正常的书籍字典，将它们指向的书籍文件删除
    for id in dicbooks:
        book = dicbooks[id]
        if book.epubfile is not None:
            os.remove(config.EPUBPATH + '\\' + book.epubfile)
        if book.mobifile is not None:
            os.remove(config.MOBIPATH + '\\' + book.mobifile)
    print('共删除%d个文件' %(len(dicbooks)))

if __name__ == '__main__':
    # 详细说明见 https://github.com/aozorahack/hackathon2016/blob/master/doc/csv.md
    CsvFile_Name = GetCsvFile(origin = True)
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
            if 'http://www.aozora.gr.jp' not in book.address:
                continue
            Books[id] = book
        print('成功读取csv信息，正在关闭csv文件')

    checkfile(Books)

    Books = filte(Books)
    print('删除完毕，正在第二次确认')
    checkfile2(Books)
    print('文件查找完成，正在将结果写入')
    with open('books.pkl', 'wb') as pklfile:
        pickle.dump(Books, pklfile)
    print('文件写入完成，共用时%f秒' %(time.time() - t0))
