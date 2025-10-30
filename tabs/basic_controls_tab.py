"""Basic Controls Tab.

Tests for basic wxPython controls: Button, TextCtrl, CheckBox, RadioBox, Choice, ComboBox, ListBox.
Demonstrates keyboard navigation and screen reader accessibility.
"""

import wx
from state_manager import TabStateHelper
from test_data import (
    get_color_names, get_country_names, get_sample_text, 
    get_sample_password, DEPARTMENTS
)


class BasicControlsTab(wx.Panel, TabStateHelper):
    """Tab containing basic input controls for accessibility testing."""
    
    def __init__(self, parent, main_frame):
        """Initialize basic controls tab and build UI."""
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Basic Controls"
        
        # Create scrolled window for content
        scroll = wx.ScrolledWindow(self, style=wx.VSCROLL)
        scroll.SetScrollRate(0, 20)
        
        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add control groups
        main_sizer.Add(self._create_button_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_textctrl_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_checkbox_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_radiobox_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_choice_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_listbox_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        
        scroll.SetSizer(main_sizer)
        
        # Layout
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(scroll, 1, wx.EXPAND)
        self.SetSizer(panel_sizer)
        
    def GetName(self):
        """Return human-readable tab name."""
        return self.tab_name
        
    def _create_button_group(self, parent):
        """Create button test group."""
        box = wx.StaticBox(parent, label="Buttons (Space/Enter to activate)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Standard button
        self.std_button = wx.Button(parent, label="&Standard Button")
        self.std_button.SetToolTip("Press Space or Enter to activate")
        self.std_button.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.std_button.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.std_button, 0, wx.ALL, 5)
        
        # Default button
        self.default_button = wx.Button(parent, label="&Default Button")
        self.default_button.SetDefault()
        self.default_button.SetToolTip("Default button - activated by Enter anywhere in dialog")
        self.default_button.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.default_button.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.default_button, 0, wx.ALL, 5)
        
        # Disabled button
        self.disabled_button = wx.Button(parent, label="Disabled Button")
        self.disabled_button.Enable(False)
        self.disabled_button.SetToolTip("This button is disabled")
        sizer.Add(self.disabled_button, 0, wx.ALL, 5)
        
        # Click counter
        self.button_clicks = 0
        self.click_label = wx.StaticText(parent, label="Button clicks: 0")
        sizer.Add(self.click_label, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_textctrl_group(self, parent):
        """Create text control test group."""
        box = wx.StaticBox(parent, label="Text Controls (Arrow keys, Home/End to navigate)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Single-line text
        label1 = wx.StaticText(parent, label="&Single-line text:")
        sizer.Add(label1, 0, wx.ALL, 5)
        
        self.single_text = wx.TextCtrl(parent, value=get_sample_text())
        self.single_text.SetToolTip("Single-line text entry - navigate with arrow keys")
        self.single_text.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.single_text, 0, wx.ALL | wx.EXPAND, 5)
        
        # Multi-line text
        label2 = wx.StaticText(parent, label="&Multi-line text:")
        sizer.Add(label2, 0, wx.ALL, 5)
        
        self.multi_text = wx.TextCtrl(
            parent, 
            value=get_sample_text() + "\n\nSecond paragraph for multi-line testing.",
            style=wx.TE_MULTILINE,
            size=(-1, 100)
        )
        self.multi_text.SetToolTip("Multi-line text - Up/Down arrows for lines, Ctrl+Home/End for document")
        self.multi_text.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.multi_text, 0, wx.ALL | wx.EXPAND, 5)
        
        # Password field
        label3 = wx.StaticText(parent, label="&Password:")
        sizer.Add(label3, 0, wx.ALL, 5)
        
        self.password_text = wx.TextCtrl(parent, value=get_sample_password(), style=wx.TE_PASSWORD)
        self.password_text.SetToolTip("Password field - characters are masked")
        self.password_text.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.password_text, 0, wx.ALL | wx.EXPAND, 5)
        
        # Read-only text
        label4 = wx.StaticText(parent, label="Read-only text:")
        sizer.Add(label4, 0, wx.ALL, 5)
        
        self.readonly_text = wx.TextCtrl(parent, value="This text is read-only", style=wx.TE_READONLY)
        self.readonly_text.SetToolTip("Read-only text - cannot be edited")
        self.readonly_text.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.readonly_text, 0, wx.ALL | wx.EXPAND, 5)
        
        return sizer
        
    def _create_checkbox_group(self, parent):
        """Create checkbox test group."""
        box = wx.StaticBox(parent, label="Checkboxes (Space to toggle)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # 2-state checkboxes
        self.check1 = wx.CheckBox(parent, label="&Enable notifications")
        self.check1.SetValue(True)
        self.check1.SetToolTip("2-state checkbox - Space to toggle")
        self.check1.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)
        self.check1.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.check1, 0, wx.ALL, 5)
        
        self.check2 = wx.CheckBox(parent, label="&Save password")
        self.check2.SetValue(False)
        self.check2.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)
        self.check2.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.check2, 0, wx.ALL, 5)
        
        self.check3 = wx.CheckBox(parent, label="&Auto-update")
        self.check3.SetValue(True)
        self.check3.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)
        self.check3.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.check3, 0, wx.ALL, 5)
        
        # 3-state checkbox
        self.check3state = wx.CheckBox(parent, label="3-state checkbox", style=wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        self.check3state.Set3StateValue(wx.CHK_UNDETERMINED)
        self.check3state.SetToolTip("3-state checkbox - cycles through checked, unchecked, indeterminate")
        self.check3state.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)
        self.check3state.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.check3state, 0, wx.ALL, 5)
        
        # Disabled checkbox
        self.check_disabled = wx.CheckBox(parent, label="Disabled checkbox")
        self.check_disabled.SetValue(True)
        self.check_disabled.Enable(False)
        sizer.Add(self.check_disabled, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_radiobox_group(self, parent):
        """Create radio button test group."""
        box = wx.StaticBox(parent, label="Radio Buttons (Arrow keys to navigate)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # RadioBox (group)
        self.radio_box = wx.RadioBox(
            parent,
            label="Select &Priority",
            choices=["Low", "Medium", "High", "Critical"],
            majorDimension=2,
            style=wx.RA_SPECIFY_COLS
        )
        self.radio_box.SetSelection(1)  # Medium
        self.radio_box.SetToolTip("Radio button group - Arrow keys to select, Space to activate")
        self.radio_box.Bind(wx.EVT_RADIOBOX, self.on_radio_change)
        self.radio_box.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.radio_box, 0, wx.ALL | wx.EXPAND, 5)
        
        # Individual radio buttons
        sizer.Add(wx.StaticText(parent, label="Select Department:"), 0, wx.ALL, 5)
        
        self.radio_buttons = []
        for i, dept in enumerate(DEPARTMENTS[:5]):  # First 5 departments
            rb = wx.RadioButton(parent, label=dept, style=wx.RB_GROUP if i == 0 else 0)
            if i == 0:
                rb.SetValue(True)
            rb.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
            rb.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
            self.radio_buttons.append(rb)
            sizer.Add(rb, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_choice_group(self, parent):
        """Create choice/combobox test group."""
        box = wx.StaticBox(parent, label="Choice Controls (Alt+Down to open, arrows to navigate)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Choice (dropdown, non-editable)
        label1 = wx.StaticText(parent, label="Select &Color:")
        sizer.Add(label1, 0, wx.ALL, 5)
        
        self.choice = wx.Choice(parent, choices=get_color_names())
        self.choice.SetSelection(0)
        self.choice.SetToolTip("Choice control - Alt+Down to open, arrows to navigate, Enter to select")
        self.choice.Bind(wx.EVT_CHOICE, self.on_choice_change)
        self.choice.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.choice, 0, wx.ALL | wx.EXPAND, 5)
        
        # ComboBox (editable dropdown)
        label2 = wx.StaticText(parent, label="Select or enter color:")
        sizer.Add(label2, 0, wx.ALL, 5)
        
        self.combobox = wx.ComboBox(parent, choices=get_color_names(), value="Blue")
        self.combobox.SetToolTip("ComboBox - editable dropdown, type or select from list")
        self.combobox.Bind(wx.EVT_COMBOBOX, self.on_choice_change)
        self.combobox.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.combobox, 0, wx.ALL | wx.EXPAND, 5)
        
        return sizer
        
    def _create_listbox_group(self, parent):
        """Create listbox test group."""
        box = wx.StaticBox(parent, label="List Boxes (Arrow keys, Space for multi-select)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Single-selection ListBox
        label1 = wx.StaticText(parent, label="Single selection list:")
        sizer.Add(label1, 0, wx.ALL, 5)
        
        # Use ALL countries (50 items) for adequate scrolling and navigation testing
        # More data helps test: keyboard navigation, scrolling, position announcements
        countries = get_country_names()
        self.listbox_single = wx.ListBox(parent, choices=countries, size=(-1, 120))
        self.listbox_single.SetSelection(0)
        self.listbox_single.SetToolTip("Single selection - Arrow keys to navigate, Enter to activate")
        self.listbox_single.Bind(wx.EVT_LISTBOX, self.on_listbox_change)
        self.listbox_single.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.listbox_single, 0, wx.ALL | wx.EXPAND, 5)
        
        # Multi-selection ListBox
        label2 = wx.StaticText(parent, label="Multi selection list (Ctrl+Space, Shift+arrows):")
        sizer.Add(label2, 0, wx.ALL, 5)
        
        # Use all 50 countries for comprehensive multi-select testing
        # Tests: Ctrl+Click, Ctrl+Space, Shift+arrows for range selection
        self.listbox_multi = wx.ListBox(
            parent, 
            choices=countries, 
            size=(-1, 120),
            style=wx.LB_MULTIPLE
        )
        self.listbox_multi.SetSelection(0)
        self.listbox_multi.SetSelection(2)
        self.listbox_multi.SetToolTip("Multi selection - Ctrl+Space to toggle, Shift+arrows for range")
        self.listbox_multi.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.listbox_multi, 0, wx.ALL | wx.EXPAND, 5)
        
        # CheckListBox
        label3 = wx.StaticText(parent, label="List with checkboxes (Space to toggle):")
        sizer.Add(label3, 0, wx.ALL, 5)
        
        self.checklist = wx.CheckListBox(parent, choices=DEPARTMENTS, size=(-1, 120))
        self.checklist.Check(0, True)
        self.checklist.Check(2, True)
        self.checklist.Check(4, True)
        self.checklist.SetToolTip("CheckListBox - Arrow keys to navigate, Space to check/uncheck")
        self.checklist.Bind(wx.EVT_CHECKLISTBOX, self.on_checklistbox_change)
        self.checklist.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.checklist, 0, wx.ALL | wx.EXPAND, 5)
        
        return sizer
        
    # Event handlers
    def on_button_click(self, event):
        """Handle button clicks.
        
        Triggered by:
        - Space bar (primary activation)
        - Enter key (alternative activation)
        - Mouse click
        
        Increments counter and updates display.
        Screen readers should announce button label + "pressed".
        """
        btn = event.GetEventObject()
        # Track total clicks across all buttons
        self.button_clicks += 1
        self.click_label.SetLabel(f"Button clicks: {self.button_clicks}")
        
        # Update status bar with click information
        self.main_frame.update_status_bar(
            f"Button clicked: {btn.GetLabel()}",
            f"Total clicks: {self.button_clicks}",
            ""
        )
        
    def on_checkbox_change(self, event):
        """Handle checkbox state changes.
        
        Supports both 2-state and 3-state checkboxes:
        - 2-state: Checked/Unchecked (standard)
        - 3-state: Checked/Unchecked/Indeterminate (tri-state)
        
        Keyboard: Space toggles state
        Screen readers announce: label + state
        """
        cb = event.GetEventObject()
        # Check if this is a 3-state checkbox
        if hasattr(cb, 'Get3StateValue'):
            state_names = {wx.CHK_UNCHECKED: "Unchecked", wx.CHK_CHECKED: "Checked", wx.CHK_UNDETERMINED: "Indeterminate"}
            state = state_names[cb.Get3StateValue()]
        else:
            # Standard 2-state checkbox
            state = "Checked" if cb.GetValue() else "Unchecked"
            
        self.main_frame.update_status_bar(
            f"Checkbox: {cb.GetLabel()}",
            f"State: {state}",
            "Space to toggle"
        )
        
    def on_radio_change(self, event):
        """Handle radio button changes.
        
        Two types of radio controls:
        1. RadioBox: Group of radio buttons in a box (compact)
        2. RadioButton: Individual radio buttons (flexible layout)
        
        Keyboard navigation:
        - Arrow keys: Move between options
        - Space: Select (if not auto-selected)
        
        Radio buttons are mutually exclusive within their group.
        Screen readers announce: group name, option, position (e.g., "2 of 3").
        """
        obj = event.GetEventObject()
        if isinstance(obj, wx.RadioBox):
            # RadioBox: All options in one control
            selection = obj.GetStringSelection()
            self.main_frame.update_status_bar(
                f"RadioBox: {obj.GetLabel()}",
                f"Selected: {selection}",
                "Arrow keys to change"
            )
        else:
            # Individual RadioButton controls
            self.main_frame.update_status_bar(
                "Radio button",
                f"Selected: {obj.GetLabel()}",
                "Arrow keys to change selection"
            )
            
    def on_choice_change(self, event):
        """Handle choice/combobox changes.
        
        Choice vs. ComboBox:
        - Choice: Read-only dropdown (select from list only)
        - ComboBox: Editable dropdown (select OR type custom value)
        
        Keyboard shortcuts:
        - Alt+Down: Open dropdown
        - Arrow keys: Navigate options
        - Type letters: Quick search
        - Enter: Confirm selection
        - Esc: Cancel
        
        Screen readers announce: control type, value, "collapsed/expanded".
        """
        obj = event.GetEventObject()
        # Get value (method differs between Choice and ComboBox)
        value = obj.GetStringSelection() if hasattr(obj, 'GetStringSelection') else obj.GetValue()
        control_type = "Choice" if isinstance(obj, wx.Choice) else "ComboBox"
        
        self.main_frame.update_status_bar(
            f"{control_type} control",
            f"Selected: {value}",
            "Alt+Down to open"
        )
        
    def on_listbox_change(self, event):
        """Handle listbox selection changes.
        
        ListBox selection modes:
        - Single: One item selected (default)
        - Multiple: Ctrl+Click, Ctrl+Space to toggle
        - Extended: Shift+Click for ranges
        
        Keyboard navigation:
        - Arrow keys: Move selection
        - Home/End: First/last item
        - Page Up/Down: Large movements
        - Type letters: Quick search
        
        Screen readers announce: item text, position (e.g., "3 of 50").
        """
        lb = event.GetEventObject()
        sel = lb.GetStringSelection()
        
        self.main_frame.update_status_bar(
            "ListBox",
            f"Selected: {sel}",
            "Arrow keys to navigate"
        )
        
    def on_checklistbox_change(self, event):
        """Handle checklistbox changes.
        
        CheckListBox: List where each item has a checkbox.
        Combines list selection with checkbox toggle.
        
        Keyboard:
        - Arrow keys: Navigate items
        - Space: Toggle checkbox for current item
        - Ctrl+A: Select all (if multi-select)
        
        Note: Selection and check state are independent.
        Can be checked without being selected.
        
        Screen readers announce: item text + checked state.
        """
        index = event.GetSelection()
        item = self.checklist.GetString(index)
        checked = self.checklist.IsChecked(index)
        
        self.main_frame.update_status_bar(
            f"CheckListBox item: {item}",
            f"State: {'Checked' if checked else 'Unchecked'}",
            "Space to toggle checkbox"
        )
        
    def on_control_focus(self, event):
        """Handle control focus events for status bar updates.
        
        Updates status bar when controls receive focus to show:
        - Control name and type
        - Expected screen reader announcements
        - Keyboard shortcuts
        
        Helps testers verify screen reader output by comparing
        actual announcements to expected behavior.
        """
        ctrl = event.GetEventObject()
        ctrl_type = ctrl.__class__.__name__
        
        # Determine control info based on type
        if isinstance(ctrl, wx.Button):
            info = f"Button: {ctrl.GetLabel()}"
            role_state = f"Role: Button, State: {'Default' if ctrl.GetId() == wx.ID_OK else 'Normal'}"
            hint = "Space/Enter to activate"
        elif isinstance(ctrl, wx.TextCtrl):
            style_desc = ""
            if ctrl.GetWindowStyle() & wx.TE_MULTILINE:
                style_desc = "Multi-line"
            elif ctrl.GetWindowStyle() & wx.TE_PASSWORD:
                style_desc = "Password"
            elif ctrl.GetWindowStyle() & wx.TE_READONLY:
                style_desc = "Read-only"
            else:
                style_desc = "Single-line"
            info = f"TextCtrl: {style_desc}"
            role_state = f"Role: Edit, Value length: {len(ctrl.GetValue())}"
            hint = "Arrow keys, Home/End, Ctrl+A to select all"
        elif isinstance(ctrl, wx.CheckBox):
            info = f"CheckBox: {ctrl.GetLabel()}"
            state = "Checked" if ctrl.GetValue() else "Unchecked"
            role_state = f"Role: Checkbox, State: {state}"
            hint = "Space to toggle"
        elif isinstance(ctrl, (wx.RadioButton, wx.RadioBox)):
            info = f"RadioButton: {ctrl.GetLabel()}"
            role_state = "Role: Radio button"
            hint = "Arrow keys to change, Space to activate"
        elif isinstance(ctrl, wx.Choice):
            info = "Choice control"
            role_state = f"Role: ComboBox, Value: {ctrl.GetStringSelection()}"
            hint = "Alt+Down to open, Arrow keys to navigate"
        elif isinstance(ctrl, wx.ComboBox):
            info = "ComboBox (editable)"
            role_state = f"Role: ComboBox (editable), Value: {ctrl.GetValue()}"
            hint = "Type or Alt+Down to select"
        elif isinstance(ctrl, wx.ListBox):
            info = "ListBox"
            sel = ctrl.GetStringSelection()
            role_state = f"Role: List, Selected: {sel}"
            hint = "Arrow keys, Ctrl+Space for multi-select"
        elif isinstance(ctrl, wx.CheckListBox):
            info = "CheckListBox"
            role_state = "Role: List with checkboxes"
            hint = "Arrow keys to navigate, Space to toggle"
        else:
            info = f"Control: {ctrl_type}"
            role_state = ""
            hint = ""
            
        self.main_frame.update_status_bar(info, role_state, hint)
        event.Skip()
        
    # State management
    def save_state(self):
        """Save tab state to JSON-serializable dictionary.
        
        Captures all control values:
        - Button click counter
        - All text control values (single/multi-line, password)
        - Checkbox states (2-state and 3-state)
        - Radio button selections (box and individual buttons)
        - Choice/ComboBox values
        - ListBox selections (single and multi-select)
        - CheckListBox check states
        
        Returns:
            dict: State dictionary for JSON serialization
        """
        return {
            # Button group
            "button_clicks": self.button_clicks,
            # Text controls
            "single_text": self.single_text.GetValue(),
            "multi_text": self.multi_text.GetValue(),
            "password_text": self.password_text.GetValue(),
            # Checkboxes
            "check1": self.check1.GetValue(),
            "check2": self.check2.GetValue(),
            "check3": self.check3.GetValue(),
            "check3state": self.check3state.Get3StateValue(),
            # Radio controls
            "radio_box": self.radio_box.GetSelection(),
            "radio_buttons": [rb.GetValue() for rb in self.radio_buttons],
            # Dropdown controls
            "choice": self.choice.GetSelection(),
            "combobox": self.combobox.GetValue(),
            # List controls
            "listbox_single": self.listbox_single.GetSelection(),
            "listbox_multi": list(self.listbox_multi.GetSelections()),
            "checklist": [self.checklist.IsChecked(i) for i in range(self.checklist.GetCount())]
        }
        
    def load_state(self, state):
        """Load tab state from saved dictionary.
        
        Restores all control values:
        - Button click counter and label
        - All text control values
        - All checkbox states (2-state and 3-state)
        - Radio button selections
        - Choice/ComboBox values
        - ListBox selections (single and multi-select)
        - CheckListBox check states
        
        Gracefully handles missing state keys (optional restore).
        
        Args:
            state (dict): State dictionary from JSON
        """
        # Restore button click counter
        if "button_clicks" in state:
            self.button_clicks = state["button_clicks"]
            self.click_label.SetLabel(f"Button clicks: {self.button_clicks}")
            
        # Restore text controls
        if "single_text" in state:
            self.single_text.SetValue(state["single_text"])
        if "multi_text" in state:
            self.multi_text.SetValue(state["multi_text"])
        if "password_text" in state:
            self.password_text.SetValue(state["password_text"])
            
        # Restore checkboxes
        if "check1" in state:
            self.check1.SetValue(state["check1"])
        if "check2" in state:
            self.check2.SetValue(state["check2"])
        if "check3" in state:
            self.check3.SetValue(state["check3"])
        if "check3state" in state:
            self.check3state.Set3StateValue(state["check3state"])
            
        # Restore radio controls
        if "radio_box" in state:
            self.radio_box.SetSelection(state["radio_box"])
        if "radio_buttons" in state:
            for rb, val in zip(self.radio_buttons, state["radio_buttons"]):
                rb.SetValue(val)
                
        # Restore dropdown controls
        if "choice" in state:
            self.choice.SetSelection(state["choice"])
        if "combobox" in state:
            self.combobox.SetValue(state["combobox"])
            
        # Restore list controls
        if "listbox_single" in state:
            self.listbox_single.SetSelection(state["listbox_single"])
        if "listbox_multi" in state:
            for idx in state["listbox_multi"]:
                self.listbox_multi.SetSelection(idx)
                
        # Restore checklist states
        if "checklist" in state:
            for i, checked in enumerate(state["checklist"]):
                if i < self.checklist.GetCount():
                    self.checklist.Check(i, checked)
                    
    def reset_to_defaults(self):
        """Reset all controls to default test data.
        
        Restores:
        - Button click counter to 0
        - Text controls to sample data
        - Checkboxes to initial states
        - Radio buttons to first option
        - Choice/ComboBox to first item
        - ListBox selections cleared
        - CheckListBox with some items checked
        
        Used when "Reset All Tabs" is selected from menu.
        Provides clean state for fresh testing.
        """
        # Reset button group
        self.button_clicks = 0
        self.click_label.SetLabel("Button clicks: 0")
        
        # Reset text controls with sample data
        self.single_text.SetValue(get_sample_text())
        self.multi_text.SetValue(get_sample_text() + "\n\nSecond paragraph for multi-line testing.")
        self.password_text.SetValue(get_sample_password())
        
        # Reset checkboxes (varied states for testing)
        self.check1.SetValue(True)
        self.check2.SetValue(False)
        self.check3.SetValue(True)
        self.check3state.Set3StateValue(wx.CHK_UNDETERMINED)
        
        self.radio_box.SetSelection(1)
        self.radio_buttons[0].SetValue(True)
        
        self.choice.SetSelection(0)
        self.combobox.SetValue("Blue")
        
        self.listbox_single.SetSelection(0)
        self.listbox_multi.SetSelection(0)
        self.listbox_multi.SetSelection(2)
        
        for i in range(self.checklist.GetCount()):
            self.checklist.Check(i, i in [0, 2, 4])
