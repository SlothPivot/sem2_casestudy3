import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import json
import urllib.request
import loginPage
import databaseConnector as db

class mainApplication:
    def __init__(self, master):
        self.master = master
        self.master.geometry("700x500")
        self.master.title("Control panel")

        self.tabs = ttk.Notebook(self.master)
        # self.tabs.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NSEW')
        self.tabs.place(x=0, y=10)

        # self.tabInventory = Inventory(self.master)        #no time
        # self.tabs.add(self.tabInventory, text="Inventory")

        self.tabNewPost = AddNewPost(self.master)
        self.tabs.add(self.tabNewPost, text="Add new post")

        # self.tabSensorInfo = SensorInfo(self.master)
        # self.tabs.add(self.tabSensorInfo, text="Sensor Information")


# class Inventory(tk.Frame):
#     def __init__(self, master):
#         super(Inventory, self).__init__(master)
#         self.listOfFrames = []
        
#         backgroundColor = "red"
#         fontForInv = font.Font(size=12)
#         for i in range(1, 4):
#             self.listOfFrames.append(tk.(self, text="a"))
#             self.listOfFrames[-1].grid(row=i,column=0)
#         self.config(bg=backgroundColor)

# class SinglePost(tk.Frame):
#     def __init__(self, master):
#         super(SinglePost, self).__init__(Inventory)

#         self.label


class AddNewPost(tk.Frame):
    """add new post tab"""
    def __init__(self, master):
        super(AddNewPost, self).__init__(master)
        backgroundColor = '#d7d7d9'

        OPTIONS = ["","Boards", "PC", "Parts"]
        CONDITION = ["","Brand New", "Refurbished", "Used"]
        
        self.name = tk.StringVar(self)
        self.model = tk.StringVar(self)
        self.category = tk.StringVar(self)
        self.category.set(OPTIONS[0])
        self.condition = tk.StringVar(self)
        self.condition.set(CONDITION[0])
        self.price = tk.StringVar(self)
        self.description = tk.StringVar(self)

        self.config(bg=backgroundColor, width=700, height=500)
        self.grid_propagate(0)

        fontForNewPost = font.Font(size=15)

        self.entryName = tk.Entry(self, textvariable=self.name)    
        self.entryModel = tk.Entry(self, textvariable=self.model)
        self.optMenuCategory = ttk.OptionMenu(self, self.category, *OPTIONS)
        self.optMenuCondition = ttk.OptionMenu(self, self.condition, *CONDITION)
        self.entrydescription = tk.Text(self, width=50, height=15)
        self.entryPrice = tk.Entry(self, textvariable=self.price)
        
        padxEntry=(0, 10)
        self.entryName.grid(row=0,column=1, ipadx=50, pady=(30, 0), sticky='EW', padx=padxEntry)
        self.entryModel.grid(row=1,column=1, sticky='EW', padx=padxEntry)
        self.optMenuCategory.grid(row=2,column=1, sticky='EW', padx=padxEntry)
        self.optMenuCondition.grid(row=3,column=1, sticky='EW', padx=padxEntry)
        self.entryPrice.grid(row=4, column=1,sticky='EW',padx=padxEntry)
        self.entrydescription.grid(row=5,column=1, pady=(0, 10), padx=padxEntry)


        self.lblName = tk.Label(self, text="Name:", bg=backgroundColor, font=fontForNewPost)
        self.lblModel = tk.Label(self, text="Model:", bg=backgroundColor, font=fontForNewPost)
        self.lblCategory = tk.Label(self, text="Category:", bg=backgroundColor, font=fontForNewPost)
        self.lblCondition = tk.Label(self, text="Condition:", bg=backgroundColor, font=fontForNewPost)
        self.lblDescription = tk.Label(self, text="Description:", bg=backgroundColor, font=fontForNewPost)
        self.lblPrice = tk.Label(self, text="Price:", bg=backgroundColor, font=fontForNewPost)
        self.lblRequiredField1 = tk.Label(self, text="<--- REQUIRED FIELD", bg=backgroundColor, fg="red")
        self.lblRequiredField2 = tk.Label(self, text="<--- REQUIRED FIELD", bg=backgroundColor, fg="red")
        self.lblRequiredField3 = tk.Label(self, text="<--- REQUIRED FIELD", bg=backgroundColor, fg="red")
        self.lblRequiredField4 = tk.Label(self, text="<--- REQUIRED FIELD", bg=backgroundColor, fg="red")
        self.lblRequiredField5 = tk.Label(self, text="<--- REQUIRED FIELD", bg=backgroundColor, fg="red")
        self.lblWrongData = tk.Label(self, text="<--- INPUT NUMBER", bg=backgroundColor, fg="red")



        self.lblName.grid(row=0,column=0, sticky="E", padx=(75,0), pady=(30, 0))
        self.lblModel.grid(row=1,column=0, sticky="E")
        self.lblCategory.grid(row=2,column=0, sticky="E")
        self.lblCondition.grid(row=3,column=0, sticky="E")
        self.lblPrice.grid(row=4,column=0,sticky="E")
        self.lblDescription.grid(row=5,column=0, sticky="E")

        self.btnAdd = tk.Button(self, text="Add", width=15, command=self.addNewPostBtn)
        
        self.btnAdd.grid(row=6, column=1, pady=(0,20))


        
    def addNewPostBtn(self):
        flagEverythingFilled = True
        if self.name.get().strip() == '':
            self.lblRequiredField1.grid(row=0,column=2,sticky="W",pady=(30, 0), padx=(0, 50 ))
            flagEverythingFilled = False
        if self.model.get().strip() == '':
            self.lblRequiredField2.grid(row=1,column=2,sticky="W")
            flagEverythingFilled = False
        if self.category.get().strip() == '':
            self.lblRequiredField3.grid(row=2,column=2,sticky="W")
            flagEverythingFilled = False
        if self.condition.get().strip() == '':
            self.lblRequiredField4.grid(row=3,column=2,sticky="W")
            flagEverythingFilled = False
        if self.price.get().strip == '':
            self.lblRequiredField5.grid(row=4,column=2,sticky="W")
            flagEverythingFilled = False
        try:
            float(self.price.get())
            self.lblWrongData.grid_forget()
        except:
            self.lblWrongData.grid(row=4,column=2,sticky="W")
            flagEverythingFilled = False

        if flagEverythingFilled:
            enteredName = str(self.name.get()).strip()
            enteredModel = str(self.model.get()).strip()
            enteredCategory = str(self.category.get())
            enteredCondition = str(self.condition.get())
            enteredDesc = str(self.entrydescription.get("1.0", "end")).strip()
            db.insertItemIntoInventory(enteredName, enteredModel, enteredCategory, enteredCondition, enteredDesc)




