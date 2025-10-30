"""
Media & Link Controls Tab
==========================
Tests for media, hyperlink, and specialized picker controls.
"""

import wx
import wx.adv
from state_manager import TabStateHelper


class MediaControlsTab(wx.Panel, TabStateHelper):
    """Tab containing media, hyperlink, and picker controls."""
    
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Media & Link Controls"
        
        scroll = wx.ScrolledWindow(self, style=wx.VSCROLL)
        scroll.SetScrollRate(0, 20)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add control groups
        main_sizer.Add(self._create_hyperlink_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_search_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_additional_pickers_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_time_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_calendar_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        
        scroll.SetSizer(main_sizer)
        
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(scroll, 1, wx.EXPAND)
        self.SetSizer(panel_sizer)
        
    def GetName(self):
        return self.tab_name
        
    def _create_hyperlink_group(self, parent):
        """Create hyperlink control group."""
        box = wx.StaticBox(parent, label="Hyperlink Controls (Enter to activate)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(wx.StaticText(parent, label="Test hyperlinks for screen reader announcement:"), 0, wx.ALL, 5)
        
        # External link
        self.hyperlink1 = wx.adv.HyperlinkCtrl(
            parent,
            id=wx.ID_ANY,
            label="Visit &wxPython Documentation",
            url="https://docs.wxpython.org/"
        )
        self.hyperlink1.SetToolTip("Press Enter to open link in browser")
        self.hyperlink1.Bind(wx.adv.EVT_HYPERLINK, self.on_hyperlink_click)
        self.hyperlink1.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.hyperlink1, 0, wx.ALL, 5)
        
        # GitHub link
        self.hyperlink2 = wx.adv.HyperlinkCtrl(
            parent,
            id=wx.ID_ANY,
            label="wxPython on &GitHub",
            url="https://github.com/wxWidgets/Phoenix"
        )
        self.hyperlink2.Bind(wx.adv.EVT_HYPERLINK, self.on_hyperlink_click)
        self.hyperlink2.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.hyperlink2, 0, wx.ALL, 5)
        
        # WCAG Guidelines link
        self.hyperlink3 = wx.adv.HyperlinkCtrl(
            parent,
            id=wx.ID_ANY,
            label="WCAG 2.2 AA &Guidelines",
            url="https://www.w3.org/WAI/WCAG22/quickref/"
        )
        self.hyperlink3.Bind(wx.adv.EVT_HYPERLINK, self.on_hyperlink_click)
        self.hyperlink3.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.hyperlink3, 0, wx.ALL, 5)
        
        # Note about screen reader behavior
        note = wx.StaticText(
            parent,
            label="Note: Screen readers should announce role as 'link' and URL destination."
        )
        note.Wrap(600)
        font = note.GetFont()
        font.SetPointSize(font.GetPointSize() - 1)
        note.SetFont(font)
        sizer.Add(note, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_search_group(self, parent):
        """Create search control group."""
        box = wx.StaticBox(parent, label="Search Controls (Type to search)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Search control with cancel button
        sizer.Add(wx.StaticText(parent, label="&Search Tasks:"), 0, wx.ALL, 5)
        
        self.search_ctrl1 = wx.SearchCtrl(parent, size=(300, -1))
        self.search_ctrl1.ShowCancelButton(True)
        self.search_ctrl1.ShowSearchButton(True)
        self.search_ctrl1.SetDescriptiveText("Enter search terms...")
        self.search_ctrl1.SetToolTip("Type to search, Esc to clear")
        self.search_ctrl1.Bind(wx.EVT_TEXT, self.on_search_text)
        self.search_ctrl1.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.on_search_button)
        self.search_ctrl1.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.on_search_cancel)
        self.search_ctrl1.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.search_ctrl1, 0, wx.ALL | wx.EXPAND, 5)
        
        # Search control with menu
        sizer.Add(wx.StaticText(parent, label="Search with &Filter Menu:"), 0, wx.ALL, 5)
        
        self.search_ctrl2 = wx.SearchCtrl(parent, size=(300, -1), style=wx.TE_PROCESS_ENTER)
        self.search_ctrl2.ShowSearchButton(True)
        self.search_ctrl2.SetDescriptiveText("Search with filters...")
        
        # Add search menu
        search_menu = wx.Menu()
        search_menu.AppendRadioItem(wx.ID_ANY, "Search All")
        search_menu.AppendRadioItem(wx.ID_ANY, "Search Tasks Only")
        search_menu.AppendRadioItem(wx.ID_ANY, "Search Documents Only")
        search_menu.AppendRadioItem(wx.ID_ANY, "Search People Only")
        search_menu.Check(search_menu.FindItemByPosition(0).GetId(), True)
        self.search_ctrl2.SetMenu(search_menu)
        
        self.search_ctrl2.Bind(wx.EVT_TEXT, self.on_search_text)
        self.search_ctrl2.Bind(wx.EVT_TEXT_ENTER, self.on_search_enter)
        self.search_ctrl2.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.search_ctrl2, 0, wx.ALL | wx.EXPAND, 5)
        
        # Results display
        self.search_results = wx.StaticText(parent, label="Search results will appear here")
        self.search_results.SetForegroundColour(wx.Colour(100, 100, 100))
        sizer.Add(self.search_results, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_additional_pickers_group(self, parent):
        """Create additional picker controls."""
        box = wx.StaticBox(parent, label="Additional Pickers (Space/Enter to open)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Directory picker
        sizer.Add(wx.StaticText(parent, label="&Directory Picker:"), 0, wx.ALL, 5)
        self.dir_picker = wx.DirPickerCtrl(
            parent,
            message="Select a directory",
            style=wx.DIRP_USE_TEXTCTRL
        )
        self.dir_picker.SetToolTip("Space/Enter to browse for directory")
        self.dir_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_dir_changed)
        self.dir_picker.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.dir_picker, 0, wx.ALL | wx.EXPAND, 5)
        
        # Font picker
        sizer.Add(wx.StaticText(parent, label="&Font Picker:"), 0, wx.ALL, 5)
        self.font_picker = wx.FontPickerCtrl(parent)
        self.font_picker.SetSelectedFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.font_picker.SetToolTip("Space/Enter to open font dialog")
        self.font_picker.Bind(wx.EVT_FONTPICKER_CHANGED, self.on_font_changed)
        self.font_picker.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.font_picker, 0, wx.ALL | wx.EXPAND, 5)
        
        # Font display
        self.font_display = wx.StaticText(
            parent,
            label="Sample text in selected font"
        )
        sizer.Add(self.font_display, 0, wx.ALL, 5)
        self._update_font_display()
        
        return sizer
        
    def _create_time_group(self, parent):
        """Create time picker control group."""
        box = wx.StaticBox(parent, label="Time Picker (Arrow keys to adjust)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(wx.StaticText(parent, label="Select &Time:"), 0, wx.ALL, 5)
        
        self.time_picker = wx.adv.TimePickerCtrl(parent)
        # Set initial time to current time
        now = wx.DateTime.Now()
        self.time_picker.SetTime(now.GetHour(), now.GetMinute(), now.GetSecond())
        self.time_picker.SetToolTip("Arrow keys to adjust time, Tab between hours/minutes")
        self.time_picker.Bind(wx.adv.EVT_TIME_CHANGED, self.on_time_changed)
        self.time_picker.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.time_picker, 0, wx.ALL | wx.EXPAND, 5)
        
        # Time display
        self.time_display = wx.StaticText(parent, label="")
        self._update_time_display()
        sizer.Add(self.time_display, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_calendar_group(self, parent):
        """Create calendar control group."""
        box = wx.StaticBox(parent, label="Calendar Control (Arrow keys to navigate)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="Full calendar view - use arrow keys to navigate dates, "
                      "Page Up/Down for months, Space to select:"
            ),
            0, wx.ALL, 5
        )
        
        self.calendar = wx.adv.CalendarCtrl(
            parent,
            style=wx.adv.CAL_SHOW_HOLIDAYS | wx.adv.CAL_MONDAY_FIRST
        )
        self.calendar.SetToolTip(
            "Arrow keys to navigate days, Page Up/Down for months, "
            "Ctrl+Page Up/Down for years, Home for today"
        )
        self.calendar.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.on_calendar_changed)
        self.calendar.Bind(wx.adv.EVT_CALENDAR_DAY, self.on_calendar_day)
        self.calendar.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        sizer.Add(self.calendar, 0, wx.ALL, 5)
        
        # Selected date display
        self.calendar_display = wx.StaticText(parent, label="")
        self._update_calendar_display()
        sizer.Add(self.calendar_display, 0, wx.ALL, 5)
        
        return sizer
        
    def _update_font_display(self):
        """Update font display text."""
        font = self.font_picker.GetSelectedFont()
        self.font_display.SetFont(font)
        
        font_desc = f"{font.GetFaceName()}, {font.GetPointSize()}pt"
        if font.GetWeight() == wx.FONTWEIGHT_BOLD:
            font_desc += ", Bold"
        if font.GetStyle() == wx.FONTSTYLE_ITALIC:
            font_desc += ", Italic"
            
        self.font_display.SetLabel(f"Sample text - {font_desc}")
        
    def _update_time_display(self):
        """Update time display.
        
        GetTime() returns a tuple (hour, minute, second) in 24-hour format.
        Formats as HH:MM:SS for display.
        """
        time = self.time_picker.GetTime()
        # GetTime() returns tuple (hour, minute, second)
        self.time_display.SetLabel(
            f"Selected time: {time[0]:02d}:{time[1]:02d}:{time[2]:02d}"
        )
        
    def _update_calendar_display(self):
        """Update calendar display."""
        date = self.calendar.GetDate()
        self.calendar_display.SetLabel(
            f"Selected date: {date.FormatISODate()} ({date.GetWeekDayName(date.GetWeekDay())})"
        )
        
    # Event handlers
    def on_hyperlink_click(self, event):
        """Handle hyperlink activation."""
        # Note: Default behavior opens URL in browser
        # We'll just update status bar
        link = event.GetEventObject()
        self.main_frame.update_status_bar(
            f"Hyperlink activated",
            f"Opening: {link.GetURL()}",
            ""
        )
        event.Skip()
        
    def on_search_text(self, event):
        """Handle search text change."""
        ctrl = event.GetEventObject()
        text = ctrl.GetValue()
        
        if text:
            # Simulate search results
            results = [
                "Task: Review documentation",
                "Task: Update requirements",
                "Document: Project Plan.pdf",
                "Person: John Smith"
            ]
            matching = [r for r in results if text.lower() in r.lower()]
            
            if matching:
                self.search_results.SetLabel(f"Found {len(matching)} result(s): {', '.join(matching[:3])}")
            else:
                self.search_results.SetLabel("No results found")
        else:
            self.search_results.SetLabel("Search results will appear here")
            
        self.main_frame.update_status_bar(
            "Search control",
            f"Text: {text if text else '(empty)'}",
            "Type to search, Esc to clear"
        )
        
    def on_search_button(self, event):
        """Handle search button click."""
        text = self.search_ctrl1.GetValue()
        self.main_frame.update_status_bar(
            "Search initiated",
            f"Searching for: {text}",
            ""
        )
        
    def on_search_cancel(self, event):
        """Handle search cancel button."""
        self.search_ctrl1.SetValue("")
        self.search_results.SetLabel("Search cleared")
        self.main_frame.update_status_bar(
            "Search cleared",
            "",
            ""
        )
        
    def on_search_enter(self, event):
        """Handle Enter key in search control."""
        text = self.search_ctrl2.GetValue()
        self.main_frame.update_status_bar(
            "Search submitted",
            f"Searching: {text}",
            ""
        )
        
    def on_dir_changed(self, event):
        """Handle directory picker change."""
        path = self.dir_picker.GetPath()
        self.main_frame.update_status_bar(
            "Directory selected",
            f"Path: {path}",
            ""
        )
        
    def on_font_changed(self, event):
        """Handle font picker change."""
        self._update_font_display()
        font = self.font_picker.GetSelectedFont()
        self.main_frame.update_status_bar(
            "Font changed",
            f"Font: {font.GetFaceName()}, {font.GetPointSize()}pt",
            ""
        )
        
    def on_time_changed(self, event):
        """Handle time picker change."""
        self._update_time_display()
        time = self.time_picker.GetTime()
        # GetTime() returns tuple (hour, minute, second)
        self.main_frame.update_status_bar(
            "Time changed",
            f"Time: {time[0]:02d}:{time[1]:02d}",
            ""
        )
        
    def on_calendar_changed(self, event):
        """Handle calendar selection change."""
        self._update_calendar_display()
        
    def on_calendar_day(self, event):
        """Handle calendar day change."""
        date = self.calendar.GetDate()
        self.main_frame.update_status_bar(
            "Calendar",
            f"Date: {date.FormatISODate()}",
            "Arrow keys to navigate, Page Up/Down for months"
        )
        
    def on_control_focus(self, event):
        """Handle focus events."""
        ctrl = event.GetEventObject()
        
        if isinstance(ctrl, wx.adv.HyperlinkCtrl):
            self.main_frame.update_status_bar(
                f"Hyperlink: {ctrl.GetLabel()}",
                f"Role: Link, URL: {ctrl.GetURL()}",
                "Enter to activate link"
            )
        elif isinstance(ctrl, wx.SearchCtrl):
            self.main_frame.update_status_bar(
                "Search control",
                f"Role: Search box, Value: {ctrl.GetValue()}",
                "Type to search, Esc to clear"
            )
        elif isinstance(ctrl, wx.DirPickerCtrl):
            self.main_frame.update_status_bar(
                "Directory picker",
                f"Role: Directory picker, Path: {ctrl.GetPath() or '(none)'}",
                "Space/Enter to browse"
            )
        elif isinstance(ctrl, wx.FontPickerCtrl):
            font = ctrl.GetSelectedFont()
            self.main_frame.update_status_bar(
                "Font picker",
                f"Role: Font picker, Font: {font.GetFaceName()}",
                "Space/Enter to select font"
            )
        elif isinstance(ctrl, wx.adv.TimePickerCtrl):
            time = ctrl.GetTime()
            # GetTime() returns tuple (hour, minute, second)
            self.main_frame.update_status_bar(
                "Time picker",
                f"Role: Time picker, Time: {time[0]:02d}:{time[1]:02d}",
                "Arrow keys to adjust, Tab between fields"
            )
        elif isinstance(ctrl, wx.adv.CalendarCtrl):
            date = ctrl.GetDate()
            self.main_frame.update_status_bar(
                "Calendar",
                f"Role: Calendar, Date: {date.FormatISODate()}",
                "Arrow keys, Page Up/Down, Home for today"
            )
            
        event.Skip()
        
    # State management
    def save_state(self):
        """Save tab state."""
        return {
            "search1": self.search_ctrl1.GetValue(),
            "search2": self.search_ctrl2.GetValue(),
            "dir_path": self.dir_picker.GetPath(),
            "font": {
                "face": self.font_picker.GetSelectedFont().GetFaceName(),
                "size": self.font_picker.GetSelectedFont().GetPointSize(),
                "weight": self.font_picker.GetSelectedFont().GetWeight(),
                "style": self.font_picker.GetSelectedFont().GetStyle()
            },
            "time": {
                "hour": self.time_picker.GetTime()[0],
                "minute": self.time_picker.GetTime()[1],
                "second": self.time_picker.GetTime()[2]
            },
            "calendar": self.calendar.GetDate().FormatISODate()
        }
        
    def load_state(self, state):
        """Load tab state."""
        if "search1" in state:
            self.search_ctrl1.SetValue(state["search1"])
        if "search2" in state:
            self.search_ctrl2.SetValue(state["search2"])
        if "dir_path" in state:
            self.dir_picker.SetPath(state["dir_path"])
            
        if "font" in state:
            font = wx.Font(
                state["font"]["size"],
                wx.FONTFAMILY_DEFAULT,
                state["font"]["style"],
                state["font"]["weight"],
                faceName=state["font"]["face"]
            )
            self.font_picker.SetSelectedFont(font)
            self._update_font_display()
            
        if "time" in state:
            # SetTime expects tuple (hour, minute, second)
            self.time_picker.SetTime(
                state["time"]["hour"],
                state["time"]["minute"],
                state["time"]["second"]
            )
            self._update_time_display()
            
        if "calendar" in state:
            dt = wx.DateTime()
            dt.ParseISODate(state["calendar"])
            self.calendar.SetDate(dt)
            self._update_calendar_display()
            
    def reset_to_defaults(self):
        """Reset to defaults."""
        self.search_ctrl1.SetValue("")
        self.search_ctrl2.SetValue("")
        self.dir_picker.SetPath("")
        
        default_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.font_picker.SetSelectedFont(default_font)
        self._update_font_display()
        
        now = wx.DateTime.Now()
        self.time_picker.SetTime(now.GetHour(), now.GetMinute(), now.GetSecond())
        self._update_time_display()
        
        self.calendar.SetDate(wx.DateTime.Today())
        self._update_calendar_display()
