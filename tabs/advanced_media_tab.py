"""Advanced Media & Data Tab.

Tests for MediaCtrl, RichTextCtrl, PropertyGrid, and DataViewCtrl.
"""

import wx
import wx.adv
import wx.media
import wx.richtext as rt
import wx.propgrid as wxpg
import wx.dataview as dv
from state_manager import TabStateHelper
from test_data import generate_person_name
import os


class AdvancedMediaTab(wx.Panel, TabStateHelper):
    """Tab containing specialized advanced controls."""
    
    def __init__(self, parent, main_frame):
        """Initialize advanced media/data tab and build UI."""
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Advanced Media & Data"
        
        scroll = wx.ScrolledWindow(self, style=wx.VSCROLL)
        scroll.SetScrollRate(0, 20)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add control groups
        main_sizer.Add(self._create_richtextctrl_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_propertygrid_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_dataview_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_mediactrl_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        
        scroll.SetSizer(main_sizer)
        
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(scroll, 1, wx.EXPAND)
        self.SetSizer(panel_sizer)
        
    def GetName(self):
        """Return human-readable tab name."""
        return self.tab_name
        
    def _create_richtextctrl_group(self, parent):
        """Create RichTextCtrl group."""
        box = wx.StaticBox(parent, label="Rich Text Control (Formatted text editor)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="Formatted text editor with bold, italic, colors, and styles:"
            ),
            0, wx.ALL, 5
        )
        
        # Rich text control
        self.richtext = rt.RichTextCtrl(
            parent,
            size=(600, 200),
            style=wx.VSCROLL | wx.HSCROLL | wx.BORDER_THEME
        )
        self.richtext.SetToolTip(
            "Arrow keys to navigate, Ctrl+B for bold, Ctrl+I for italic, "
            "Ctrl+U for underline, standard edit shortcuts work"
        )
        self.richtext.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        # Add formatted sample text
        self.richtext.BeginBold()
        self.richtext.WriteText("Welcome to Rich Text Editor\n\n")
        self.richtext.EndBold()
        
        self.richtext.WriteText("This editor supports ")
        self.richtext.BeginBold()
        self.richtext.WriteText("bold")
        self.richtext.EndBold()
        self.richtext.WriteText(", ")
        
        self.richtext.BeginItalic()
        self.richtext.WriteText("italic")
        self.richtext.EndItalic()
        self.richtext.WriteText(", and ")
        
        self.richtext.BeginUnderline()
        self.richtext.WriteText("underline")
        self.richtext.EndUnderline()
        self.richtext.WriteText(" text.\n\n")
        
        self.richtext.BeginTextColour(wx.Colour(0, 0, 255))
        self.richtext.WriteText("You can also use different colors!")
        self.richtext.EndTextColour()
        self.richtext.WriteText("\n\n")
        
        self.richtext.BeginFontSize(14)
        self.richtext.WriteText("Different font sizes are supported too.\n\n")
        self.richtext.EndFontSize()
        
        self.richtext.WriteText(
            "Screen readers should announce text content and navigate by character, "
            "word, line, and paragraph. Standard edit shortcuts (Ctrl+A, Ctrl+C, "
            "Ctrl+V, Ctrl+X, Ctrl+Z) all work.\n\n"
            "Try editing this text and adding your own formatted content!"
        )
        
        sizer.Add(self.richtext, 1, wx.ALL | wx.EXPAND, 5)
        
        # Formatting buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.bold_btn = wx.Button(parent, label="&Bold (Ctrl+B)")
        self.bold_btn.Bind(wx.EVT_BUTTON, lambda e: self._apply_format('bold'))
        self.bold_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.bold_btn, 0, wx.ALL, 5)
        
        self.italic_btn = wx.Button(parent, label="&Italic (Ctrl+I)")
        self.italic_btn.Bind(wx.EVT_BUTTON, lambda e: self._apply_format('italic'))
        self.italic_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.italic_btn, 0, wx.ALL, 5)
        
        self.underline_btn = wx.Button(parent, label="&Underline (Ctrl+U)")
        self.underline_btn.Bind(wx.EVT_BUTTON, lambda e: self._apply_format('underline'))
        self.underline_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.underline_btn, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_propertygrid_group(self, parent):
        """Create PropertyGrid group."""
        box = wx.StaticBox(parent, label="Property Grid (Property sheet editor)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="Property sheet for configuring object properties:"
            ),
            0, wx.ALL, 5
        )
        
        # Property grid
        self.propgrid = wxpg.PropertyGrid(
            parent,
            size=(600, 300),
            style=wxpg.PG_SPLITTER_AUTO_CENTER | wxpg.PG_BOLD_MODIFIED
        )
        self.propgrid.SetToolTip(
            "Arrow keys to navigate properties, Enter to edit, Tab to cycle editors, "
            "F4 to expand combo boxes"
        )
        self.propgrid.Bind(wxpg.EVT_PG_CHANGED, self.on_property_changed)
        self.propgrid.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        # Add property categories and properties
        self.propgrid.Append(wxpg.PropertyCategory("1 - Application Settings"))
        self.propgrid.Append(wxpg.StringProperty("Application Name", value="Accessibility Test Suite"))
        self.propgrid.Append(wxpg.StringProperty("Version", value="1.0.0"))
        self.propgrid.Append(wxpg.BoolProperty("Auto Save", value=True))
        self.propgrid.Append(wxpg.IntProperty("Auto Save Interval (seconds)", value=300))
        
        self.propgrid.Append(wxpg.PropertyCategory("2 - Display Settings"))
        self.propgrid.Append(wxpg.ColourProperty("Background Color", value=wx.WHITE))
        self.propgrid.Append(wxpg.ColourProperty("Text Color", value=wx.BLACK))
        self.propgrid.Append(wxpg.FontProperty("Font"))
        
        # Enum property
        theme_prop = wxpg.EnumProperty(
            "Theme",
            "Theme",
            ["Light", "Dark", "High Contrast", "System Default"],
            [0, 1, 2, 3],
            0
        )
        self.propgrid.Append(theme_prop)
        
        self.propgrid.Append(wxpg.PropertyCategory("3 - Window Settings"))
        self.propgrid.Append(wxpg.IntProperty("Width", value=1200))
        self.propgrid.Append(wxpg.IntProperty("Height", value=800))
        self.propgrid.Append(wxpg.BoolProperty("Maximized", value=False))
        self.propgrid.Append(wxpg.BoolProperty("Always on Top", value=False))
        
        self.propgrid.Append(wxpg.PropertyCategory("4 - Accessibility"))
        self.propgrid.Append(wxpg.BoolProperty("High Contrast Mode", value=False))
        self.propgrid.Append(wxpg.IntProperty("Font Scale (%)", value=100))
        self.propgrid.Append(wxpg.BoolProperty("Screen Reader Support", value=True))
        self.propgrid.Append(wxpg.BoolProperty("Keyboard Only Mode", value=False))
        
        sizer.Add(self.propgrid, 1, wx.ALL | wx.EXPAND, 5)
        
        # Property info
        self.propgrid_label = wx.StaticText(parent, label="Select properties to edit")
        sizer.Add(self.propgrid_label, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_dataview_group(self, parent):
        """Create DataViewCtrl group."""
        box = wx.StaticBox(parent, label="Data View Control (Virtual list/tree)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="High-performance data viewer with sorting and filtering:"
            ),
            0, wx.ALL, 5
        )
        
        # Data view control
        self.dataview = dv.DataViewListCtrl(
            parent,
            size=(600, 250),
            style=dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE
        )
        self.dataview.SetToolTip(
            "Arrow keys to navigate, Space to select, Enter to activate, "
            "Ctrl+A to select all, Ctrl+Click for multi-select"
        )
        self.dataview.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.on_dataview_selection)
        self.dataview.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.on_dataview_activated)
        self.dataview.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        # Add columns
        self.dataview.AppendTextColumn("ID", width=60)
        self.dataview.AppendTextColumn("Employee", width=150)
        self.dataview.AppendTextColumn("Department", width=120)
        self.dataview.AppendTextColumn("Title", width=150)
        self.dataview.AppendTextColumn("Salary", width=100)
        self.dataview.AppendTextColumn("Start Date", width=100)
        
        # Add sample data (100 rows for adequate scrolling/testing)
        # Use realistic names for better screen reader testing
        departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"]
        titles = ["Manager", "Senior", "Junior", "Lead", "Director", "Analyst", "Specialist"]
        
        for i in range(100):
            # Generate realistic names instead of "Employee 1, Employee 2"
            # Screen readers sound more natural with real names
            employee_name = generate_person_name()
            self.dataview.AppendItem([
                str(i + 1001),  # ID: 1001-1100
                employee_name,  # Realistic name from test_data
                departments[i % len(departments)],
                f"{titles[i % len(titles)]} {departments[i % len(departments)]}",
                f"${55000 + (i * 1500):,}",  # Salary range: $55k-$203.5k
                f"2020-{(i % 12) + 1:02d}-15"  # Various start dates
            ])
        
        sizer.Add(self.dataview, 1, wx.ALL | wx.EXPAND, 5)
        
        # Selection info
        self.dataview_label = wx.StaticText(parent, label="No selection")
        sizer.Add(self.dataview_label, 0, wx.ALL, 5)
        
        # Action buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.select_all_btn = wx.Button(parent, label="Select &All")
        self.select_all_btn.Bind(wx.EVT_BUTTON, self.on_dataview_select_all)
        self.select_all_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.select_all_btn, 0, wx.ALL, 5)
        
        self.clear_selection_btn = wx.Button(parent, label="&Clear Selection")
        self.clear_selection_btn.Bind(wx.EVT_BUTTON, self.on_dataview_clear)
        self.clear_selection_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.clear_selection_btn, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_mediactrl_group(self, parent):
        """Create MediaCtrl group."""
        box = wx.StaticBox(parent, label="Media Control (Audio/Video playback)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="Media player control (requires media file to test playback):"
            ),
            0, wx.ALL, 5
        )
        
        # Media control
        self.media = wx.media.MediaCtrl(
            parent,
            size=(600, 200),
            style=wx.SIMPLE_BORDER
        )
        self.media.SetToolTip("Use buttons below to control playback")
        self.media.Bind(wx.media.EVT_MEDIA_LOADED, self.on_media_loaded)
        self.media.Bind(wx.media.EVT_MEDIA_STATECHANGED, self.on_media_state_changed)
        self.media.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        sizer.Add(self.media, 0, wx.ALL | wx.EXPAND, 5)
        
        # Media controls
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.load_btn = wx.Button(parent, label="&Load File...")
        self.load_btn.Bind(wx.EVT_BUTTON, self.on_load_media)
        self.load_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        btn_sizer.Add(self.load_btn, 0, wx.ALL, 5)
        
        self.play_btn = wx.Button(parent, label="&Play")
        self.play_btn.Bind(wx.EVT_BUTTON, self.on_play_media)
        self.play_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        self.play_btn.Enable(False)
        btn_sizer.Add(self.play_btn, 0, wx.ALL, 5)
        
        self.pause_btn = wx.Button(parent, label="P&ause")
        self.pause_btn.Bind(wx.EVT_BUTTON, self.on_pause_media)
        self.pause_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        self.pause_btn.Enable(False)
        btn_sizer.Add(self.pause_btn, 0, wx.ALL, 5)
        
        self.stop_btn = wx.Button(parent, label="&Stop")
        self.stop_btn.Bind(wx.EVT_BUTTON, self.on_stop_media)
        self.stop_btn.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        self.stop_btn.Enable(False)
        btn_sizer.Add(self.stop_btn, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALL, 5)
        
        # Volume control
        vol_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vol_sizer.Add(wx.StaticText(parent, label="&Volume:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.volume_slider = wx.Slider(
            parent,
            value=50,
            minValue=0,
            maxValue=100,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.volume_slider.SetToolTip("Arrow keys to adjust volume")
        self.volume_slider.Bind(wx.EVT_SLIDER, self.on_volume_changed)
        self.volume_slider.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        vol_sizer.Add(self.volume_slider, 1, wx.ALL | wx.EXPAND, 5)
        
        sizer.Add(vol_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # Media info
        self.media_label = wx.StaticText(parent, label="No media loaded")
        sizer.Add(self.media_label, 0, wx.ALL, 5)
        
        return sizer
        
    def _apply_format(self, format_type):
        """Apply formatting to selected text in RichTextCtrl.
        
        Applies text formatting to current selection only.
        If no text is selected, formatting has no effect (wxPython behavior).
        
        Keyboard shortcuts:
        - Ctrl+B: Bold
        - Ctrl+I: Italic
        - Ctrl+U: Underline
        
        Screen readers should announce formatted text appropriately.
        """
        # Only apply formatting if user has selected text
        # This matches standard word processor behavior
        if format_type == 'bold':
            if self.richtext.HasSelection():
                self.richtext.ApplyBoldToSelection()
        elif format_type == 'italic':
            if self.richtext.HasSelection():
                self.richtext.ApplyItalicToSelection()
        elif format_type == 'underline':
            if self.richtext.HasSelection():
                self.richtext.ApplyUnderlineToSelection()
                
    # Event handlers
    
    def on_property_changed(self, event):
        """Handle property grid value change.
        
        Triggered when user modifies any property value.
        PropertyGrid validates input based on property type:
        - BoolProperty: checkbox toggle
        - StringProperty: text input
        - IntProperty: numeric input only
        - ColorProperty: color picker dialog
        - FontProperty: font picker dialog
        - EnumProperty: dropdown selection
        
        Screen readers announce property name and new value.
        """
        prop = event.GetProperty()
        if prop:
            name = prop.GetName()
            value = prop.GetValue()
            # Update label to show what was changed
            self.propgrid_label.SetLabel(f"Changed: {name} = {value}")
            # Update status bar for screen reader verification
            self.main_frame.update_status_bar(
                f"Property changed: {name}",
                f"New value: {value}",
                ""
            )
            
    def on_dataview_selection(self, event):
        """Handle data view selection change.
        
        DataViewCtrl supports multi-select (Ctrl+Click, Shift+Click, Ctrl+A).
        Updates display to show:
        - No selection: "No selection"
        - Single selection: Employee name and row number
        - Multiple selection: Count of selected rows
        
        Screen readers announce:
        - Row position ("Row X of Y")
        - Column values as user navigates
        - Selection count changes
        """
        # Get all selected items (can be multiple with Ctrl+Click)
        selections = self.dataview.GetSelections()
        count = len(selections)
        
        # Update display based on selection count
        if count == 0:
            self.dataview_label.SetLabel("No selection")
        elif count == 1:
            # Show details for single selection
            row = self.dataview.GetRow(selections[0])
            employee = self.dataview.GetTextValue(row, 1)  # Column 1 = Name
            self.dataview_label.SetLabel(f"Selected: {employee} (row {row + 1})")
        else:
            # Just show count for multiple selections
            self.dataview_label.SetLabel(f"{count} rows selected")
            
        # Update status bar with keyboard hints
        self.main_frame.update_status_bar(
            f"Data view selection: {count} item(s)",
            "",
            "Arrow keys, Space to select, Ctrl+A for all"
        )
        
    def on_dataview_activated(self, event):
        """Handle data view item activation (Enter key or double-click).
        
        Activation typically means "open" or "view details".
        Here we show a dialog with employee information.
        
        Keyboard: Enter key on selected row
        Mouse: Double-click on row
        
        Screen readers announce the row before activation,
        then read the dialog content.
        """
        item = event.GetItem()
        if item.IsOk():
            # Get row data from activated item
            row = self.dataview.GetRow(item)
            employee = self.dataview.GetTextValue(row, 1)  # Column 1 = Name
            dept = self.dataview.GetTextValue(row, 2)  # Column 2 = Department
            # Show details dialog
            wx.MessageBox(
                f"Employee: {employee}\nDepartment: {dept}",
                "Item Activated",
                wx.OK | wx.ICON_INFORMATION
            )
            
    def on_dataview_select_all(self, event):
        """Select all items in data view.
        
        Keyboard shortcut: Ctrl+A (standard)
        Tests multi-select behavior and selection announcements.
        Screen readers should announce total selection count.
        """
        self.dataview.SelectAll()
        
    def on_dataview_clear(self, event):
        """Clear data view selection.
        
        Useful for testing selection state changes.
        Screen readers should announce "no selection" or similar.
        """
        self.dataview.UnselectAll()
        self.dataview_label.SetLabel("Selection cleared")
        
    def on_load_media(self, event):
        """Load media file via file picker dialog.
        
        Opens file dialog to select audio/video file.
        Supported formats depend on system codecs:
        - Audio: MP3, WAV, WMA
        - Video: MP4, AVI, WMV
        
        After loading:
        - Enables Play and Stop buttons
        - Displays filename
        - Media ready for playback
        
        File dialog is fully keyboard accessible:
        - Tab to navigate controls
        - Type to search filenames
        - Enter to select
        - Esc to cancel
        """
        # Define file filters for media types
        wildcard = "Media files|*.mp3;*.mp4;*.wav;*.avi;*.wmv|All files|*.*"
        dlg = wx.FileDialog(
            self,
            "Choose a media file",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            # Attempt to load media (may fail for unsupported formats)
            if self.media.Load(path):
                self.media_label.SetLabel(f"Loaded: {os.path.basename(path)}")
                # Enable playback controls now that media is loaded
                self.play_btn.Enable(True)
                self.stop_btn.Enable(True)
            else:
                self.media_label.SetLabel("Failed to load media file")
                wx.MessageBox(
                    "Could not load the selected media file.",
                    "Load Error",
                    wx.OK | wx.ICON_ERROR
                )
        dlg.Destroy()
        
    def on_play_media(self, event):
        """Play loaded media.
        
        Starts or resumes playback from current position.
        Enables Pause button for playback control.
        
        Screen readers should announce "Playing" state.
        """
        if self.media.Play():
            self.media_label.SetLabel("Playing...")
            self.pause_btn.Enable(True)
            
    def on_pause_media(self, event):
        """Pause media playback.
        
        Pauses at current position. Play resumes from here.
        Different from Stop (which resets to beginning).
        
        Screen readers should announce "Paused" state.
        """
        if self.media.Pause():
            self.media_label.SetLabel("Paused")
            
    def on_stop_media(self, event):
        """Stop media playback.
        
        Stops playback and resets to beginning.
        Next Play will start from the start.
        Disables Pause button (no playback active).
        
        Screen readers should announce "Stopped" state.
        """
        if self.media.Stop():
            self.media_label.SetLabel("Stopped")
            self.pause_btn.Enable(False)
            
    def on_volume_changed(self, event):
        """Handle volume slider change.
        
        Volume range: 0-100 (slider) → 0.0-1.0 (MediaCtrl)
        Updates both media volume and status bar display.
        
        Keyboard shortcuts:
        - Arrow keys: Adjust volume
        - Page Up/Down: Larger adjustments
        - Home: Minimum (0)
        - End: Maximum (100)
        
        Screen readers announce volume percentage.
        """
        # Convert 0-100 range to 0.0-1.0 for MediaCtrl API
        volume = self.volume_slider.GetValue() / 100.0
        self.media.SetVolume(volume)
        self.main_frame.update_status_bar(
            "Volume control",
            f"Volume: {self.volume_slider.GetValue()}%",
            "Arrow keys to adjust"
        )
        
    def on_media_loaded(self, event):
        """Handle media loaded event.
        
        Triggered when media file finishes loading.
        Updates display to indicate media is ready for playback.
        Could be extended to show duration, metadata, etc.
        """
        self.media_label.SetLabel("Media loaded and ready")
        
    def on_media_state_changed(self, event):
        """Handle media state change.
        
        MediaCtrl states:
        - MEDIASTATE_STOPPED: Not playing, position at start
        - MEDIASTATE_PAUSED: Not playing, position maintained
        - MEDIASTATE_PLAYING: Actively playing
        
        Updates display to reflect current playback state.
        Screen readers should announce state changes.
        """
        state = self.media.GetState()
        if state == wx.media.MEDIASTATE_PLAYING:
            self.media_label.SetLabel("Playing...")
        elif state == wx.media.MEDIASTATE_PAUSED:
            self.media_label.SetLabel("Paused")
        elif state == wx.media.MEDIASTATE_STOPPED:
            self.media_label.SetLabel("Stopped")
            
    def on_control_focus(self, event):
        """Handle control focus events for status bar updates.
        
        Updates status bar when controls receive focus to show:
        - Control name and type
        - Expected screen reader announcements
        - Keyboard shortcuts
        
        Helps testers verify that screen readers are announcing
        controls correctly by comparing actual vs. expected output.
        """
        ctrl = event.GetEventObject()
        
        # Rich text editor with formatting support
        if isinstance(ctrl, rt.RichTextCtrl):
            self.main_frame.update_status_bar(
                "Rich text editor",
                "Role: Text editor, Supports formatting",
                "Ctrl+B bold, Ctrl+I italic, Ctrl+U underline"
            )
        # Property grid for structured data editing
        elif isinstance(ctrl, wxpg.PropertyGrid):
            self.main_frame.update_status_bar(
                "Property grid",
                "Role: Property sheet editor",
                "Arrow keys to navigate, Enter to edit, F4 for combos"
            )
        # Virtual list control with multi-select
        elif isinstance(ctrl, dv.DataViewListCtrl):
            selections = ctrl.GetSelectedItemsCount()
            self.main_frame.update_status_bar(
                "Data view control",
                f"Role: Virtual list, {selections} selected",
                "Arrow keys, Space to select, Ctrl+A for all"
            )
        # Media player control
        elif isinstance(ctrl, wx.media.MediaCtrl):
            state = ctrl.GetState()
            state_name = "Stopped"
            if state == wx.media.MEDIASTATE_PLAYING:
                state_name = "Playing"
            elif state == wx.media.MEDIASTATE_PAUSED:
                state_name = "Paused"
            self.main_frame.update_status_bar(
                "Media control",
                f"Role: Media player, State: {state_name}",
                "Use buttons to control playback"
            )
        # Media control buttons (Play, Pause, Stop, Load)
        elif isinstance(ctrl, wx.Button):
            label = ctrl.GetLabel()
            self.main_frame.update_status_bar(
                f"Button: {label}",
                "Role: Button",
                "Space to activate"
            )
        # Volume slider (0-100 range)
        elif isinstance(ctrl, wx.Slider):
            self.main_frame.update_status_bar(
                "Volume slider",
                f"Role: Slider, Value: {ctrl.GetValue()}%",
                "Arrow keys to adjust"
            )
            
        # Allow event to propagate for default focus behavior
        event.Skip()
        
    # State management
    def save_state(self):
        """Save tab state to JSON-serializable dictionary.
        
        Captures:
        - Rich text content (plain text, formatting lost)
        - Property grid values (all properties as strings)
        - Volume slider value (0-100)
        
        Note: Media playback state is not saved (intentional).
        User must reload media files on restart.
        
        Returns:
            dict: State dictionary for JSON serialization
        """
        # Extract all property values (skip category headers)
        props = {}
        iterator = self.propgrid.GetIterator()
        while not iterator.AtEnd():
            prop = iterator.GetProperty()
            if prop and not isinstance(prop, wxpg.PropertyCategory):
                # Convert all values to strings for JSON compatibility
                props[prop.GetName()] = str(prop.GetValue())
            iterator.Next()
                
        return {
            "richtext": self.richtext.GetValue(),
            "properties": props,
            "volume": self.volume_slider.GetValue()
        }
        
    def load_state(self, state):
        """Load tab state from saved dictionary.
        
        Restores:
        - Rich text content (plain text only)
        - Property grid values (with type conversion)
        - Volume slider and MediaCtrl volume
        
        Gracefully handles:
        - Missing state keys (optional restore)
        - Invalid property values (silently ignored)
        - Type conversion errors (property skipped)
        
        Args:
            state (dict): State dictionary from JSON
        """
        # Restore rich text content
        if "richtext" in state:
            self.richtext.SetValue(state["richtext"])
            
        # Restore property grid values with error handling
        if "properties" in state:
            for name, value in state["properties"].items():
                prop = self.propgrid.GetProperty(name)
                if not prop:
                    continue

                # Be defensive when restoring property values. Some property
                # types (e.g. FontProperty) expect complex wx objects and
                # attempting to SetValue() with a string (from older saves)
                # can trigger C++ assertions in the propgrid layer. To avoid
                # noisy assertion logs or crashes, detect properties whose
                # current value is a complex wx type and skip restoring from
                # plain strings.
                try:
                    cur_val = prop.GetValue()
                except Exception:
                    cur_val = None

                # If the property's current type is wx.Font and the saved
                # representation is a plain string, skip restoring it.
                if isinstance(cur_val, wx.Font) and isinstance(value, str):
                    continue

                # Otherwise try to set the value and catch any error. Use a
                # broad except to guard against underlying C++ assertion
                # conversions that raise non-ValueError exceptions.
                try:
                    prop.SetValue(value)
                except Exception:
                    # Skip properties that fail to restore
                    continue
                        
        # Restore volume (affects both slider and media control)
        if "volume" in state:
            self.volume_slider.SetValue(state["volume"])
            # Convert to 0.0-1.0 range for MediaCtrl
            self.media.SetVolume(state["volume"] / 100.0)
            
    def reset_to_defaults(self):
        """Reset all controls to default values.
        
        Restores:
        - Rich text to welcome message with formatting
        - Property grid to initial sample values
        - Volume to 50%
        - Media playback stopped
        - DataView selection cleared
        
        Used when "Reset All Tabs" is selected from menu.
        Provides clean state for fresh testing.
        """
        # Reset rich text with formatted welcome message
        self.richtext.Clear()
        self.richtext.BeginBold()
        self.richtext.WriteText("Welcome to Rich Text Editor\n\n")
        self.richtext.EndBold()
        self.richtext.WriteText("Sample formatted text...")
        
        # Reset property grid to initial sample values
        self.propgrid.GetProperty("Application Name").SetValue("Accessibility Test Suite")
        self.propgrid.GetProperty("Version").SetValue("1.0.0")
        self.propgrid.GetProperty("Auto Save").SetValue(True)
        
        # Reset media to stopped state with 50% volume
        self.media.Stop()
        self.volume_slider.SetValue(50)
        self.media.SetVolume(0.5)
        self.media_label.SetLabel("No media loaded")
        
        # Clear data view selection
        self.dataview.UnselectAll()
