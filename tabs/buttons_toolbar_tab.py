"""Buttons & Toolbar Tab.

Tests for button variants, toolbar, and info bar controls.
"""

import wx
from state_manager import TabStateHelper


class ButtonsToolbarTab(wx.Panel, TabStateHelper):
    """Tab containing button variants, toolbar, and info bar controls."""
    
    def __init__(self, parent, main_frame):
        """Initialize buttons & toolbar tab and build UI."""
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Buttons & Toolbar"
        
        scroll = wx.ScrolledWindow(self, style=wx.VSCROLL)
        scroll.SetScrollRate(0, 20)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add control groups
        main_sizer.Add(self._create_bitmap_button_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_toolbar_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_infobar_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_scrollbar_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        
        scroll.SetSizer(main_sizer)
        
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(scroll, 1, wx.EXPAND)
        self.SetSizer(panel_sizer)
        
    def GetName(self):
        """Return human-readable tab name."""
        return self.tab_name
        
    def _create_bitmap_button_group(self, parent):
        """Create bitmap button group."""
        box = wx.StaticBox(parent, label="Bitmap Buttons (Space to activate)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="Buttons with icons - screen readers should announce label and role:"
            ),
            0, wx.ALL, 5
        )
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create simple bitmap buttons with text labels
        # Using art provider for standard icons
        self.save_btn = wx.Button(parent, label="&Save")
        self.save_btn.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_BUTTON))
        self.save_btn.SetToolTip("Save current document (Ctrl+S)")
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_bitmap_button)
        self.save_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.save_btn, 0, wx.ALL, 5)
        
        self.open_btn = wx.Button(parent, label="&Open")
        self.open_btn.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON))
        self.open_btn.SetToolTip("Open document (Ctrl+O)")
        self.open_btn.Bind(wx.EVT_BUTTON, self.on_bitmap_button)
        self.open_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.open_btn, 0, wx.ALL, 5)
        
        self.print_btn = wx.Button(parent, label="&Print")
        self.print_btn.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_BUTTON))
        self.print_btn.SetToolTip("Print document (Ctrl+P)")
        self.print_btn.Bind(wx.EVT_BUTTON, self.on_bitmap_button)
        self.print_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.print_btn, 0, wx.ALL, 5)
        
        self.help_btn = wx.Button(parent, label="&Help")
        self.help_btn.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_BUTTON))
        self.help_btn.SetToolTip("Show help (F1)")
        self.help_btn.Bind(wx.EVT_BUTTON, self.on_bitmap_button)
        self.help_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.help_btn, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALL, 5)
        
        # Button click counter
        self.bitmap_btn_label = wx.StaticText(parent, label="No button clicked yet")
        sizer.Add(self.bitmap_btn_label, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_toolbar_group(self, parent):
        """Create toolbar control group."""
        box = wx.StaticBox(parent, label="Toolbar (Tab to navigate, Space to activate)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="Full toolbar with tools, separators, and toggles:"
            ),
            0, wx.ALL, 5
        )
        
        # Create toolbar
        self.toolbar = wx.ToolBar(parent, style=wx.TB_HORIZONTAL | wx.TB_TEXT)
        
        # File tools
        self.toolbar.AddTool(
            wx.ID_NEW,
            "New",
            wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR),
            shortHelp="New document (Ctrl+N)"
        )
        self.toolbar.AddTool(
            wx.ID_OPEN,
            "Open",
            wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR),
            shortHelp="Open document (Ctrl+O)"
        )
        self.toolbar.AddTool(
            wx.ID_SAVE,
            "Save",
            wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR),
            shortHelp="Save document (Ctrl+S)"
        )
        
        self.toolbar.AddSeparator()
        
        # Edit tools (toggle buttons)
        self.toolbar.AddCheckTool(
            wx.ID_ANY,
            "Bold",
            wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_TOOLBAR),
            shortHelp="Bold text (Ctrl+B)"
        )
        self.toolbar.AddCheckTool(
            wx.ID_ANY,
            "Italic",
            wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_TOOLBAR),
            shortHelp="Italic text (Ctrl+I)"
        )
        self.toolbar.AddCheckTool(
            wx.ID_ANY,
            "Underline",
            wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_TOOLBAR),
            shortHelp="Underline text (Ctrl+U)"
        )
        
        self.toolbar.AddSeparator()
        
        # Clipboard tools
        self.toolbar.AddTool(
            wx.ID_CUT,
            "Cut",
            wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR),
            shortHelp="Cut (Ctrl+X)"
        )
        self.toolbar.AddTool(
            wx.ID_COPY,
            "Copy",
            wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR),
            shortHelp="Copy (Ctrl+C)"
        )
        self.toolbar.AddTool(
            wx.ID_PASTE,
            "Paste",
            wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR),
            shortHelp="Paste (Ctrl+V)"
        )
        
        self.toolbar.AddSeparator()
        
        # Undo/Redo
        self.toolbar.AddTool(
            wx.ID_UNDO,
            "Undo",
            wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR),
            shortHelp="Undo (Ctrl+Z)"
        )
        self.toolbar.AddTool(
            wx.ID_REDO,
            "Redo",
            wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR),
            shortHelp="Redo (Ctrl+Y)"
        )
        
        self.toolbar.Realize()
        self.toolbar.Bind(wx.EVT_TOOL, self.on_toolbar_tool)
        
        sizer.Add(self.toolbar, 0, wx.ALL | wx.EXPAND, 5)
        
        # Toolbar action display
        self.toolbar_label = wx.StaticText(parent, label="Click toolbar buttons to see actions")
        sizer.Add(self.toolbar_label, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_infobar_group(self, parent):
        """Create info bar control group."""
        box = wx.StaticBox(parent, label="Info Bar (Esc to dismiss)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="Info bars for notifications - screen readers announce content automatically:"
            ),
            0, wx.ALL, 5
        )
        
        # Info bar container
        self.infobar = wx.InfoBar(parent)
        sizer.Add(self.infobar, 0, wx.ALL | wx.EXPAND, 5)
        
        # Buttons to show different info bar types
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.info_btn = wx.Button(parent, label="Show &Info")
        self.info_btn.Bind(wx.EVT_BUTTON, lambda e: self._show_infobar(
            "This is an informational message.",
            wx.ICON_INFORMATION
        ))
        self.info_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.info_btn, 0, wx.ALL, 5)
        
        self.warning_btn = wx.Button(parent, label="Show &Warning")
        self.warning_btn.Bind(wx.EVT_BUTTON, lambda e: self._show_infobar(
            "This is a warning message - please review your changes.",
            wx.ICON_WARNING
        ))
        self.warning_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.warning_btn, 0, wx.ALL, 5)
        
        self.error_btn = wx.Button(parent, label="Show &Error")
        self.error_btn.Bind(wx.EVT_BUTTON, lambda e: self._show_infobar(
            "This is an error message - the operation failed.",
            wx.ICON_ERROR
        ))
        self.error_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.error_btn, 0, wx.ALL, 5)
        
        self.dismiss_btn = wx.Button(parent, label="&Dismiss Info Bar")
        self.dismiss_btn.Bind(wx.EVT_BUTTON, lambda e: self.infobar.Dismiss())
        self.dismiss_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.dismiss_btn, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_scrollbar_group(self, parent):
        """Create scrollbar control group."""
        box = wx.StaticBox(parent, label="Scroll Bar (Arrow keys, Page Up/Down)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="Horizontal and vertical scrollbars for accessibility testing:"
            ),
            0, wx.ALL, 5
        )
        
        # Horizontal scrollbar
        sizer.Add(wx.StaticText(parent, label="&Horizontal Scrollbar:"), 0, wx.ALL, 5)
        
        self.h_scrollbar = wx.ScrollBar(
            parent,
            style=wx.SB_HORIZONTAL,
            size=(300, -1)
        )
        self.h_scrollbar.SetScrollbar(
            position=50,      # Current position
            thumbSize=10,     # Thumb size (visible portion)
            range=100,        # Total range
            pageSize=10       # Page size (Page Up/Down)
        )
        self.h_scrollbar.SetToolTip("Arrow keys, Page Up/Down, Home/End")
        self.h_scrollbar.Bind(wx.EVT_SCROLL, self.on_h_scroll)
        self.h_scrollbar.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.h_scrollbar, 0, wx.ALL | wx.EXPAND, 5)
        
        self.h_scroll_label = wx.StaticText(parent, label="")
        self._update_h_scroll_label()
        sizer.Add(self.h_scroll_label, 0, wx.ALL, 5)
        
        # Vertical scrollbar
        sizer.Add(wx.StaticText(parent, label="&Vertical Scrollbar:"), 0, wx.ALL, 5)
        
        v_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.v_scrollbar = wx.ScrollBar(
            parent,
            style=wx.SB_VERTICAL,
            size=(-1, 100)
        )
        self.v_scrollbar.SetScrollbar(
            position=30,
            thumbSize=10,
            range=100,
            pageSize=10
        )
        self.v_scrollbar.SetToolTip("Arrow keys, Page Up/Down, Home/End")
        self.v_scrollbar.Bind(wx.EVT_SCROLL, self.on_v_scroll)
        self.v_scrollbar.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        v_sizer.Add(self.v_scrollbar, 0, wx.ALL, 5)
        
        self.v_scroll_label = wx.StaticText(parent, label="")
        self._update_v_scroll_label()
        v_sizer.Add(self.v_scroll_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        sizer.Add(v_sizer, 0, wx.ALL, 5)
        
        return sizer
        
    def _show_infobar(self, message, icon):
        """Show info bar with message."""
        self.infobar.ShowMessage(message, icon)
        self.main_frame.update_status_bar(
            "Info bar shown",
            f"Type: {self._get_icon_name(icon)}",
            "Esc to dismiss"
        )
        
    def _get_icon_name(self, icon):
        """Get icon name for display."""
        if icon == wx.ICON_INFORMATION:
            return "Information"
        elif icon == wx.ICON_WARNING:
            return "Warning"
        elif icon == wx.ICON_ERROR:
            return "Error"
        return "None"
        
    def _update_h_scroll_label(self):
        """Update horizontal scrollbar label."""
        pos = self.h_scrollbar.GetThumbPosition()
        range_val = self.h_scrollbar.GetRange()
        self.h_scroll_label.SetLabel(f"Position: {pos} of {range_val}")
        
    def _update_v_scroll_label(self):
        """Update vertical scrollbar label."""
        pos = self.v_scrollbar.GetThumbPosition()
        range_val = self.v_scrollbar.GetRange()
        self.v_scroll_label.SetLabel(f"Position: {pos} of {range_val}")
        
    # Event handlers
    def on_bitmap_button(self, event):
        """Handle bitmap button click."""
        btn = event.GetEventObject()
        label = btn.GetLabel()
        self.bitmap_btn_label.SetLabel(f"{label} button clicked")
        self.main_frame.update_status_bar(
            f"{label} button activated",
            "Role: Button with bitmap",
            ""
        )
        
    def on_toolbar_tool(self, event):
        """Handle toolbar tool click."""
        tool_id = event.GetId()
        tool = self.toolbar.FindById(tool_id)
        
        if tool:
            label = tool.GetLabel()
            is_toggled = self.toolbar.GetToolState(tool_id)
            
            if tool.IsToggle():
                status = "checked" if is_toggled else "unchecked"
                self.toolbar_label.SetLabel(f"{label} tool toggled ({status})")
            else:
                self.toolbar_label.SetLabel(f"{label} tool activated")
                
            self.main_frame.update_status_bar(
                f"Toolbar: {label}",
                f"Role: Tool button, State: {status if tool.IsToggle() else 'pressed'}",
                ""
            )
        
    def on_h_scroll(self, event):
        """Handle horizontal scrollbar."""
        self._update_h_scroll_label()
        pos = self.h_scrollbar.GetThumbPosition()
        self.main_frame.update_status_bar(
            "Horizontal scrollbar",
            f"Position: {pos}",
            "Arrow keys, Page Up/Down, Home/End"
        )
        
    def on_v_scroll(self, event):
        """Handle vertical scrollbar."""
        self._update_v_scroll_label()
        pos = self.v_scrollbar.GetThumbPosition()
        self.main_frame.update_status_bar(
            "Vertical scrollbar",
            f"Position: {pos}",
            "Arrow keys, Page Up/Down, Home/End"
        )
        
    def on_control_focus(self, event):
        """Handle focus events."""
        ctrl = event.GetEventObject()
        
        if isinstance(ctrl, wx.Button):
            label = ctrl.GetLabel()
            self.main_frame.update_status_bar(
                f"Button: {label}",
                "Role: Button with bitmap",
                "Space to activate"
            )
        elif isinstance(ctrl, wx.ScrollBar):
            pos = ctrl.GetThumbPosition()
            orientation = "Horizontal" if ctrl.HasFlag(wx.SB_HORIZONTAL) else "Vertical"
            self.main_frame.update_status_bar(
                f"{orientation} scrollbar",
                f"Role: Scrollbar, Position: {pos}",
                "Arrow keys, Page Up/Down, Home/End"
            )
            
        event.Skip()
        
    # State management
    def save_state(self):
        """Save tab state."""
        toolbar_state = {}
        for tool_id in [wx.ID_NEW, wx.ID_OPEN, wx.ID_SAVE]:
            tool = self.toolbar.FindById(tool_id)
            if tool and tool.IsToggled():
                toolbar_state[tool_id] = self.toolbar.GetToolState(tool_id)
                
        return {
            "h_scrollbar": self.h_scrollbar.GetThumbPosition(),
            "v_scrollbar": self.v_scrollbar.GetThumbPosition(),
            "toolbar": toolbar_state
        }
        
    def load_state(self, state):
        """Load tab state."""
        if "h_scrollbar" in state:
            self.h_scrollbar.SetThumbPosition(state["h_scrollbar"])
            self._update_h_scroll_label()
            
        if "v_scrollbar" in state:
            self.v_scrollbar.SetThumbPosition(state["v_scrollbar"])
            self._update_v_scroll_label()
            
        if "toolbar" in state:
            for tool_id, checked in state["toolbar"].items():
                self.toolbar.ToggleTool(tool_id, checked)
                
    def reset_to_defaults(self):
        """Reset to defaults."""
        self.h_scrollbar.SetThumbPosition(50)
        self._update_h_scroll_label()
        
        self.v_scrollbar.SetThumbPosition(30)
        self._update_v_scroll_label()
        
        # Uncheck all toggle tools
        for i in range(self.toolbar.GetToolsCount()):
            tool = self.toolbar.GetToolByPos(i)
            if tool and tool.IsToggle():
                self.toolbar.ToggleTool(tool.GetId(), False)
                
        self.infobar.Dismiss()
        self.bitmap_btn_label.SetLabel("No button clicked yet")
        self.toolbar_label.SetLabel("Click toolbar buttons to see actions")
