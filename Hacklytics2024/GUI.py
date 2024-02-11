from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

import yfinance as yf
import pandas as pd
import warnings
import numpy as np

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/tony/Downloads/")


def buttonInput():
    #Here are the inputs from user e1 = risk, e2 = investments, e3 = time
    entry_1.get()
    entry_2.get()
    entry_3.get()
    entry_1.delete(0, 'end')
    entry_2.delete(0, F'end')
    entry_3.delete(0,'end')
    stock_prices=np.random.normal(20000,25000,5000)
    plt.hist(stock_prices, 50)
    plt.show()
window = Tk()

window.geometry("828x510")
window.configure(bg="#B2D2A4")

canvas = Canvas(
    window,
    bg="#2A3D45",
    height=510,
    width=828,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    828.0,
    72.0,
    fill="#7A6C5D",
    outline="")

canvas.create_text(
    260,
    1.0,
    anchor="nw",
    text="Portfolio Generator",
    fill="#1E1C19",
    font=("Comic Sans MS", 38 * -1)
)

canvas.create_text(
    315.0,
    235.0,
    anchor="nw",
    text="Add Investment (USD)",
    fill="#7A6C5D",
    font=("Comic Sans MS", 30 * -1)
)


entry_bg_1 = canvas.create_image(
    421.5,
    160.0,
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=315.0,
    y=174.0,
    width=173.0,
    height=34.0
)

canvas.create_text(
    315.0,
    137.0,
    anchor="nw",
    text="Enter Risk (%)",
    fill="#7A6C5D",
    font=("Comic Sans MS", 30 * -1)
)


entry_bg_2 = canvas.create_image(
    421.5,
    308.0,
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=315.0,
    y=270.0,
    width=173.0,
    height=34.0
)

button_1 = Button(
    text="Generate Portfolio",
    font=("Comic Sans MS", 15),
    borderwidth=0,
    highlightthickness=0,
    command=lambda: buttonInput(),
    relief="flat"
)
button_1.place(
    x=305.0,
    y=460.0,
    width=193.0,
    height=36.0
)
canvas.create_text(
    315.0,
    325.0,
    anchor="nw",
    text="Enter Time (DAYS)",
    fill="#7A6C5D",
    font=("Comic Sans MS", 30 * -1)

)


entry_bg_3 = canvas.create_image(
    421.5,
    308.0,
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",

    highlightthickness=0
)
entry_3.place(
    x=315.0,
    y=365.0,
    width=173.0,
    height=34.0
)
window.resizable(False, False)
window.mainloop()
