"""
Advanced Controls Tab
=====================
Tests for Tier 2 controls: ToggleButton, BitmapButton, Pickers, Spinners/Sliders,
Progress indicators, and Containers.
"""

import wx
import wx.adv
from state_manager import TabStateHelper
from test_data import get_color_names, DEPARTMENTS


class AdvancedControlsTab(wx.Panel, TabStateHelper):
    """Tab containing advanced/Tier 2 controls for accessibility testing."""
    
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Advanced Controls"
        
        # Create scrolled window
        scroll = wx.ScrolledWindow(self, style=wx.VSCROLL)
        scroll.SetScrollRate(0, 20)
        
        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add control groups
        main_sizer.Add(self._create_toggle_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_picker_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_spin_slider_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_progress_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_container_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        
        scroll.SetSizer(main_sizer)
        
        # Layout
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(scroll, 1, wx.EXPAND)
        self.SetSizer(panel_sizer)
        
    def GetName(self):
        return self.tab_name
        
    def _create_toggle_group(self, parent):
        """Create toggle button group."""
        box = wx.StaticBox(parent, label="Toggle Buttons (Space to toggle)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        self.toggle1 = wx.ToggleButton(parent, label="&Bold")
        self.toggle1.SetValue(False)
        self.toggle1.SetToolTip("Toggle button - Space to toggle state")
        self.toggle1.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle)
        self.toggle1.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.toggle1, 0, wx.ALL, 5)
        
        self.toggle2 = wx.ToggleButton(parent, label="&Italic")
        self.toggle2.SetValue(True)
        self.toggle2.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle)
        self.toggle2.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.toggle2, 0, wx.ALL, 5)
        
        self.toggle3 = wx.ToggleButton(parent, label="&Underline")
        self.toggle3.SetValue(False)
        self.toggle3.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle)
        self.toggle3.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.toggle3, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_picker_group(self, parent):
        """Create picker controls group."""
        box = wx.StaticBox(parent, label="Picker Controls (Space/Enter to open)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Date picker
        sizer.Add(wx.StaticText(parent, label="&Date Picker:"), 0, wx.ALL, 5)
        self.date_picker = wx.adv.DatePickerCtrl(parent, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.date_picker.SetToolTip("Date picker - Alt+Down to open calendar, Arrow keys to navigate")
        self.date_picker.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.date_picker, 0, wx.ALL | wx.EXPAND, 5)
        
        # Color picker
        sizer.Add(wx.StaticText(parent, label="&Color Picker:"), 0, wx.ALL, 5)
        self.color_picker = wx.ColourPickerCtrl(parent)
        self.color_picker.SetToolTip("Color picker - Space/Enter to open dialog")
        self.color_picker.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.color_picker, 0, wx.ALL | wx.EXPAND, 5)
        
        # File picker
        sizer.Add(wx.StaticText(parent, label="&File Picker:"), 0, wx.ALL, 5)
        self.file_picker = wx.FilePickerCtrl(
            parent,
            message="Select a file",
            wildcard="All files (*.*)|*.*"
        )
        self.file_picker.SetToolTip("File picker - Space/Enter to open file dialog")
        self.file_picker.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.file_picker, 0, wx.ALL | wx.EXPAND, 5)
        
        return sizer
        
    def _create_spin_slider_group(self, parent):
        """Create spin/slider controls group."""
        box = wx.StaticBox(parent, label="Spin & Slider Controls (Arrow keys to adjust)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # SpinCtrl
        sizer.Add(wx.StaticText(parent, label="&Spin Control (0-100):"), 0, wx.ALL, 5)
        self.spin = wx.SpinCtrl(parent, value="50", min=0, max=100)
        self.spin.SetToolTip("Spin control - Arrow keys or type value")
        self.spin.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin_change)
        sizer.Add(self.spin, 0, wx.ALL | wx.EXPAND, 5)
        
        # Slider
        sizer.Add(wx.StaticText(parent, label="&Slider (0-100):"), 0, wx.ALL, 5)
        self.slider = wx.Slider(
            parent,
            value=50,
            minValue=0,
            maxValue=100,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.slider.SetToolTip("Slider - Arrow keys to adjust, Page Up/Down for larger steps")
        self.slider.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        self.slider.Bind(wx.EVT_SLIDER, self.on_slider_change)
        sizer.Add(self.slider, 0, wx.ALL | wx.EXPAND, 5)
        
        return sizer
        
    def _create_progress_group(self, parent):
        """Create progress indicator group."""
        box = wx.StaticBox(parent, label="Progress Indicators")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Gauge
        sizer.Add(wx.StaticText(parent, label="Progress bar (45%):"), 0, wx.ALL, 5)
        self.gauge = wx.Gauge(parent, range=100)
        self.gauge.SetValue(45)
        self.gauge.SetToolTip("Progress gauge at 45%")
        sizer.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 5)
        
        # Buttons to control gauge
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        inc_btn = wx.Button(parent, label="+10%")
        inc_btn.Bind(wx.EVT_BUTTON, lambda e: self._update_gauge(10))
        btn_sizer.Add(inc_btn, 0, wx.ALL, 5)
        
        dec_btn = wx.Button(parent, label="-10%")
        dec_btn.Bind(wx.EVT_BUTTON, lambda e: self._update_gauge(-10))
        btn_sizer.Add(dec_btn, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_container_group(self, parent):
        """Create container controls group."""
        box = wx.StaticBox(parent, label="Container Controls")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # CollapsiblePane
        self.collapsible = wx.CollapsiblePane(parent, label="&Expandable Section (Space to toggle)")
        self.collapsible.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_collapse_change)
        
        pane = self.collapsible.GetPane()
        pane_sizer = wx.BoxSizer(wx.VERTICAL)
        pane_sizer.Add(
            wx.StaticText(pane, label="This content is inside a collapsible pane."),
            0, wx.ALL, 5
        )
        pane_sizer.Add(
            wx.TextCtrl(pane, value="Sample text inside collapsible pane"),
            0, wx.ALL | wx.EXPAND, 5
        )
        pane.SetSizer(pane_sizer)
        
        sizer.Add(self.collapsible, 0, wx.ALL | wx.EXPAND, 5)
        
        # StaticBox with grouped controls
        group_box = wx.StaticBox(parent, label="Grouped Controls")
        group_sizer = wx.StaticBoxSizer(group_box, wx.VERTICAL)
        
        cb1 = wx.CheckBox(parent, label="Option &1")
        cb1.SetValue(True)
        group_sizer.Add(cb1, 0, wx.ALL, 5)
        
        cb2 = wx.CheckBox(parent, label="Option &2")
        group_sizer.Add(cb2, 0, wx.ALL, 5)
        
        sizer.Add(group_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        return sizer
        
    def _update_gauge(self, delta):
        """Update gauge value."""
        new_val = max(0, min(100, self.gauge.GetValue() + delta))
        self.gauge.SetValue(new_val)
        self.main_frame.update_status_bar(
            f"Progress updated: {new_val}%",
            "",
            ""
        )
        
    # Event handlers
    def on_toggle(self, event):
        """Handle toggle button events."""
        btn = event.GetEventObject()
        state = "Pressed" if btn.GetValue() else "Not pressed"
        
        self.main_frame.update_status_bar(
            f"Toggle button: {btn.GetLabel()}",
            f"State: {state}",
            "Space to toggle"
        )
        
    def on_spin_change(self, event):
        """Handle spin control changes."""
        value = self.spin.GetValue()
        self.main_frame.update_status_bar(
            "Spin control",
            f"Value: {value}",
            "Arrow keys or type to change"
        )
        
    def on_slider_change(self, event):
        """Handle slider changes."""
        value = self.slider.GetValue()
        self.main_frame.update_status_bar(
            "Slider",
            f"Value: {value}",
            "Arrow keys to adjust"
        )
        
    def on_collapse_change(self, event):
        """Handle collapsible pane changes."""
        collapsed = self.collapsible.IsCollapsed()
        state = "Collapsed" if collapsed else "Expanded"
        
        self.main_frame.update_status_bar(
            "Collapsible pane",
            f"State: {state}",
            "Space to toggle"
        )
        
    def on_control_focus(self, event):
        """Handle focus events."""
        ctrl = event.GetEventObject()
        
        if isinstance(ctrl, wx.ToggleButton):
            state = "Pressed" if ctrl.GetValue() else "Not pressed"
            self.main_frame.update_status_bar(
                f"Toggle button: {ctrl.GetLabel()}",
                f"Role: Toggle button, State: {state}",
                "Space to toggle"
            )
        elif isinstance(ctrl, wx.adv.DatePickerCtrl):
            date = ctrl.GetValue()
            self.main_frame.update_status_bar(
                "Date picker",
                f"Role: Date picker, Value: {date.FormatISODate()}",
                "Alt+Down to open, Arrow keys to navigate"
            )
        elif isinstance(ctrl, wx.ColourPickerCtrl):
            color = ctrl.GetColour()
            self.main_frame.update_status_bar(
                "Color picker",
                f"Role: Color picker, RGB: ({color.Red()}, {color.Green()}, {color.Blue()})",
                "Space/Enter to open dialog"
            )
        elif isinstance(ctrl, wx.FilePickerCtrl):
            path = ctrl.GetPath()
            self.main_frame.update_status_bar(
                "File picker",
                f"Role: File picker, Path: {path if path else '(none)'}",
                "Space/Enter to browse"
            )
        elif isinstance(ctrl, wx.SpinCtrl):
            self.main_frame.update_status_bar(
                "Spin control",
                f"Role: Spin button, Value: {ctrl.GetValue()}, Range: {ctrl.GetMin()}-{ctrl.GetMax()}",
                "Arrow keys or type value"
            )
        elif isinstance(ctrl, wx.Slider):
            self.main_frame.update_status_bar(
                "Slider",
                f"Role: Slider, Value: {ctrl.GetValue()}, Range: {ctrl.GetMin()}-{ctrl.GetMax()}",
                "Arrow keys, Page Up/Down, Home/End"
            )
            
        event.Skip()
        
    # State management
    def save_state(self):
        """Save tab state."""
        return {
            "toggle1": self.toggle1.GetValue(),
            "toggle2": self.toggle2.GetValue(),
            "toggle3": self.toggle3.GetValue(),
            "date": self.date_picker.GetValue().FormatISODate(),
            "color": self.color_picker.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),
            "file": self.file_picker.GetPath(),
            "spin": self.spin.GetValue(),
            "slider": self.slider.GetValue(),
            "gauge": self.gauge.GetValue(),
            "collapsible_expanded": not self.collapsible.IsCollapsed()
        }
        
    def load_state(self, state):
        """Load tab state."""
        if "toggle1" in state:
            self.toggle1.SetValue(state["toggle1"])
        if "toggle2" in state:
            self.toggle2.SetValue(state["toggle2"])
        if "toggle3" in state:
            self.toggle3.SetValue(state["toggle3"])
            
        if "date" in state:
            dt = wx.DateTime()
            dt.ParseISODate(state["date"])
            self.date_picker.SetValue(dt)
            
        if "color" in state:
            self.color_picker.SetColour(state["color"])
            
        if "file" in state:
            self.file_picker.SetPath(state["file"])
            
        if "spin" in state:
            self.spin.SetValue(state["spin"])
            
        if "slider" in state:
            self.slider.SetValue(state["slider"])
            
        if "gauge" in state:
            self.gauge.SetValue(state["gauge"])
            
        if "collapsible_expanded" in state:
            if state["collapsible_expanded"]:
                self.collapsible.Expand()
            else:
                self.collapsible.Collapse()
                
    def reset_to_defaults(self):
        """Reset to defaults."""
        self.toggle1.SetValue(False)
        self.toggle2.SetValue(True)
        self.toggle3.SetValue(False)
        
        self.date_picker.SetValue(wx.DateTime.Now())
        self.color_picker.SetColour(wx.Colour(255, 255, 255))
        self.file_picker.SetPath("")
        
        self.spin.SetValue(50)
        self.slider.SetValue(50)
        self.gauge.SetValue(45)
        
        self.collapsible.Collapse()
