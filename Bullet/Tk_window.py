from cgitb import text
from doctest import master
import imp
from re import X
from sqlite3 import Row
from textwrap import fill
import tkinter as tk
from tkinter.tix import COLUMN  # 使用Tkinter前需要先匯入
from tkinter import *
from turtle import bgcolor, width
import Globals

Globals.initial()

# region 例項化object，建立視窗window
window = tk.Tk()
window.title('IP SETTING')
window.geometry('500x300')  # 這裡的乘是小x
serverIP = Globals.serverIP
text_IP = Label(text=serverIP, font=2, bg='#fff')
# text_IP.grid(row=2,column=1, sticky="WE") 
# text_IP.grid(row=2,column=1, sticky="WE") 
entry_IP=Entry(font=2, takefocus = True)
entry_IP.insert(0, serverIP)
entry_IP.grid(row=0,column=1, sticky="WE")
# endregion

def insert_end():   # 在文字框內容最後接著插入輸入內容
    # serverIP = entry_IP.get()
    global serverIP
    global text_IP
    entry = entry_IP.get()
    print("IP: ", entry)
    text_IP = Label(text=entry, font=2, bg='#fff')
    text_IP.grid(row=2,column=1, sticky="WE")

def IP_Reset():   # 清除輸入&確認欄位
    global serverIP
    global text_IP
    serverIP = Globals.serverIP
    entry_IP.delete(0, END)
    text_IP = Label(text='', font=2, bg='#fff')
    text_IP.grid(row=2,column=1, sticky="WE") 

def TK_connect():
    print("IP: ", serverIP)
    #輸入欄位
    label_IP=Label(text='Entry your IP: ', font=2, height=2) 
    label_IP.grid(row=0,column=0,sticky=W)
    entry_IP=Entry(font=2, takefocus=TRUE)
    entry_IP.insert(0, serverIP)
    entry_IP.grid(row=0,column=1, sticky=W)
    #設定IP按鈕
    setBtn=Button(text="設置", font=2, command=insert_end) 
    setBtn.grid(row=0,column=3)
    #重設按鈕
    cancelBtn=Button(text="重設", font=2, command=IP_Reset) 
    cancelBtn.grid(row=0,column=5)
    #確認欄位(確認輸入的資料)
    check_Label=Label(text='Your IP is: ', font=2) 
    check_Label.grid(row=2,column=0, sticky=W)
    text_IP = Label(text=serverIP, font=2, bg='#fff')
    text_IP.grid(row=2,column=1, sticky="WE") 
    #確認按鈕(按下後進入遊戲)
    checkBtn=Button(text="確認", font=2, command=window.destroy) 
    checkBtn.grid(row=2,column=3)
    window.mainloop()

# TK_connect()