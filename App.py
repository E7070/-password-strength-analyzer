import argparse
import tkinter as tk
from tkinter import messagebox
from analyzer import analyze


# ---------------- GUI PART ---------------- #

def launch_gui():
    def check_password():
        password = entry.get()

        if not password:
            messagebox.showwarning("Warning", "Please enter a password!")
            return

        result = analyze(password)

        strength_label.config(text=f"Strength: {result['strength']}")
        entropy_label.config(text=f"Entropy: {result['entropy']}")
        crack_label.config(text=f"Crack Time: {result['crack_time']}")

        tips_text.delete("1.0", tk.END)
        if result["tips"]:
            for tip in result["tips"]:
                tips_text.insert(tk.END, f"- {tip}\n")
        else:
            tips_text.insert(tk.END, "Your password looks excellent!")


    root = tk.Tk()
    root.title("Password Strength Analyzer")
    root.geometry("420x420")
    root.resizable(False, False)

    tk.Label(root, text="Password Strength Analyzer", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(root, text="Enter Password").pack()
    entry = tk.Entry(root, show="*", width=30, font=("Arial", 12))
    entry.pack(pady=5)

    tk.Button(root, text="Analyze", command=check_password).pack(pady=10)

    strength_label = tk.Label(root, text="Strength: ")
    strength_label.pack()
    entropy_label = tk.Label(root, text="Entropy: ")
    entropy_label.pack()
    crack_label = tk.Label(root, text="Crack Time: ")
    crack_label.pack()

    tk.Label(root, text="Suggestions").pack(pady=5)
    tips_text = tk.Text(root, height=8, width=45)
    tips_text.pack()

    root.mainloop()


# ---------------- CLI PART ---------------- #

def launch_cli(password):
    result = analyze(password)

    print("\n🔐 Password Strength Analysis 🔐\n")
    print(f"Length      : {result['length']}")
    print(f"Entropy     : {result['entropy']}")
    print(f"Strength    : {result['strength']}")
    print(f"Crack Time  : {result['crack_time']}")

    if result["tips"]:
        print("\nSuggestions:")
        for tip in result["tips"]:
            print(f"- {tip}")
    else:
        print("\nYour password looks excellent! 🎉")


# ---------------- MAIN ---------------- #

def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer (CLI + GUI)")
    parser.add_argument("-p", "--password", help="Password to analyze (CLI mode)")
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")

    args = parser.parse_args()

    if args.gui:
        launch_gui()
    elif args.password:
        launch_cli(args.password)
    else:
        print("\nNo mode selected. Try:\n")
        print("CLI : python app.py -p MyPass@123")
        print("GUI : python app.py --gui\n")


if __name__ == "__main__":
    main()
