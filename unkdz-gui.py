import os.path
import sys
import threading
import webbrowser

from tkinter import *
from tkinter import ttk, filedialog

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from undz import DZFileTools
from unkdz import KDZFileTools

window = Tk()
window.title("KDZ解包")
window.geometry('400x120')
window.resizable(False, False)

filename = StringVar(window)
dirname = StringVar(window)
status = StringVar(window)


def browse_file():
    val = filedialog.askopenfilename(initialdir="/", title="选择KDZ文件",
                                     filetypes=(("kdz files", "*.kdz"), ("all files", "*.*")))
    if val:
        filename.set(val)
        if not dirname.get():
            val = os.path.dirname(val) + '/' + os.path.basename(val)[:-4]
            dirname.set(val)


def browse_dir():
    val = filedialog.askdirectory(initialdir="/", title="选择解包目录", )
    if val:
        dirname.set(val)


def open_browser(_):
    webbrowser.open("https://lgrom.com/")


def open_dir(_):
    if dirname.get():
        os.startfile(dirname.get())


def process_task():
    try:
        kdzfile = filename.get()
        outdir = dirname.get()

        kdztools = KDZFileTools()
        kdztools.run(kdzfile, outdir, extractID=0)

        dzfile = kdztools.partList[0][0].decode()

        dztools = DZFileTools()
        dztools.run(outdir + '/' + dzfile, outdir, extractChunk=1)
        dztools.run(outdir + '/' + dzfile, outdir, rawprogram=1)

        status.set('解包完成')

    except Exception as e:
        status.set('解包失败 ' + repr(e))


def start_task():
    if status.get() in ['', '解包完成']:
        status.set('正在解包...')
        thread1 = threading.Thread(target=process_task)
        thread1.start()


ttk.Label(window, text="KDZ文件").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(window, textvariable=filename, width=30).grid(row=0, column=1, pady=5)
ttk.Button(window, text="浏览", command=browse_file, width=6).grid(row=0, column=2, pady=5)
a = ttk.Label(window, text="下载KDZ", foreground="blue", cursor="hand2")
a.grid(row=0, column=3, padx=5, pady=5)
a.bind("<Button-1>", open_browser)

ttk.Label(window, text="解包目录").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(window, textvariable=dirname, width=30).grid(row=1, column=1, pady=5)
ttk.Button(window, text="浏览", command=browse_dir, width=6).grid(row=1, column=2, pady=5)
b = ttk.Label(window, text="打开目录", foreground="blue", cursor="hand2")
b.grid(row=1, column=3, padx=5, pady=5)
b.bind("<Button-1>", open_dir)

ttk.Label(window, textvariable=status).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
ttk.Button(window, text="解包", command=start_task).grid(row=2, column=2, columnspan=2, padx=5, pady=5)

window.mainloop()
