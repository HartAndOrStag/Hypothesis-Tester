from hypothesisTester import HypothesisTester
import tkinter

# initialize tkinter root
root = tkinter.Tk()

# set default window size
root.geometry("600x400")

# run hypothesis tester app
HypothesisTester(root)
root.mainloop()