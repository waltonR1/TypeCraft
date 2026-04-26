import tkinter as tk
from tkinter import ttk

class BaseTab(ttk.Frame):
    def __init__(self, notebook, title, app_ui):
        super().__init__(notebook, padding=15)
        self.notebook = notebook
        self.app_ui = app_ui # Reference to the main UI class
        self.notebook.add(self, text=f" {title} ")
        self._build()

    def _build(self):
        """Override in subclasses"""
        pass
