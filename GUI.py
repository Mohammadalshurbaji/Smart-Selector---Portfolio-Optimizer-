from pathlib import Path
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import numpy as np

import pandas as pd
import yfinance as yf
import warnings
import riskfolio as rp

warnings.filterwarnings("ignore")
pd.options.display.float_format = "{:.4%}".format

# Date range
start = "2019-01-01"
end = "2023-12-30"

# Tickers of assets
assets = [
    "AAPL",
    "MSFT",
    "AMZN",
    "GOOGL",
    "TSLA",
    "JPM",
    "V",
    "JNJ",
    "NVDA",
    "PG",
    "MA",
    "HD",
    "DIS",
    "INTC",
    "UNH",
    "VZ",
    "NFLX",
    "ADBE",
    "PYPL",
    "CRM",
    "CMCSA",
    "KO",
]
assets.sort()

# Downloading data
data = yf.download(assets, start=start, end=end)
data = data.loc[:, ("Adj Close", slice(None))]
data.columns = assets

Y = data[assets].pct_change().dropna()

port = rp.Portfolio(returns=Y)

method_mu = "hist"
method_cov = "hist"
port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

model = "Classic"
rm = "MV"
obj = "Sharpe"
hist = True
rf = 0
l = 0

points = 50
frontier = port.efficient_frontier(model=model, rm=rm, points=points, rf=rf, hist=hist)
# print(frontier.T)

mu = port.mu
cov = port.cov
returns = port.returns

abc = frontier
t_factor = 252
risks = []
rets = []
ratios = []
for i in range(abc.shape[1]):
    weights = abc.iloc[:, i].to_numpy().reshape(-1, 1)
    risk = rp.Sharpe_Risk(weights, cov=cov, returns=returns, rm=rm)
    risk = risk * t_factor**0.5
    risks.append(risk)

    mu_ = np.array(mu, ndmin=2)
    ret = mu_ @ weights
    ret = ret.item() * t_factor
    rets.append(ret)

    ratio = (ret - rf) / risk
    ratios.append(ratio)

t_frontier = frontier.T
t_frontier["Expected Return"] = rets
t_frontier["Expected Risk"] = risks
t_frontier["Return Ratio"] = ratios
minrisk = min(t_frontier["Expected Risk"]) * 100


def optimize_portfolio(risk_level):
    if risk_level < minrisk:
        w = pd.DataFrame(
            t_frontier[t_frontier["Expected Risk"] * 100 <= minrisk].iloc[-1, :-3]
        )
        ax = rp.plot_pie(
            w=w,
            title="Optimized Portfolio",
            others=0.05,
            nrow=25,
            cmap="tab20",
            height=6,
            width=10,
            ax=None,
        )
        plt.show()
    else:
        # if risk_level < min(t_frontier['Expected Risk']):
        #     return min(t_frontier['Expected Risk'])
        # else:
        w = pd.DataFrame(
            t_frontier[t_frontier["Expected Risk"] * 100 <= risk_level].iloc[-1, :-3]
        )
        # filtered_frontier = t_frontier[t_frontier['Expected Risk']*100 < risk_level]

        # if not filtered_frontier.empty:
        #     # Proceed with accessing the last row and excluding the last three columns
        #     w = pd.DataFrame(filtered_frontier.iloc[-1, :-3])
        # else:
        #     print("No portfolios found with the specified risk level.")
        ax = rp.plot_pie(
            w=w,
            title="Optimized Portfolio",
            others=0.05,
            nrow=25,
            cmap="tab20",
            height=6,
            width=10,
            ax=None,
        )
        plt.show()


OUTPUT_PATH = Path(__file__).parent

window = Tk()

window.geometry("828x510")
window.configure(bg="#B2D2A4")


def buttonInput():
    # Here are the inputs from user e1 = risk, e2 = investments, e3 = time
    entry_1_value = entry_1.get()
    entry_2_value = entry_2.get()

    entry_1.delete(0, "end")
    entry_2.delete(0, "end")

    if len(entry_1_value) == 0 or len(entry_2_value) == 0:
        print("Please enter data")
    # if entry_1_value < minrisk:
    #     raise ValueError "Please input a number higher than {minrisk}")
    elif entry_1_value == "0":
        w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)
        ax = rp.plot_pie(
            w=w,
            title="Optimal Portfolio",
            others=0.05,
            nrow=25,
            cmap="tab20",
            height=6,
            width=10,
            ax=None,
        )
        plt.show()
    else:

        # remmeber to convert to floats
        try:
            optimize_portfolio(float(entry_1_value))
            # if optimize_portfolio(float(entry_1_value)) is not None:

            # else:
            #     optimize_portfolio(float(entry_1_value))

            # stock_prices = np.random.normal(float(entry_1_value), float(entry_2_value))
            # plt.hist(stock_prices, 50)
            # plt.show()

        except ValueError:

            def delete_textbox():
                new_text.destroy()

            new_text = Text(
                window,
                bg="#D9D9D9",
                fg="#000716",
                height=2,
                width=35,
                wrap="word",
                font=("Comic Sans MS", 12),
            )
            new_text.insert("end", "          Please Enter a valid number: ")
            new_text.place(x=250, y=215)  # Adjust the position as needed

            # Adding a delete button inside the new text box
            delete_button = Button(
                new_text,
                text="Delete",
                command=delete_textbox,
                relief="flat",
                bg="#D9D9D9",
                fg="#000716",
                font=("Comic Sans MS", 12),
            )
            delete_button.place(x=60, y=100)
            new_text.window_create("end", window=delete_button)
            print("Please enter a valid number")


canvas = Canvas(
    window,
    bg="#99AA38",
    height=510,
    width=828,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.place(x=0, y=0)
canvas.create_rectangle(0.0, 0.0, 828.0, 72.0, fill="#14591D", outline="")

canvas.create_text(
    240,
    10,
    anchor="nw",
    text="The Smart Select",
    fill="#0A210F",
    font=("Comic Sans MS", 38 * -1),
)
canvas.create_text(
    290,
    80,
    anchor="nw",
    text="Enter 0 for Optimal Portfolio",
    fill="#0A210F",
    font=("Comic Sans MS", 13),
)
canvas.create_text(
    335,
    110,
    anchor="nw",
    text="Minimum Risk: " + str(int(minrisk)),
    fill="#0A210F",
    font=("Comic Sans MS", 13),
)

canvas.create_text(
    250.0,
    225.0,
    anchor="nw",
    text="Add Investment (USD)",
    fill="#0A210F",
    font=("Comic Sans MS", 30 * -1),
)

entry_bg_1 = canvas.create_image(
    421.5,
    160.0,
)
entry_1 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_1.place(x=315.0, y=174.0, width=173.0, height=34.0)

canvas.create_text(
    305.0,
    130.0,
    anchor="nw",
    text="Enter Risk (%)",
    fill="#0A210F",
    font=("Comic Sans MS", 30 * -1),
)

entry_bg_2 = canvas.create_image(
    421.5,
    308.0,
)
entry_2 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_2.place(x=315.0, y=270.0, width=173.0, height=34.0)

button_1 = Button(
    text="Generate Portfolio",
    font=("Comic Sans MS", 15),
    borderwidth=0,
    highlightthickness=0,
    command=lambda: buttonInput(),
    relief="flat",
)
button_1.place(x=305.0, y=390.0, width=193.0, height=36.0)


window.resizable(False, False)
window.mainloop()
