import tkinter as tk
from tkinter import ttk


class Dialog(tk.Toplevel):

    def __init__(self, parent, title=None, label_text=None):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        if label_text:
            self.label_text = label_text
        self.parent = parent
        self.result = None
        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx() - 200,
                                  parent.winfo_rooty() - 50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = tk.Frame(self)
        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    # command hooks
    def validate(self):
        return 1  # override

    def apply(self):
        pass  # override


class MyEntryWindow(Dialog):
    def body(self, master):
        self.grid()
        self.wm_title("TSCa File Copy Data Entry")
        master.grid()
        self.label1 = ttk.Label(master, text="Enter run identifier")
        self.label1.grid(column=0, row=0)
        self.e1 = ttk.Entry(master)
        self.e1.grid(column=1, row=0, pady=10)
        return self.e1

    def apply(self):
        self.run_id = self.e1.get()

    def entry_button_callback(self, event):
        self.destroy()


class MyInformationWindow(Dialog):

    def body(self, master):
        self.grid()
        self.wm_title("TSCa File Copy Information")
        self.label = ttk.Label(master, text=self.label_text)
        self.label.grid(column=0, row=0)
