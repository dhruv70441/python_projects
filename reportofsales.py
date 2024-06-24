import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

class Report:
    def __init__(self, root):
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="dhruvp@70441",
            database="mydata"
        )

        query = "SELECT * FROM sales"
        self.df = pd.read_sql(query, self.conn)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['Amount'] = pd.to_numeric(self.df['Amount'])
        self.df['Quantity'] = pd.to_numeric(self.df['Quantity'])

        self.root = root
        self.root.title("Sales Dashboard")
        self.root.geometry("1000x700")

        self.setup_ui()

    def setup_ui(self):
        # Layout
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=1)

        self.left_frame = Frame(self.main_frame, width=200, bg='lightgrey', padx=10, pady=10)
        self.left_frame.pack(side=LEFT, fill=Y)

        self.chart_frame = Frame(self.main_frame, bg='white')
        self.chart_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        # Date range inputs
        Label(self.left_frame, text="Starting Date (YYYY-MM-DD)", bg='lightgrey').pack(pady=5)
        self.start_date_entry = Entry(self.left_frame)
        self.start_date_entry.pack(pady=5)

        Label(self.left_frame, text="Ending Date (YYYY-MM-DD)", bg='lightgrey').pack(pady=5)
        self.end_date_entry = Entry(self.left_frame)
        self.end_date_entry.pack(pady=5)

        # Chart type toggle buttons
        toggle_frame = Frame(self.main_frame)
        toggle_frame.pack(side=TOP, fill=X)

        ttk.Button(toggle_frame, text="Line Chart", command=lambda: self.create_plot_window("Sales Over Time", self.plot_sales_over_time, 'line')).pack(side=LEFT, padx=10)
        ttk.Button(toggle_frame, text="Bar Chart", command=lambda: self.create_plot_window("Sales Over Time", self.plot_sales_over_time, 'bar')).pack(side=LEFT, padx=10)

        # Time period filter buttons
        filter_frame = Frame(self.main_frame)
        filter_frame.pack(side=TOP, fill=X)

        ttk.Button(filter_frame, text="Monthly", command=lambda: self.create_plot_window("Sales Over Time", self.plot_sales_over_time, 'line')).pack(side=LEFT, padx=10)
        ttk.Button(filter_frame, text="Quarterly", command=lambda: self.create_plot_window("Sales Over Time", self.plot_sales_over_time, 'line')).pack(side=LEFT, padx=10)

        # Chart list and buttons
        Label(self.left_frame, text="Charts", bg='lightgrey', font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Button(self.left_frame, text="Sales Over Time", command=lambda: self.create_plot_window("Sales Over Time", self.plot_sales_over_time, 'line')).pack(pady=5)
        ttk.Button(self.left_frame, text="Quantity Over Time", command=lambda: self.create_plot_window("Quantity Over Time", self.plot_quantity_over_time, 'line')).pack(pady=5)
        ttk.Button(self.left_frame, text="Top Medicines", command=lambda: self.create_plot_window("Top Medicines", self.plot_top_meds, 'bar')).pack(pady=5)
        ttk.Button(self.left_frame, text="Top Medicines Contribution", command=lambda: self.create_plot_window("Top Medicines Contribution", self.plot_top_meds_pie, 'pie')).pack(pady=5)
        ttk.Button(self.left_frame, text="Top Selling Days", command=lambda: self.create_plot_window("Top Selling Days", self.plot_top_selling_days, 'bar')).pack(pady=5)
        ttk.Button(self.left_frame, text="Stacked Sales", command=lambda: self.create_plot_window("Stacked Sales", self.plot_stacked_sales, 'bar')).pack(pady=5)
        ttk.Button(self.left_frame, text="Rate vs Quantity", command=lambda: self.create_plot_window("Rate vs Quantity", self.plot_rate_vs_quantity, 'scatter')).pack(pady=5)
        ttk.Button(self.left_frame, text="Sales Distribution", command=lambda: self.create_plot_window("Sales Distribution", self.plot_sales_distribution, 'hist')).pack(pady=5)

    def filter_data(self, start_date, end_date):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_df = self.df[(self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)]
        return filtered_df

    def create_plot_window(self, title, plot_func, plot_type):
        self.clear_canvas()
        fig, ax = plt.subplots(figsize=(8, 6))
        plot_func(ax, plot_type)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def plot_sales_over_time(self, ax, plot_type):
        filtered_df = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).resample('M', on='Date').sum()
        filtered_df['Amount'].plot(ax=ax, kind=plot_type, color='blue', title='Sales Amount Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sales Amount')
        ax.legend(['Sales Amount'])

    def plot_quantity_over_time(self, ax, plot_type):
        filtered_df = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).resample('M', on='Date').sum()
        filtered_df['Quantity'].plot(ax=ax, kind=plot_type, color='green', title='Quantity Sold Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Quantity Sold')
        ax.legend(['Quantity Sold'])

    def plot_top_meds(self, ax, plot_type):
        top_meds = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).groupby('TabletName')['Quantity'].sum().nlargest(10)
        top_meds.plot(kind='bar', ax=ax, color='purple', title='Top 10 Sold Medicines')
        ax.set_xlabel('Medicine')
        ax.set_ylabel('Quantity Sold')
        ax.legend(['Quantity Sold'])

    def plot_top_meds_pie(self, ax, plot_type):
        top_meds = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).groupby('TabletName')['Quantity'].sum().nlargest(10)
        top_meds.plot(kind='pie', ax=ax, autopct='%1.1f%%', title='Top 10 Medicines Contribution to Sales')

    def plot_top_selling_days(self, ax, plot_type):
        top_days = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).groupby('Date')['Amount'].sum().nlargest(10)
        top_days.plot(kind='bar', ax=ax, color='orange', title='Top 10 Selling Days')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sales Amount')
        ax.legend(['Sales Amount'])

    def plot_stacked_sales(self, ax, plot_type):
        stacked_data = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).pivot_table(values='Quantity', index='Date', columns='TabletName', aggfunc='sum')
        stacked_data.plot(kind='bar', stacked=True, ax=ax, title='Sales Quantities of Different Medicines by Date')
        ax.set_xlabel('Date')
        ax.set_ylabel('Quantity Sold')
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    def plot_rate_vs_quantity(self, ax, plot_type):
        sns.scatterplot(data=self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()), x='Rate', y='Quantity', ax=ax)
        ax.set_title('Rate vs Quantity Sold')
        ax.set_xlabel('Rate')
        ax.set_ylabel('Quantity Sold')

    def plot_sales_distribution(self, ax, plot_type):
        sns.histplot(self.filter_data(self.start_date_entry.get(), self.end_date_entry.get())['Amount'], bins=20, ax=ax)
        ax.set_title('Distribution of Sales Amounts')
        ax.set_xlabel('Sales Amount')
        ax.set_ylabel('Frequency')

    def clear_canvas(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    app = Report(root)
    root.mainloop()
