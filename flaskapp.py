# -*- coding: utf-8 -*-

from chkfile import Book
from flask import Flask
import search
from flask import render_template
from flask import request

app = Flask('name')

@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/hello-j')
def japanese():
    return render_template('japanese.html')

@app.route('/search', methods=['GET'])
def searchBook():
    bookName = request.args.get('book')
    author = request.args.get('author')
    if bookName != 'book' and author != 'author':
        bookFromName = search.searchName(BOOKS, bookName)
        bookFromAuthor = search.searchWriter(bookFromName, author)
        bookResult = list()
        for each in bookFromAuthor:
            book = bookFromAuthor[each]
            bookResult.append(book)
        return render_template('result.html', books = bookResult, bookname = bookName, author = author)
    elif bookName == 'book' and author != 'author':
        bookFromAuthor = search.searchWriter(BOOKS, author)
        bookResult = list()
        for each in bookFromAuthor:
            book = bookFromAuthor[each]
            bookResult.append(book)
        return render_template('result.html', books = bookResult, bookname = '*', author = author)
    elif bookName != 'book' and author == 'author':
        bookFromName = search.searchName(BOOKS, bookName)
        bookResult = list()
        for each in bookFromName:
            book = bookFromName[each]
            bookResult.append(book)
        return render_template('result.html', books = bookResult, bookname = bookName, author = '*')

@app.route('/fromID', methods=['GET'])
def fromID():
    number = request.args.get('number')
    if len(number) < 6:
        number = '0' * (6-len(number)) + number
    book = BOOKS[number]
    return render_template('book.html', book = book, title = book.writer+' '+book.name)

@app.route('/fromURL', methods=['GET'])
def fromURL():
    bookCard = request.args.get('url')
    if 'http://www.aozora.gr.jp/cards/' in bookCard:
        number = bookCard.split('/')[-1].replace('card', '').replace('.html', '')
        if len(number) < 6:
            number = '0' * (6-len(number)) + number
        book = BOOKS[number]
        return render_template('book.html', book = book, title = book.writer+' '+book.name)
    else:
        return "请检查您输入的url是否正确，必须输入青空文库图书卡的url"

@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == '__main__':
    import pickle
    with open('books.pkl', 'rb') as pklfile:
        BOOKS = pickle.load(pklfile)
    app.run()
