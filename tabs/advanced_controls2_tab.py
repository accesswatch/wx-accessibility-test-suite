"""
Advanced Controls Tab 2
========================
Tests for spin control double, AUI notebook, and other specialized controls.
"""

import wx
import wx.aui
from state_manager import TabStateHelper


class AdvancedControls2Tab(wx.Panel, TabStateHelper):
    """Tab containing SpinCtrlDouble, AuiNotebook, and specialized controls."""
    
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Advanced Controls 2"
        
        scroll = wx.ScrolledWindow(self, style=wx.VSCROLL)
        scroll.SetScrollRate(0, 20)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add control groups
        main_sizer.Add(self._create_spinctrldouble_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_aui_notebook_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        
        scroll.SetSizer(main_sizer)
        
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(scroll, 1, wx.EXPAND)
        self.SetSizer(panel_sizer)
        
    def GetName(self):
        return self.tab_name
        
    def _create_spinctrldouble_group(self, parent):
        """Create SpinCtrlDouble control group."""
        box = wx.StaticBox(parent, label="Spin Control Double (Arrow keys, type value)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="Spin controls for decimal/floating-point values:"
            ),
            0, wx.ALL, 5
        )
        
        # Price spinner (2 decimals)
        sizer.Add(wx.StaticText(parent, label="&Price ($):"), 0, wx.ALL, 5)
        
        self.price_spin = wx.SpinCtrlDouble(
            parent,
            value="19.99",
            min=0.00,
            max=999.99,
            initial=19.99,
            inc=0.50
        )
        self.price_spin.SetDigits(2)
        self.price_spin.SetToolTip("Arrow keys to adjust by $0.50, type exact value")
        self.price_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_spin_double)
        self.price_spin.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.price_spin, 0, wx.ALL | wx.EXPAND, 5)
        
        # Percentage spinner (1 decimal)
        sizer.Add(wx.StaticText(parent, label="&Percentage (%):"), 0, wx.ALL, 5)
        
        self.percent_spin = wx.SpinCtrlDouble(
            parent,
            value="75.5",
            min=0.0,
            max=100.0,
            initial=75.5,
            inc=0.1
        )
        self.percent_spin.SetDigits(1)
        self.percent_spin.SetToolTip("Arrow keys to adjust by 0.1%, type exact value")
        self.percent_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_spin_double)
        self.percent_spin.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.percent_spin, 0, wx.ALL | wx.EXPAND, 5)
        
        # Temperature spinner (1 decimal)
        sizer.Add(wx.StaticText(parent, label="&Temperature (°C):"), 0, wx.ALL, 5)
        
        self.temp_spin = wx.SpinCtrlDouble(
            parent,
            value="20.5",
            min=-50.0,
            max=50.0,
            initial=20.5,
            inc=0.5
        )
        self.temp_spin.SetDigits(1)
        self.temp_spin.SetToolTip("Arrow keys to adjust by 0.5°C, type exact value")
        self.temp_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_spin_double)
        self.temp_spin.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.temp_spin, 0, wx.ALL | wx.EXPAND, 5)
        
        # Display
        self.spin_double_label = wx.StaticText(parent, label="Adjust spinners to see values")
        sizer.Add(self.spin_double_label, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_aui_notebook_group(self, parent):
        """Create AUI Notebook control group."""
        box = wx.StaticBox(parent, label="AUI Notebook (Ctrl+Tab, Ctrl+Shift+Tab, drag tabs)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="Advanced UI notebook with tab management features:"
            ),
            0, wx.ALL, 5
        )
        
        # Create AUI Notebook
        self.aui_notebook = wx.aui.AuiNotebook(
            parent,
            style=wx.aui.AUI_NB_TOP |
                  wx.aui.AUI_NB_TAB_SPLIT |
                  wx.aui.AUI_NB_TAB_MOVE |
                  wx.aui.AUI_NB_SCROLL_BUTTONS |
                  wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB |
                  wx.aui.AUI_NB_MIDDLE_CLICK_CLOSE
        )
        
        # Add sample pages
        for i in range(5):
            page = self._create_aui_page(self.aui_notebook, i + 1)
            self.aui_notebook.AddPage(
                page,
                f"Document {i + 1}",
                select=(i == 0)
            )
            
        self.aui_notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_aui_page_changed)
        self.aui_notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_aui_page_close)
        self.aui_notebook.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        sizer.Add(self.aui_notebook, 1, wx.ALL | wx.EXPAND, 5)
        
        # Tab management buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.add_tab_btn = wx.Button(parent, label="&Add Tab")
        self.add_tab_btn.Bind(wx.EVT_BUTTON, self.on_add_aui_tab)
        self.add_tab_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.add_tab_btn, 0, wx.ALL, 5)
        
        self.remove_tab_btn = wx.Button(parent, label="&Remove Current Tab")
        self.remove_tab_btn.Bind(wx.EVT_BUTTON, self.on_remove_aui_tab)
        self.remove_tab_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.remove_tab_btn, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALL, 5)
        
        # Info label
        self.aui_label = wx.StaticText(
            parent,
            label="Use Ctrl+Tab/Ctrl+Shift+Tab to switch tabs, drag to reorder, click X to close"
        )
        sizer.Add(self.aui_label, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_aui_page(self, parent, page_num):
        """Create a sample AUI notebook page."""
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Page title
        title = wx.StaticText(
            panel,
            label=f"Document {page_num}",
            style=wx.ALIGN_CENTER
        )
        title_font = title.GetFont()
        title_font.SetPointSize(title_font.GetPointSize() + 4)
        title_font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        sizer.Add(title, 0, wx.ALL | wx.EXPAND, 10)
        
        # Sample content
        content = wx.TextCtrl(
            panel,
            value=f"This is the content area for Document {page_num}.\n\n"
                  f"You can add any controls here. This demonstrates how AUI Notebook\n"
                  f"manages multiple document pages with advanced features like:\n\n"
                  f"- Tab dragging to reorder\n"
                  f"- Close buttons on tabs\n"
                  f"- Keyboard navigation (Ctrl+Tab)\n"
                  f"- Multiple tab rows if needed\n\n"
                  f"Screen readers should announce tab position and count.",
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP
        )
        sizer.Add(content, 1, wx.ALL | wx.EXPAND, 10)
        
        # Checkbox for testing
        checkbox = wx.CheckBox(panel, label=f"Enable feature for Document {page_num}")
        sizer.Add(checkbox, 0, wx.ALL, 10)
        
        panel.SetSizer(sizer)
        return panel
        
    # Event handlers
    def on_spin_double(self, event):
        """Handle SpinCtrlDouble change."""
        ctrl = event.GetEventObject()
        value = ctrl.GetValue()
        
        if ctrl == self.price_spin:
            label = "Price"
            unit = "$"
        elif ctrl == self.percent_spin:
            label = "Percentage"
            unit = "%"
        else:  # temp_spin
            label = "Temperature"
            unit = "°C"
            
        self.spin_double_label.SetLabel(f"{label} changed to: {value}{unit}")
        self.main_frame.update_status_bar(
            f"{label} spinner",
            f"Value: {value}{unit}",
            "Arrow keys to adjust, type exact value"
        )
        
    def on_aui_page_changed(self, event):
        """Handle AUI notebook page change."""
        selection = self.aui_notebook.GetSelection()
        if selection != wx.NOT_FOUND:
            page_text = self.aui_notebook.GetPageText(selection)
            page_count = self.aui_notebook.GetPageCount()
            
            self.aui_label.SetLabel(
                f"Selected: {page_text} (tab {selection + 1} of {page_count})"
            )
            self.main_frame.update_status_bar(
                f"AUI Notebook: {page_text}",
                f"Tab {selection + 1} of {page_count}",
                "Ctrl+Tab to switch, drag to reorder"
            )
        event.Skip()
        
    def on_aui_page_close(self, event):
        """Handle AUI notebook page close."""
        selection = event.GetSelection()
        page_text = self.aui_notebook.GetPageText(selection)
        
        if self.aui_notebook.GetPageCount() <= 1:
            wx.MessageBox(
                "Cannot close the last tab.",
                "Cannot Close",
                wx.OK | wx.ICON_INFORMATION
            )
            event.Veto()
        else:
            self.aui_label.SetLabel(f"Closed tab: {page_text}")
            
    def on_add_aui_tab(self, event):
        """Add a new AUI notebook tab."""
        page_count = self.aui_notebook.GetPageCount()
        new_page_num = page_count + 1
        
        page = self._create_aui_page(self.aui_notebook, new_page_num)
        self.aui_notebook.AddPage(page, f"Document {new_page_num}", select=True)
        
        self.aui_label.SetLabel(f"Added Document {new_page_num}")
        
    def on_remove_aui_tab(self, event):
        """Remove current AUI notebook tab."""
        selection = self.aui_notebook.GetSelection()
        
        if selection != wx.NOT_FOUND:
            if self.aui_notebook.GetPageCount() <= 1:
                wx.MessageBox(
                    "Cannot close the last tab.",
                    "Cannot Close",
                    wx.OK | wx.ICON_INFORMATION
                )
            else:
                page_text = self.aui_notebook.GetPageText(selection)
                self.aui_notebook.DeletePage(selection)
                self.aui_label.SetLabel(f"Removed tab: {page_text}")
                
    def on_control_focus(self, event):
        """Handle focus events."""
        ctrl = event.GetEventObject()
        
        if isinstance(ctrl, wx.SpinCtrlDouble):
            value = ctrl.GetValue()
            min_val = ctrl.GetMin()
            max_val = ctrl.GetMax()
            
            if ctrl == self.price_spin:
                label = "Price spinner"
                unit = "$"
            elif ctrl == self.percent_spin:
                label = "Percentage spinner"
                unit = "%"
            else:
                label = "Temperature spinner"
                unit = "°C"
                
            self.main_frame.update_status_bar(
                label,
                f"Role: Spin control, Value: {value}{unit}, Range: {min_val}-{max_val}",
                "Arrow keys to adjust, type exact value"
            )
        elif isinstance(ctrl, wx.aui.AuiNotebook):
            selection = ctrl.GetSelection()
            if selection != wx.NOT_FOUND:
                page_text = ctrl.GetPageText(selection)
                page_count = ctrl.GetPageCount()
                self.main_frame.update_status_bar(
                    f"AUI Notebook: {page_text}",
                    f"Role: Tab control, Tab {selection + 1} of {page_count}",
                    "Ctrl+Tab to switch, drag to reorder"
                )
        elif isinstance(ctrl, wx.Button):
            label = ctrl.GetLabel()
            self.main_frame.update_status_bar(
                f"Button: {label}",
                "Role: Button",
                "Space to activate"
            )
            
        event.Skip()
        
    # State management
    def save_state(self):
        """Save tab state."""
        aui_tabs = []
        for i in range(self.aui_notebook.GetPageCount()):
            aui_tabs.append(self.aui_notebook.GetPageText(i))
            
        return {
            "price": self.price_spin.GetValue(),
            "percent": self.percent_spin.GetValue(),
            "temperature": self.temp_spin.GetValue(),
            "aui_selection": self.aui_notebook.GetSelection(),
            "aui_tabs": aui_tabs
        }
        
    def load_state(self, state):
        """Load tab state."""
        if "price" in state:
            self.price_spin.SetValue(state["price"])
            
        if "percent" in state:
            self.percent_spin.SetValue(state["percent"])
            
        if "temperature" in state:
            self.temp_spin.SetValue(state["temperature"])
            
        if "aui_tabs" in state:
            # Remove all existing pages
            while self.aui_notebook.GetPageCount() > 0:
                self.aui_notebook.DeletePage(0)
                
            # Add saved tabs
            for i, tab_name in enumerate(state["aui_tabs"]):
                page = self._create_aui_page(self.aui_notebook, i + 1)
                self.aui_notebook.AddPage(page, tab_name, select=False)
                
        if "aui_selection" in state and state["aui_selection"] != wx.NOT_FOUND:
            if state["aui_selection"] < self.aui_notebook.GetPageCount():
                self.aui_notebook.SetSelection(state["aui_selection"])
                
    def reset_to_defaults(self):
        """Reset to defaults."""
        self.price_spin.SetValue(19.99)
        self.percent_spin.SetValue(75.5)
        self.temp_spin.SetValue(20.5)
        
        # Reset AUI notebook to 5 tabs
        while self.aui_notebook.GetPageCount() > 0:
            self.aui_notebook.DeletePage(0)
            
        for i in range(5):
            page = self._create_aui_page(self.aui_notebook, i + 1)
            self.aui_notebook.AddPage(page, f"Document {i + 1}", select=(i == 0))
            
        self.spin_double_label.SetLabel("Adjust spinners to see values")
        self.aui_label.SetLabel("Use Ctrl+Tab/Ctrl+Shift+Tab to switch tabs, drag to reorder, click X to close")