class SensorInfo(tk.Frame):
    def __init__(self, master):
        super(SensorInfo, self).__init__(master)

        self.urlDHT11 = 'http://82.161.206.227:5000/dht11'
        self.urlLdr = 'http://82.161.206.227:5000/ldr'
        self.readDataDHT = urllib.request.urlopen(self.urlDHT11).read().decode()
        self.readLdr = urllib.request.urlopen(self.urlLdr).read().decode()
        try:
            self.humidity = json.loads(self.readDataDHT)['humidity']
            self.temperature = json.loads(self.readDataDHT)['temperature']
            self.ldr = json.loads(self.readLdr)['count']
        except:
            pass

        backgroundColor = "#d7d7d9"
        fontForLabel = font.Font(size=15)

        self.config(bg=backgroundColor)

        self.labelSensInfo = tk.Label(self, text = "Sensor Information", bg=backgroundColor, font=fontForLabel)
        self.labelTemp = tk.Label(self, text = "Temperature: " + str(self.temperature) + u"\N{DEGREE SIGN}C", bg=backgroundColor, font=fontForLabel)
        self.labelLight = tk.Label(self, text = "Light: " + str(self.ldr), bg=backgroundColor, font=fontForLabel)
        self.labelHumidity = tk.Label(self, text = "Humidity: " + str(self.humidity) + "%", bg=backgroundColor, font=fontForLabel)
        
        self.padx = (50, 0)
        self.labelSensInfo.grid(row=0, column=2, columnspan=4, padx=(50,300))
        self.labelTemp.grid(row=2, column=1, sticky='W', padx=self.padx, pady=(100, 0))
        self.labelLight.grid(row=3, column=1, sticky='W', pady=(0, 0), padx=self.padx)
        self.labelHumidity.grid(row=4, column=1, sticky='W', padx=self.padx)

        self.refreshHumidityLabel()
        self.refreshLightLabel()
        self.refreshTempLabel()


    def refreshTempLabel(self):
        try:
            self.readDataDHT = urllib.request.urlopen(self.urlDHT11).read().decode()
            self.temperature = str(json.loads(self.readDataDHT)['temperature'])
        except:
            pass
        self.labelTemp.configure(text = "Temperature: " + str(self.temperature) + u"\N{DEGREE SIGN}C")
        self.labelTemp.after(3000, self.refreshTempLabel)
        

    def refreshLightLabel(self):
        try:
            self.readLdr = urllib.request.urlopen(self.urlLdr).read().decode()
            self.ldr = json.loads(self.readLdr)['count']
        except:
            pass
        if self.ldr <= 2000:
            self.labelLight.configure(text = "Light: " + str(self.ldr) + " (Very bright, please check)")
        elif self.ldr > 2000 and self.ldr < 9000:
            self.labelLight.configure(text = "Light: " + str(self.ldr) + " (Average, no checking required)")
        elif self.ldr >= 9000:
            self.labelLight.configure(text = "Light: " + str(self.ldr) + " (Very dark, please check)")
        self.labelLight.after(3000, self.refreshLightLabel)

    def refreshHumidityLabel(self):
        try:
            self.readDataDHT = urllib.request.urlopen(self.urlDHT11).read().decode()
            self.humidity = str(json.loads(self.readDataDHT)['humidity'])
        except:
            pass
        self.labelHumidity.configure(text = "Humidity: " + str(self.humidity) + "%")
        self.labelHumidity.after(3000, self.refreshHumidityLabel)




def mainApp():
    root = tk.Tk()
    mainApplication(root)
    root.mainloop()

if __name__ == '__main__':
    if loginPage.loginMe():
        mainApp()
