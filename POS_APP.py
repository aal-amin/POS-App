import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MainFrame(tk.Frame):
    def __init__(self, parent, Items, HeightOfItems):
        super().__init__(parent)
        self.Items = Items
        self.Height = HeightOfItems
        self.HeightOfItems = len(self.Items)*HeightOfItems
        self.pack(expand=True, fill='both')
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side='top', expand=True, fill='both')
        self.Left_frame()
        self.Right_frame()
        self.Bottom_frame()


    #left frame
    def Left_frame(self):
        self.left_frame = tk.Frame(self.top_frame, bg="lightblue", width=200)#200
        self.left_frame.pack(side='left', expand=True, fill='both')
        self.left_frame.pack_propagate(False)
        
        self.canvas = tk.Canvas(self.left_frame,
                                background='#dad7c5',
                                scrollregion=(0,0, 200,
                                self.HeightOfItems))#200
        self.canvas.pack(expand=True, fill='both')

        global display_items
        display_items = tk.Frame(self.left_frame, bg='#dad7c5')
        self.canvas_window = self.canvas.create_window((0,0),
                                                       window=display_items,
                                                       anchor='nw',
                                                       width=347,
                                                       height=self.HeightOfItems)
        
        #up-down scroll bar == yview
        scrollBar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollBar.set)
        scrollBar.place(relx=1, rely=0, anchor="ne", relheight=1)
        
        self.canvas.bind_all('<Button-4>', self.Scroll)       
        self.canvas.bind_all('<Button-5>', self.Scroll)

        self.images = [] # for image 
        
        for index, item in enumerate(self.Items):
            self.PlaceItem(item).pack(expand=True, fill='both', padx=6, pady=4)

    def Scroll(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, 'units') #scroll up
        elif event.num == 5:
            self.canvas.yview_scroll(1, 'units') #scroll down


    def PlaceItem(self, item):
        ItemFrame = tk.Frame(display_items, bg='white', highlightbackground="#ccc", highlightthickness=1)
        ItemFrame.rowconfigure((0, 1, 2), weight=1)
        ItemFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, uniform='a')

        try:
            img = Image.open(item[3])
            img = img.resize((100, 100))  #image resize
            photo = ImageTk.PhotoImage(img)
            self.images.append(photo)
        except Exception as e:
            photo = None

        # Image
        if photo:
            img_label = ttk.Label(ItemFrame, image=photo)
            img_label.grid(row=0, column=0, columnspan=3, rowspan=3, sticky='nsw', padx=5, pady=5)
        else:
            ttk.Label(ItemFrame, text="No Image").grid(row=0,
                                                       column=0,
                                                       columnspan=3,
                                                       rowspan=3,
                                                       sticky='nsw',padx=5)

        #product name
        ttk.Label(ItemFrame, 
                text=item[0].upper(),  
                font=("Arial", 12, "bold"),
                anchor='w',
                  background='white').grid(row=0, column=3, columnspan=5, sticky='w', padx=5)

        # Price
        ttk.Label(ItemFrame,
                text=f"{item[1]} tk",
                foreground="orange",
                font=("Arial", 12, "bold"),
                anchor='e',
                  background='white').grid(row=0, column=8, columnspan=2, sticky='e', padx=5)

        # Quantity
        ttk.Label(ItemFrame,
                text=f"Quantity: {item[2]}x",
                font=("Arial", 10),
                anchor='w',
                  background='white').grid(row=1, column=3, columnspan=7, sticky='w', padx=5)

        # Add to Cart Button
        ttk.Button(ItemFrame,
                text='🛒 Add to Receipt',
                style='Cart.TButton',
                command=lambda item=item: self.Select_product(item)).grid(row=2,
                                                                          column=3,
                                                                          columnspan=7,
                                                                          sticky='ew',
                                                                          padx=5, pady=5)
        return ItemFrame

    #update the receipt's items
    def Update_receipt(self):        
        self.receipt_box.delete('1.0', tk.END)
        total_amount=0
        self.receipt_box.insert(tk.END,'ITEM       QTY       PRICE \n...........................\n')
        for item in receipt_data:
            line = f"{item[0]:<11} x{item[2]:<7} ৳{item[1]*item[2]}\n"
            self.receipt_box.insert('end', line)
            total_amount += item[1]*item[2]
        self.receipt_box.insert('end', f'\n...........................\n')
        self.receipt_box.insert('end', f'TOTAL                ৳{total_amount}\n')
        self.receipt_box.insert('end', f'Cash                 ৳{total_amount+50}\n')
        self.receipt_box.insert('end', f'Change               ৳{total_amount+50-total_amount}\n')
        self.receipt_box.insert('end', '...........................\n')
        self.receipt_box.insert('end','\n        THANK YOU!     \n')

    #click on add to receipt button
    def Select_product(self, items):
        for item in receipt_data:
            if item[0]==items[0]:
                item[2] += 1
                break
        else:
            items[2] = 1
            receipt_data.append(items)
        self.Update_receipt()

 
    # Right side frame
    def Right_frame(self):
        self.right_frame = tk.Frame(self.top_frame, bg="lightgray", width=100)#lightgray
        self.right_frame.pack(side='right', expand=True, fill='both')
        self.right_frame.pack_propagate(False)

        #make receipt
        self.receipt_frame = tk.Frame(self.right_frame, background='white')
        self.receipt_frame.pack(expand=True, fill='both', padx=8, pady=10)

        receipt_label = ttk.Label(self.receipt_frame,
                                  text="🧾 Receipt",
                                  font=("Ubuntu",14, "bold"),
                                  background='white')
        receipt_label.pack(pady=10)

        self.receipt_box = tk.Text(self.receipt_frame,
                              height=20,
                              font=("Consolas", 10),
                              bg="#dad7c5",
                              fg="black",
                              insertbackground="black",
                              border=2)

        self.receipt_box.pack(padx=10, pady=10)
        self.receipt_box.insert(tk.END,'ITEM       QTY       PRICE \n...........................\n')


    # Bottom form frame
    def Bottom_frame(self):
        bottom_frame = tk.Frame(self, bg="lightgray", height=100)
        bottom_frame.pack(side='bottom', fill='x')

        self.name_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        self.image_var = tk.StringVar()

        # Add form widgets to bottom frame
        ttk.Label(bottom_frame, text="Name:").pack(side="left", padx=5, pady=10)
        ttk.Entry(bottom_frame, textvariable=self.name_var, width=10).pack(side="left", padx=5)

        ttk.Label(bottom_frame, text="Price:").pack(side="left", padx=5)
        ttk.Entry(bottom_frame, textvariable=self.price_var, width=5).pack(side="left", padx=5)

        ttk.Label(bottom_frame, text="Qty:").pack(side="left", padx=5)
        ttk.Entry(bottom_frame, textvariable=self.qty_var, width=5).pack(side="left", padx=5)

        ttk.Label(bottom_frame, text="Image:").pack(side="left", padx=5)
        ttk.Entry(bottom_frame, textvariable=self.image_var, width=15).pack(side="left", padx=5)

        ttk.Button(bottom_frame, text='➕ Add',style='Cart.TButton', command=self.Add).pack(side='left', padx=5)

    def Add(self):
        try:
            # Get form inputs
            name = self.name_var.get() or 'product'
            price = int(self.price_var.get())
            qty = int(self.qty_var.get())
            image = self.image_var.get()+'.png' or None

            # Insert the new item at the beginning of the list
            Add_item.insert(0, [name, price, qty, image])

            # Recalculate height
            self.HeightOfItems = len(Add_item) * self.Height
            self.canvas.config(scrollregion=(0, 0, 200, self.HeightOfItems))
            self.canvas.itemconfig(self.canvas_window, height=self.HeightOfItems)

            # Clear old widgets
            for widget in display_items.winfo_children():
                widget.destroy()

            # Re-render all items in new order
            for item in Add_item:
                self.PlaceItem(item).pack(expand=True, fill='both', padx=6, pady=4)

            # Scroll to top so user sees new item
            self.canvas.yview_moveto(0.0)

            # Clear form
            self.name_var.set("")
            self.price_var.set("")
            self.qty_var.set("")
            self.image_var.set("")
        except ValueError:
            print('Invalid price or quantity')


# Main app 
root = tk.Tk()
root.title('POS App')
root.geometry('620x500')
root.resizable(False, False)

receipt_data = []
total_amount = 0

style = ttk.Style()
style.configure('Cart.TButton', font=('Arial', 10), background='orange', foreground='black')

Add_item = [['Mango', 20, 10, 'mango.png'],
            ['Pineapple', 200, 10, 'pineapple.png'],
            ['Apple', 200, 11, 'apple.png'],
            ['berry', 400, 11, 'blackberry.png'],
            ['lemon', 40, 30, 'lemon.png']]

frame = MainFrame(root, Add_item, 122)
root.mainloop()
