"""Advanced Controls 4 Tab.

Tests for SplitterWindow, alternative notebook types, Wizard-like navigation,
ActivityIndicator, and specialized list controls.
"""

import wx
import wx.adv
import wx.lib.agw.flatnotebook as fnb
from state_manager import TabStateHelper


class AdvancedControls4Tab(wx.Panel, TabStateHelper):
    """Tab containing final set of advanced controls for accessibility testing."""
    
    def __init__(self, parent, main_frame):
        """Initialize advanced controls 4 tab and build UI controls."""
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Advanced Controls 4"
        
        # Main scrolled window
        scroll = wx.ScrolledWindow(self)
        scroll.SetScrollRate(10, 10)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Instructions
        inst_text = wx.StaticText(
            scroll,
            label="Final advanced controls: SplitterWindow (resizable panels), alternative notebook types "
                  "(ListBook, Choicebook), ActivityIndicator (loading spinner), and specialized list controls. "
                  "Test keyboard navigation, screen reader announcements, and complex layout interactions."
        )
        inst_text.Wrap(800)
        main_sizer.Add(inst_text, 0, wx.ALL | wx.EXPAND, 10)
        
        # Create control groups
        main_sizer.Add(self._create_splitter_group(scroll), 1, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_alternative_notebooks_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_activity_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_specialized_lists_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        
        scroll.SetSizer(main_sizer)
        
        # Outer sizer
        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        outer_sizer.Add(scroll, 1, wx.EXPAND)
        self.SetSizer(outer_sizer)
        
    def GetName(self):
        """Return human-readable tab name."""
        return self.tab_name
        
    def _create_splitter_group(self, parent):
        """Create SplitterWindow group.
        
        Tests resizable split panels:
        - Keyboard sash dragging (Shift+arrows when sash has focus)
        - Left/right or top/bottom panel focus
        - Minimum pane size enforcement
        - Screen reader announces split orientation
        """
        box = wx.StaticBox(parent, label="Splitter Window (Drag sash or Tab to panels)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Horizontal splitter
        self.splitter_h = wx.SplitterWindow(parent, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        
        # Left panel
        left_panel = wx.Panel(self.splitter_h)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(wx.StaticText(left_panel, label="Left Panel"), 0, wx.ALL, 5)
        self.splitter_left_text = wx.TextCtrl(
            left_panel,
            value="Content in left panel. Tab to navigate between panels.",
            style=wx.TE_MULTILINE
        )
        left_sizer.Add(self.splitter_left_text, 1, wx.ALL | wx.EXPAND, 5)
        left_panel.SetSizer(left_sizer)
        
        # Right panel with nested vertical splitter
        self.splitter_v = wx.SplitterWindow(self.splitter_h, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        
        # Top panel (of right side)
        top_panel = wx.Panel(self.splitter_v)
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(wx.StaticText(top_panel, label="Top Panel (Right Side)"), 0, wx.ALL, 5)
        self.splitter_top_text = wx.TextCtrl(
            top_panel,
            value="Nested splitter - vertical split",
            style=wx.TE_MULTILINE
        )
        top_sizer.Add(self.splitter_top_text, 1, wx.ALL | wx.EXPAND, 5)
        top_panel.SetSizer(top_sizer)
        
        # Bottom panel (of right side)
        bottom_panel = wx.Panel(self.splitter_v)
        bottom_sizer = wx.BoxSizer(wx.VERTICAL)
        bottom_sizer.Add(wx.StaticText(bottom_panel, label="Bottom Panel (Right Side)"), 0, wx.ALL, 5)
        self.splitter_bottom_text = wx.TextCtrl(
            bottom_panel,
            value="Drag sashes to resize panels",
            style=wx.TE_MULTILINE
        )
        bottom_sizer.Add(self.splitter_bottom_text, 1, wx.ALL | wx.EXPAND, 5)
        bottom_panel.SetSizer(bottom_sizer)
        
        # Initialize splitters
        self.splitter_v.SplitHorizontally(top_panel, bottom_panel, 100)
        self.splitter_v.SetMinimumPaneSize(50)
        
        self.splitter_h.SplitVertically(left_panel, self.splitter_v, 250)
        self.splitter_h.SetMinimumPaneSize(100)
        
        sizer.Add(self.splitter_h, 1, wx.ALL | wx.EXPAND, 5)
        
        info = wx.StaticText(
            parent,
            label="Keyboard: Tab between panels, Click/drag sash to resize. "
                  "Screen reader should announce panel changes and sash position."
        )
        info.Wrap(680)
        sizer.Add(info, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_alternative_notebooks_group(self, parent):
        """Create alternative notebook types.
        
        Tests different tab navigation patterns:
        - ListBook: Tabs in a list on the side
        - Choicebook: Tabs in a dropdown choice control
        - FlatNotebook: Modern flat-style tabs (from AGW library)
        """
        box = wx.StaticBox(parent, label="Alternative Notebook Types")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Create a panel to hold both notebooks side by side
        notebooks_panel = wx.Panel(parent)
        notebooks_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # ListBook
        listbook_panel = wx.Panel(notebooks_panel)
        listbook_sizer = wx.BoxSizer(wx.VERTICAL)
        listbook_sizer.Add(wx.StaticText(listbook_panel, label="ListBook (list on left):"), 0, wx.ALL, 5)
        
        self.listbook = wx.Listbook(listbook_panel, size=(350, 150))
        
        # Add pages to ListBook
        page1 = wx.Panel(self.listbook)
        wx.StaticText(page1, label="Page 1 content", pos=(10, 10))
        self.listbook_text1 = wx.TextCtrl(page1, value="Text in page 1", pos=(10, 40), size=(250, -1))
        self.listbook.AddPage(page1, "Page 1")
        
        page2 = wx.Panel(self.listbook)
        wx.StaticText(page2, label="Page 2 content", pos=(10, 10))
        self.listbook_check = wx.CheckBox(page2, label="Checkbox in page 2", pos=(10, 40))
        self.listbook.AddPage(page2, "Page 2")
        
        page3 = wx.Panel(self.listbook)
        wx.StaticText(page3, label="Page 3 content", pos=(10, 10))
        self.listbook_btn = wx.Button(page3, label="Button in page 3", pos=(10, 40))
        self.listbook.AddPage(page3, "Page 3")
        
        self.listbook.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.on_listbook_changed)
        
        listbook_sizer.Add(self.listbook, 1, wx.ALL | wx.EXPAND, 5)
        listbook_panel.SetSizer(listbook_sizer)
        notebooks_sizer.Add(listbook_panel, 1, wx.ALL | wx.EXPAND, 5)
        
        # Choicebook
        choicebook_panel = wx.Panel(notebooks_panel)
        choicebook_sizer = wx.BoxSizer(wx.VERTICAL)
        choicebook_sizer.Add(wx.StaticText(choicebook_panel, label="Choicebook (dropdown):"), 0, wx.ALL, 5)
        
        self.choicebook = wx.Choicebook(choicebook_panel, size=(350, 150))
        
        # Add pages to Choicebook
        cb_page1 = wx.Panel(self.choicebook)
        wx.StaticText(cb_page1, label="Option A content", pos=(10, 10))
        self.choicebook_spin = wx.SpinCtrl(cb_page1, value="50", pos=(10, 40))
        self.choicebook.AddPage(cb_page1, "Option A")
        
        cb_page2 = wx.Panel(self.choicebook)
        wx.StaticText(cb_page2, label="Option B content", pos=(10, 10))
        self.choicebook_slider = wx.Slider(cb_page2, value=75, minValue=0, maxValue=100, pos=(10, 40), size=(200, -1))
        self.choicebook.AddPage(cb_page2, "Option B")
        
        self.choicebook.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.on_choicebook_changed)
        
        choicebook_sizer.Add(self.choicebook, 1, wx.ALL | wx.EXPAND, 5)
        choicebook_panel.SetSizer(choicebook_sizer)
        notebooks_sizer.Add(choicebook_panel, 1, wx.ALL | wx.EXPAND, 5)
        
        notebooks_panel.SetSizer(notebooks_sizer)
        sizer.Add(notebooks_panel, 0, wx.ALL | wx.EXPAND, 5)
        
        self.alt_notebook_label = wx.StaticText(parent, label="ListBook: Page 1, Choicebook: Option A")
        sizer.Add(self.alt_notebook_label, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_activity_group(self, parent):
        """Create ActivityIndicator group.
        
        Tests loading/busy indicators:
        - Start/stop animation
        - Screen reader announces "busy" state
        - Keyboard control of animation
        """
        box = wx.StaticBox(parent, label="Activity Indicator (Loading Spinner)")
        sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        # Activity indicator
        self.activity = wx.ActivityIndicator(parent)
        self.activity.SetToolTip("Loading indicator - announces busy state to screen readers")
        sizer.Add(self.activity, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        # Controls
        controls_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.activity_start_btn = wx.Button(parent, label="&Start Animation")
        self.activity_start_btn.Bind(wx.EVT_BUTTON, self.on_activity_start)
        controls_sizer.Add(self.activity_start_btn, 0, wx.ALL, 5)
        
        self.activity_stop_btn = wx.Button(parent, label="S&top Animation")
        self.activity_stop_btn.Bind(wx.EVT_BUTTON, self.on_activity_stop)
        controls_sizer.Add(self.activity_stop_btn, 0, wx.ALL, 5)
        
        self.activity_label = wx.StaticText(parent, label="Status: Stopped")
        controls_sizer.Add(self.activity_label, 0, wx.ALL, 5)
        
        info = wx.StaticText(
            parent,
            label="Screen readers should announce 'busy' when running. "
                  "Used to indicate background operations."
        )
        info.Wrap(400)
        controls_sizer.Add(info, 0, wx.ALL, 5)
        
        sizer.Add(controls_sizer, 1, wx.ALL | wx.EXPAND, 5)
        
        return sizer
        
    def _create_specialized_lists_group(self, parent):
        """Create specialized list controls.
        
        Tests advanced list patterns:
        - EditableListBox: List with Add/Remove/Edit buttons
        - RearrangeCtrl: List with up/down reorder buttons
        """
        box = wx.StaticBox(parent, label="Specialized List Controls")
        sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        # EditableListBox
        editable_panel = wx.Panel(parent)
        editable_sizer = wx.BoxSizer(wx.VERTICAL)
        editable_sizer.Add(wx.StaticText(editable_panel, label="EditableListBox:"), 0, wx.ALL, 5)
        
        self.editable_list = wx.adv.EditableListBox(
            editable_panel,
            label="Items (New/Edit/Delete buttons)",
            size=(300, 200)
        )
        # Populate with sample items
        self.editable_list.SetStrings(["Item 1", "Item 2", "Item 3", "Item 4"])
        editable_sizer.Add(self.editable_list, 1, wx.ALL | wx.EXPAND, 5)
        
        editable_panel.SetSizer(editable_sizer)
        sizer.Add(editable_panel, 1, wx.ALL | wx.EXPAND, 5)
        
        # RearrangeCtrl
        rearrange_panel = wx.Panel(parent)
        rearrange_sizer = wx.BoxSizer(wx.VERTICAL)
        rearrange_sizer.Add(wx.StaticText(rearrange_panel, label="RearrangeCtrl:"), 0, wx.ALL, 5)
        
        # Populate with sample items (order, label)
        items = [
            (0, "First Priority"),
            (1, "Second Priority"),
            (2, "Third Priority"),
            (3, "Fourth Priority")
        ]
        self.rearrange = wx.RearrangeCtrl(
            rearrange_panel,
            size=(300, 200),
            order=[order for order, _ in items],
            items=[label for _, label in items]
        )
        
        rearrange_sizer.Add(self.rearrange, 1, wx.ALL | wx.EXPAND, 5)
        
        info = wx.StaticText(
            rearrange_panel,
            label="Use Move Up/Down buttons or drag to reorder"
        )
        info.Wrap(280)
        rearrange_sizer.Add(info, 0, wx.ALL, 5)
        
        rearrange_panel.SetSizer(rearrange_sizer)
        sizer.Add(rearrange_panel, 1, wx.ALL | wx.EXPAND, 5)
        
        return sizer
        
    # Event handlers
    def on_listbook_changed(self, event):
        """Handle listbook page change."""
        sel = self.listbook.GetSelection()
        page_text = self.listbook.GetPageText(sel)
        self._update_alt_notebook_label()
        self.main_frame.update_status_bar(
            "ListBook",
            f"Page: {page_text}",
            "Arrow keys in list to switch pages, Tab for content"
        )
        event.Skip()
        
    def on_choicebook_changed(self, event):
        """Handle choicebook page change."""
        sel = self.choicebook.GetSelection()
        page_text = self.choicebook.GetPageText(sel)
        self._update_alt_notebook_label()
        self.main_frame.update_status_bar(
            "Choicebook",
            f"Option: {page_text}",
            "Alt+Down to open dropdown, Arrow keys to select, Tab for content"
        )
        event.Skip()
        
    def _update_alt_notebook_label(self):
        """Update status label for alternative notebooks."""
        lb_sel = self.listbook.GetSelection()
        cb_sel = self.choicebook.GetSelection()
        lb_text = self.listbook.GetPageText(lb_sel) if lb_sel >= 0 else "None"
        cb_text = self.choicebook.GetPageText(cb_sel) if cb_sel >= 0 else "None"
        self.alt_notebook_label.SetLabel(f"ListBook: {lb_text}, Choicebook: {cb_text}")
        
    def on_activity_start(self, event):
        """Start activity indicator animation."""
        self.activity.Start()
        self.activity_label.SetLabel("Status: Running (Busy)")
        self.main_frame.update_status_bar(
            "Activity Indicator",
            "Busy - animation running",
            "Screen reader should announce busy state"
        )
        
    def on_activity_stop(self, event):
        """Stop activity indicator animation."""
        self.activity.Stop()
        self.activity_label.SetLabel("Status: Stopped")
        self.main_frame.update_status_bar(
            "Activity Indicator",
            "Idle - animation stopped",
            ""
        )
        
    # State management
    def save_state(self):
        """Save tab state."""
        return {
            "splitter_h_pos": self.splitter_h.GetSashPosition(),
            "splitter_v_pos": self.splitter_v.GetSashPosition(),
            "splitter_left_text": self.splitter_left_text.GetValue(),
            "splitter_top_text": self.splitter_top_text.GetValue(),
            "splitter_bottom_text": self.splitter_bottom_text.GetValue(),
            "listbook_selection": self.listbook.GetSelection(),
            "listbook_text1": self.listbook_text1.GetValue(),
            "listbook_check": self.listbook_check.GetValue(),
            "choicebook_selection": self.choicebook.GetSelection(),
            "choicebook_spin": self.choicebook_spin.GetValue(),
            "choicebook_slider": self.choicebook_slider.GetValue(),
            "activity_running": self.activity.IsRunning(),
            "editable_list_items": list(self.editable_list.GetStrings()),
            "rearrange_items": list(self.rearrange.GetItems())
        }
        
    def load_state(self, state):
        """Load tab state."""
        if "splitter_h_pos" in state:
            self.splitter_h.SetSashPosition(state["splitter_h_pos"])
            
        if "splitter_v_pos" in state:
            self.splitter_v.SetSashPosition(state["splitter_v_pos"])
            
        if "splitter_left_text" in state:
            self.splitter_left_text.SetValue(state["splitter_left_text"])
            
        if "splitter_top_text" in state:
            self.splitter_top_text.SetValue(state["splitter_top_text"])
            
        if "splitter_bottom_text" in state:
            self.splitter_bottom_text.SetValue(state["splitter_bottom_text"])
            
        if "listbook_selection" in state:
            sel = state["listbook_selection"]
            if 0 <= sel < self.listbook.GetPageCount():
                self.listbook.SetSelection(sel)
                
        if "listbook_text1" in state:
            self.listbook_text1.SetValue(state["listbook_text1"])
            
        if "listbook_check" in state:
            self.listbook_check.SetValue(state["listbook_check"])
            
        if "choicebook_selection" in state:
            sel = state["choicebook_selection"]
            if 0 <= sel < self.choicebook.GetPageCount():
                self.choicebook.SetSelection(sel)
                
        if "choicebook_spin" in state:
            self.choicebook_spin.SetValue(state["choicebook_spin"])
            
        if "choicebook_slider" in state:
            self.choicebook_slider.SetValue(state["choicebook_slider"])
            
        if "activity_running" in state and state["activity_running"]:
            self.activity.Start()
            self.activity_label.SetLabel("Status: Running (Busy)")
        else:
            self.activity.Stop()
            self.activity_label.SetLabel("Status: Stopped")
            
        if "editable_list_items" in state:
            self.editable_list.SetStrings(state["editable_list_items"])
            
        if "rearrange_items" in state:
            self.rearrange.SetItems(state["rearrange_items"])
            
        self._update_alt_notebook_label()
                
    def reset_to_defaults(self):
        """Reset tab to default state."""
        self.splitter_h.SetSashPosition(250)
        self.splitter_v.SetSashPosition(100)
        self.splitter_left_text.SetValue("Content in left panel. Tab to navigate between panels.")
        self.splitter_top_text.SetValue("Nested splitter - vertical split")
        self.splitter_bottom_text.SetValue("Drag sashes to resize panels")
        self.listbook.SetSelection(0)
        self.listbook_text1.SetValue("Text in page 1")
        self.listbook_check.SetValue(False)
        self.choicebook.SetSelection(0)
        self.choicebook_spin.SetValue(50)
        self.choicebook_slider.SetValue(75)
        self.activity.Stop()
        self.activity_label.SetLabel("Status: Stopped")
        self.editable_list.SetStrings(["Item 1", "Item 2", "Item 3", "Item 4"])
        self.rearrange.SetItems(["First Priority", "Second Priority", "Third Priority", "Fourth Priority"])
        self._update_alt_notebook_label()
