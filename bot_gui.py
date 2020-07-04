from bot import RiceBot
import tkinter as tk
from tkinter import messagebox

def run_bot(entry_val, chosen_category):
    '''
    Creates a RiceBot that runs on the given category and answers the number of
    questions specified by the input box.

    Parameters
    ----------
    entry_val : str
        The given input that was entered through the text field, represents the
        number of questions to be answered

    chosen_category : str
        The category for the bot to answer questions of
    '''

    try:
        num_questions = int(entry_val)
        bot = RiceBot(chosen_category)
        bot.run(num_questions)
    except ValueError:
        messagebox.showerror("Bad Input", "The input for number of questions must be a number!")
    except:
        messagebox.showerror("Failed", "Failed to run bot for some reason")


HEIGHT = 250
WIDTH = 500

# the categories that this bot supports right now
categories = {"english-vocabulary", "multiplication-table", "famous-quotations", "spanish", 
"french", "german", "italian", "czech", "latin"}

root = tk.Tk()
root.title("Free Rice Bot")

# the canvas
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

# the frame
frame = tk.Frame(root, bg="#80c1ff", bd=10)
frame.place(relx = 0.05, rely = 0.05, relw = 0.9, relh = 0.9)

# the submit button
button = tk.Button(frame, text = "Submit", command = lambda: run_bot(entry.get(), chosen_category.get()))
button.place(anchor = 'n', relx = 0.5, rely = 0.8, relwidth = 0.2, relheight = 0.1)

# the category label
label1 = tk.Label(frame, text = "Category:")
label1.place(relx = 0.6, rely = 0, relwidth = 0.4, relheight = 0.2)

# the chosen category variable
chosen_category = tk.StringVar(root)
chosen_category.set("english-vocabulary")

# the dropdown menu to choose the category
dropdown = tk.OptionMenu(frame, chosen_category, *categories)
dropdown.place(relx = 0.6, rely = 0.25, relwidth = 0.4, relheight = 0.1)

# the input field to enter the number of questions for the bot to answer
entry = tk.Entry(frame)
entry.place(relx = 0, rely = 0.25, relwidth = 0.5, relheight = 0.1)

# the number of questions label
label2 = tk.Label(frame, text = "Number of Questions:")
label2.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.2)

root.mainloop()