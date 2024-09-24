import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random

# Define the symbols, payouts and frequencies
symbols = ['@', '$', '&', '!', '*']

payouts = {'@': 2, '$': 5, '&': 7, '!': 10, '*': 100}

freq_table = [[5, 9, 13, 21, 1],
             [12, 8, 14, 18, 2],
             [9, 4, 13, 17, 3]]

total_bet = 0
total_winnings = 0
jackpot_wins = 0
current_spin = 0
num_spins = 0

def spin():
    #randomizing middle row with frequencies
    middle_row = [
        random.choices(symbols, weights=freq_table[0])[0],
        random.choices(symbols, weights=freq_table[1])[0],
        random.choices(symbols, weights=freq_table[2])[0]]

    # upper row = (index-1) and lower row = (index+1)
    upper_row = [symbols[(symbols.index(x) - 1) % len(symbols)] for x in middle_row]
    lower_row = [symbols[(symbols.index(x) + 1) % len(symbols)] for x in middle_row]

    return [upper_row, middle_row, lower_row]


def calc_winning(middle_row):
    if len(set(middle_row)) == 1:  
        return payouts[middle_row[0]] 
    return 0 


def delay_func():
    global current_spin, num_spins
    if current_spin < num_spins:
        update_display()
        current_spin += 1
        root.after(1500, delay_func)
    else:
        spin_entry.delete(0, tk.END)


def spin_caller():
    global current_spin, num_spins
    try:
        num_spins = int(spin_entry.get())
        if num_spins < 1:
            raise ValueError("Number of spins must be greater than 0")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number of spins")
        return

    current_spin = 0
    delay_func()


def update_display():
    global balance, total_bet, total_winnings, jackpot_wins
    balance -= bet
    total_bet += bet

    spin_result = spin()

    # Update the display
    slot1.config(text=spin_result[0][0])
    slot2.config(text=spin_result[0][1])
    slot3.config(text=spin_result[0][2])

    slot4.config(text=spin_result[1][0])
    slot5.config(text=spin_result[1][1])
    slot6.config(text=spin_result[1][2])

    slot7.config(text=spin_result[2][0])
    slot8.config(text=spin_result[2][1])
    slot9.config(text=spin_result[2][2])

    middle_row = spin_result[1]

    winnings = calc_winning(middle_row)

    balance += winnings
    total_winnings += winnings

    #Jackpot
    if middle_row == ['*', '*', '*']:
        jackpot_wins += 1

    balance_label.config(text=f"Balance: {balance}")
    rtp = (total_winnings / total_bet) * 100 if total_bet > 0 else 0
    rtp_label.config(text=f"RTP: {rtp:.2f}%")
    jackpot_label.config(text=f"Jackpot Wins: {jackpot_wins}")

    if winnings > 0:
        messagebox.showinfo("Congratulations!", f"You won {winnings}!")

    if balance < bet:
        messagebox.showinfo("Game Over", "You ran out of balance!")
        root.quit()


# Main window
root = tk.Tk()
root.title("Slot Machine")
root.geometry("600x600")
root.configure(bg='#4390a3')

# Initial balance and bet amount
balance = 10
bet = 1

slot_frame = tk.Frame(root, bg='#4390a3')
slot_frame.pack(pady=50)

slot1 = tk.Label(slot_frame, text='?', font=('Arial', 30), width=5, bg='#e0f7fa')
slot1.grid(row=0, column=0, padx=5, pady=5)
slot2 = tk.Label(slot_frame, text='?', font=('Arial', 30), width=5, bg='#e0f7fa')
slot2.grid(row=0, column=1, padx=5, pady=5)
slot3 = tk.Label(slot_frame, text='?', font=('Arial', 30), width=5, bg='#e0f7fa')
slot3.grid(row=0, column=2, padx=5, pady=5)

slot4 = tk.Label(slot_frame, text='?', font=('Arial', 30), width=5, bg='#e0f7fa')
slot4.grid(row=1, column=0, padx=5, pady=5)
slot5 = tk.Label(slot_frame, text='?', font=('Arial', 30), width=5, bg='#e0f7fa')
slot5.grid(row=1, column=1, padx=5, pady=5)
slot6 = tk.Label(slot_frame, text='?', font=('Arial', 30), width=5, bg='#e0f7fa')
slot6.grid(row=1, column=2, padx=5, pady=5)

slot7 = tk.Label(slot_frame, text='?', font=('Arial', 30), width=5, bg='#e0f7fa')
slot7.grid(row=2, column=0, padx=5, pady=5)
slot8 = tk.Label(slot_frame, text='?', font=('Arial', 30), width=5, bg='#e0f7fa')
slot8.grid(row=2, column=1, padx=5, pady=5)
slot9 = tk.Label(slot_frame, text='?', font=('Arial', 30), width=5, bg='#e0f7fa')
slot9.grid(row=2, column=2, padx=5, pady=5)


balance_label = tk.Label(root, text=f"Balance: {balance}", font=('Arial', 14, 'bold'), bg='#4390a3')
balance_label.pack(pady=10)

rtp_label = tk.Label(root, text=f"RTP: 0.00%", font=('Arial', 14, 'bold'), bg='#4390a3')
rtp_label.pack(pady=5)

jackpot_label = tk.Label(root, text=f"Jackpot Wins: 0", font=('Arial', 14, 'bold'), bg='#4390a3')
jackpot_label.pack(pady=5)

spin_label = tk.Label(root, text="Enter number of spins:", font=('Arial', 14, 'bold'), bg='#4390a3')
spin_label.pack(pady=10)

spin_entry = tk.Entry(root, font=('Arial', 14))
spin_entry.pack(pady=10)

spin_button = tk.Button(root, text="Spin", command=spin_caller, font=('Arial', 14), bg='#00796b', fg='#e0f7fa')
spin_button.pack(pady=20)

root.mainloop()
