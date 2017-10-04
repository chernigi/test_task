"""python 2.7"""

from Tkinter import *
import tkMessageBox
import scipy.stats as stats
import numpy as np
import string
import collections
import random

class mGUI:
    def __init__(self, master):
        """initialize GUI"""
        frame = Frame(master)
        frame.pack()
        self.top_label_sax = Label(frame, text="Please specify the input parameters for SAX")
        self.ts_len = Label(frame, text="Time Series Length:")
        self.alphabet_size = Label(frame, text="Alphabet Size:")
        self.paa_size = Label(frame, text="PAA Size:")
        self.ts_len_entry = Entry(frame, textvariable=ts_len_var)
        self.alphabet_size_entry = Entry(frame, textvariable=alphabet_size_var)
        self.paa_size_entry = Entry(frame, textvariable=paa_size_var)
        self.calculate_button1 = Button(frame, text="Calculate", command=lambda: alphabet_transformation(ts_len_var, paa_size_var, alphabet_size_var))
        self.calculate_button1.bind("<Button-1>")
        self.top_label_sax.grid(row=0)
        self.ts_len.grid(row=1)
        self.alphabet_size.grid(row=2)
        self.paa_size.grid(row=3)
        self.ts_len_entry.grid(row=1, column=1)
        self.alphabet_size_entry.grid(row=2, column=1)
        self.paa_size_entry.grid(row=3, column=1)
        self.calculate_button1.grid(row=4, column=1)
        self.bottom_label = Label(frame, text="The SAX-Represenatation")
        self.bottom_label.grid(row=5)
        self.result_statistics = Label(frame, text="Statistics")
        self.result_statistics.grid(row=6)
        self.result_label = Label(frame, text="Press Calculate to see the result")
        self.result_label.grid(row=5, column=1)
        self.result_label_statistics = Label(frame, text="-")
        self.result_label_statistics.grid(row=6, column =1)
        self.exitButton = Button(frame, text="Exit", command=frame.quit)
        self.exitButton.grid(row=7, column=1)

        def generate_ts(ts_size):
            """generates a time series with a Gaussian noise"""
            x = np.arange(ts_size)
            f = 5
            noise = 0.0008 * np.asarray(random.sample(range(0, 1000), ts_size))
            ts = np.sin(2 * np.pi * x * f / 800) + noise
            return ts

        def znorm(ts):
            """normalize ts using zero normalization, so that mean is 0 and standard deviation is 1"""
            mean_ts = ts.mean()
            std_ts = np.std(ts)
            ts_norm=(ts-mean_ts)/std_ts
            return ts_norm

        def PAA(ts_norm, n_chunks):
            """create a PAA representation of the normalized ts:
            divide the normalized ts into n_chunks equal parts and for each calculate the mean"""
            length_ts = ts_norm.size
            chunk_mean=np.zeros((n_chunks))
            try:
                if len(ts_norm) % n_chunks == 0: #if divided without a remainder
                    ts_split = np.split(ts_norm, n_chunks, axis=0)
                    chunk_mean = np.asarray(map(lambda xs: xs.mean(axis=0), ts_split))
                else:
                    ts_split = np.zeros((n_chunks))
                    for i in range(0, length_ts * n_chunks-1):
                        idx = i // length_ts
                        pos = i // n_chunks
                        ts_split[idx] = ts_split[idx] + ts_norm[pos]
                    for i in range(0, n_chunks):
                        chunk_mean[i] = ts_split[i]/length_ts
                return chunk_mean
            except ZeroDivisionError:
                tkMessageBox.showinfo("Error", "PAA can not be 0")

        def alphabet_transformation(ts_size, n_chunks, alphabet_size):
            """transform PAA to alphabet representation"""
            ts_size=ts_len_var.get()
            n_chunks=paa_size_var.get()
            alphabet_size=alphabet_size_var.get()
            if alphabet_size > 26 or alphabet_size<1:
                tkMessageBox.showinfo("Error", "The alphabet size can not be greater than 26 and smaller than 0")
                return
            else:
                alphabet=string.ascii_lowercase[:alphabet_size]
            ts=generate_ts(ts_size)
            #get precomputed breakpoints for the given alphabet size
            breakpoints = stats.norm.ppf(np.linspace(1./alphabet_size,
                                            1-1./alphabet_size,
                                            alphabet_size-1))
            def translate(ts_values):
               """assign alphabet char to a ts data point"""
               return np.asarray([(alphabet[0] if ts_value < breakpoints[0]
                        else (alphabet[-1] if ts_value > breakpoints[-1]
                                else alphabet[np.where(breakpoints <= ts_value)[0][-1]+1]))
                                    for ts_value in ts_values])
            ts_norm=znorm(ts)
            paa_ts = PAA(ts_norm, n_chunks)
            sax_result = np.apply_along_axis(translate, 0, paa_ts)
            update_label(sax_result)
            update_statistics(sax_result, n_chunks)

        def update_label(sax_result):
            """update the result field in GUI"""
            self.result_label.config(text=str(sax_result))

        def update_statistics(sax_result, n_chunks):
            """give statistics about characters in the SAX representation"""
            stat_dict={}
            stat_dict_sorted=collections.OrderedDict()
            for i in range(0,n_chunks):
                if sax_result[i] in stat_dict.keys():
                    stat_dict[sax_result[i]] = stat_dict.get(sax_result[i]) + 1
                else:
                    stat_dict[sax_result[i]]=1
            sortedalphabet = sorted(stat_dict.keys(), key=lambda x: x.lower()) #sort statistics alphabetically
            result_statistics=list()
            for i in sortedalphabet:
                values = stat_dict[i]
                stat_dict_sorted[i] = values
                result_statistics.extend((str(i)+"="+str(values)+","))
            result_statistics=result_statistics[:-1] #remove last comma
            self.result_label_statistics.config(text=result_statistics)

root = Tk()
ts_len_var = IntVar()
alphabet_size_var = IntVar()
result_var=StringVar()
paa_size_var = IntVar()
root.title("SAX Implementation")
start_app=mGUI(root)
root.mainloop()

