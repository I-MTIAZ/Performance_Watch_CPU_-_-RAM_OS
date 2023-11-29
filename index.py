import psutil
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class ResourceMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resource Monitor")

        # Set the initial size of the window
        self.root.geometry("800x600")  # Change the width and height as needed

        # Configure row and column weights to make them expandable
        self.root.grid_rowconfigure(1, weight=1, minsize=50)  # Set a minimum size for row 1
        self.root.grid_rowconfigure(2, weight=1, minsize=50)  # Set a minimum size for row 2
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Change font size for labels
        label_font = ('Helvetica', 12)  # Change the font and size as needed
        frame = tk.Frame(root)
 
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("green.Horizontal.TProgressbar",
            foreground='red', background='green')

        self.label_cpu = tk.Label(root, text="CPU Usage: ", font=label_font)
        self.label_cpu.grid(row=0, column=0, padx=1,pady=10, )

        self.progressbar_cpu = ttk.Progressbar(root, orient="horizontal", mode='determinate', length=400)
        self.progressbar_cpu.grid(row=0, column=1, padx=5)

        self.label_ram = tk.Label(root, text="RAM Usage: ", font=label_font)
        self.label_ram.grid(row=1, column=0, padx=5)

        self.progressbar_ram = ttk.Progressbar(root, orient="horizontal", mode='determinate', length=400,style='green.Horizontal.TProgressbar')
        self.progressbar_ram.grid(row=1, column=1, padx=5)

        # Matplotlib figure and axis for the graph
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)

        # Canvas to embed the graph in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")  # Span across all columns

        # Lists to store historical data for the graph
        self.cpu_data = []
        self.ram_data = []
        self.timestamps = []

        # Variables to control what to display
        self.show_cpu_var = tk.BooleanVar(value=True)  # Set to True initially
        self.show_ram_var = tk.BooleanVar(value=True)  # Set to True initially

        # Add buttons
        
        self.cpu_button = tk.Button(root, text="Show CPU", command=self.show_cpu,width=20,height=2,bg='#4B99F2',font=('Helvetica', 10),relief="groove")
        self.cpu_button.grid(row=3, column=0, pady=5)

        self.ram_button = tk.Button(root, text="Show RAM", command=self.show_ram,width=20,height=2,bg='#4CAF50',font=('Helvetica', 10),relief="groove")
        self.ram_button.grid(row=3, column=1, pady=5)

        self.both_button = tk.Button(root, text="Show Both", command=self.show_both,width=20,height=2,bg='#A1C2B9',font=('Helvetica', 10),relief="groove")
        self.both_button.grid(row=3, column=2, pady=5)

        self.update_labels_and_graph()

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_ram_usage(self):
        return psutil.virtual_memory().percent

    def update_labels_and_graph(self):
        cpu_usage = self.get_cpu_usage()
        ram_usage = self.get_ram_usage()

        # Update labels
        self.label_cpu.config(text=f"CPU Usage: {cpu_usage}%", font=('Helvetica', 12))
        self.progressbar_cpu['value'] = cpu_usage

        self.label_ram.config(text=f"RAM Usage: {ram_usage}%", font=('Helvetica', 12))
        self.progressbar_ram['value'] = ram_usage

        # Update data lists for the graph
        timestamp = datetime.now()
        self.timestamps.append(timestamp)
        self.cpu_data.append(cpu_usage)
        self.ram_data.append(ram_usage)

        # Clear the previous plot
        self.ax.clear()

        # Plot lines for CPU and RAM data based on button press
        if self.show_cpu_var.get():
            self.ax.plot(self.timestamps, self.cpu_data, label='CPU Usage', color='blue')

        if self.show_ram_var.get():
            self.ax.plot(self.timestamps, self.ram_data, label='RAM Usage', color='green')

        # Set labels and legend
        self.ax.set_ylabel('Usage (%)')
        self.ax.set_xlabel('Time')
        self.ax.legend()

        # Format x-axis as timestamps
        self.ax.xaxis_date()

        # Update canvas
        self.canvas.draw()

        # Schedule the update after 1000 milliseconds (1 second)
        self.root.after(1000, self.update_labels_and_graph)

    def show_cpu(self):
        self.show_cpu_var.set(True)
        self.show_ram_var.set(False)

    def show_ram(self):
        self.show_cpu_var.set(False)
        self.show_ram_var.set(True)

    def show_both(self):
        self.show_cpu_var.set(True)
        self.show_ram_var.set(True)

def main():
    root = tk.Tk()
    app = ResourceMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
