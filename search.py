import pickle
from chkfile import Book

with open('books.pkl', 'rb') as pklfile:
    books = pickle.load(pklfile)

def searchID(books, id):
    if id in books:
        return [books[id]]
    else:
        return []

def searchName(books, name):
    result = {}
    for id in books:
        book = books[id]
        if name in book.name or name in book.name_accent:
            result[id] = book
    return result

def searchWriter(books, writer):
    result = {}
    for id in books:
        book = books[id]
        if writer in book.writer:
            result[id] = book
    return result
