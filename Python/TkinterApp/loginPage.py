import tkinter as tk
import passHash as ph
import databaseConnector as db

class LoginFrame:

    def __init__(self, master):
        self.master = master
        self.master.geometry("250x200")
        self.master.title("Login")
        self.master.resizable(False, False)

        password = tk.StringVar()
        username = tk.StringVar()
        self.correctPass = False

        self.loginFrame = tk.Frame(self.master)
        self.button1 = tk.Button(self.loginFrame, text = 'Login', width = 15, command = lambda: self.validateLogin(username, password))
        self.usernameEntry = tk.Entry(self.loginFrame, textvariable = username)
        self.passwordEntry = tk.Entry(self.loginFrame, show = "\u2022", textvariable = password) #bullet character
        self.labelUsername = tk.Label(self.loginFrame, text = "Username")
        self.labelPassword = tk.Label(self.loginFrame, text = "Password")
        self.labelInvalidCredentials = tk.Label(self.loginFrame, text="Invalid credentials", fg="red")

        self.labelUsername.grid(row = 0, column = 0)
        self.usernameEntry.grid(row = 0, column = 1)
        self.labelPassword.grid(row = 1, column = 0)
        self.passwordEntry.grid(row = 1, column = 1)
        self.button1.grid(row = 2, column = 0, columnspan = 2)
        self.loginFrame.place(x=30, y=50)


    def validateLogin(self, username, password):
        usernameToCheck = str(username.get())
        passwordToCheck = str(password.get())
        try:
            checkStr = db.readCreds(usernameToCheck)
            if ph.verify_password(checkStr[1], passwordToCheck):
                self.master.destroy()           #closes the window
                self.correctPass = True
            else:
                self.labelInvalidCredentials.grid(row=3, column=0, columnspan=2)#Invalid credentials
        except:
            self.labelInvalidCredentials.grid(row=3, column=0, columnspan=2) #invalid credentials



def loginMe(): 
    root = tk.Tk()
    app = LoginFrame(root)
    root.mainloop()
    return app.correctPass


if __name__ == '__main__':
    loginMe()