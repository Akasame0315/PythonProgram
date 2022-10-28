from cgitb import text
from doctest import master
import imp
from re import X
from sqlite3 import Row
from textwrap import fill
import tkinter as tk
from tkinter.tix import COLUMN  # 使用Tkinter前需要先匯入
from tkinter import *
import GlobalValue

GlobalValue.initial()

# 例項化object，建立視窗window
window = tk.Tk()
window.title('IP SETTING')
window.geometry('500x300')  # 這裡的乘是小x

serverIP = ''
# serverIP = GlobalValue.serverIP
text_IP = Label(text=serverIP)

def insert_end():   # 在文字框內容最後接著插入輸入內容
    global serverIP
    global text_IP
    serverIP = entry_IP.get()
    print("IP: ", serverIP)
    text_IP = Label(text=serverIP)
    text_IP.grid(row=1,column=1, sticky=W) 
    # GlobalValue.serverIP = serverIP

def IP_Reset():   # 在文字框內容最後接著插入輸入內容
    global serverIP
    global text_IP
    serverIP = ""
    entry_IP.delete(0, END)
    text_IP.grid_forget()

print("IP: ", serverIP)
label_IP=Label(text='Entry your IP: :', height=2) 
label_IP.grid(row=0,column=0,sticky=W) #一個有sticky,一個沒有sticky，以作區分 
entry_IP=Entry(font=2)
entry_IP.grid(row=0,column=1, sticky=W)
setBtn=Button(text="設置", command=insert_end) 
setBtn.grid(row=0,column=3,columnspan=2,padx=5, pady=5) # 下面主要是將第一列拉大來顯示上面sticky的效果 

check_Label=Label(text='Your IP is: ') 
check_Label.grid(row=1,column=0, sticky=W) 
text_IP = Label(text=serverIP)
text_IP.grid(row=1,column=1, sticky=W) 

checkBtn=Button(text="確認", command=window.destroy) 
checkBtn.grid(row=1,column=3)
cancelBtn=Button(text="重設", command=IP_Reset) 
cancelBtn.grid(row=1,column=4)

# window.mainloop()