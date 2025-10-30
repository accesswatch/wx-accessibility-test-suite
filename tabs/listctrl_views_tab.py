"""
ListCtrl Views Tab
==================
Tests for wx.ListCtrl with multiple view modes: Report, List, Icon, Small Icon.
Demonstrates view switching and accessibility across different display modes.
Tests controls WITHOUT checkboxes to verify pure list/icon navigation.
"""

import wx
from state_manager import TabStateHelper
from test_data import generate_task_list


class ListCtrlViewsTab(wx.Panel, TabStateHelper):
    """Tab containing ListCtrl with switchable views (NO checkboxes)."""
    
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "ListCtrl Multiple Views"
        # Generate 100 tasks for adequate scrolling and navigation testing
        # More data helps test: scrolling behavior, selection tracking, search/filter
        self.tasks = generate_task_list(100)
        self.current_view = "Report"
        
        # Create image list for icon views
        self.image_list = wx.ImageList(32, 32)
        self._create_icons()
        
        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Instructions
        inst_text = wx.StaticText(
            self,
            label="ListCtrl with multiple view modes. No checkboxes - tests pure navigation. "
                  "Switch views to test accessibility in Report, List, Icon, and Small Icon modes. "
                  "Arrow keys navigate, Enter activates, F2 to edit (in Report view)."
        )
        inst_text.Wrap(800)
        main_sizer.Add(inst_text, 0, wx.ALL | wx.EXPAND, 10)
        
        # View selection buttons
        view_sizer = wx.BoxSizer(wx.HORIZONTAL)
        view_sizer.Add(wx.StaticText(self, label="View Mode:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        
        self.report_btn = wx.Button(self, label="&Report View")
        self.report_btn.Bind(wx.EVT_BUTTON, lambda e: self._switch_view("Report"))
        view_sizer.Add(self.report_btn, 0, wx.ALL, 5)
        
        self.list_btn = wx.Button(self, label="&List View")
        self.list_btn.Bind(wx.EVT_BUTTON, lambda e: self._switch_view("List"))
        view_sizer.Add(self.list_btn, 0, wx.ALL, 5)
        
        self.icon_btn = wx.Button(self, label="&Icon View")
        self.icon_btn.Bind(wx.EVT_BUTTON, lambda e: self._switch_view("Icon"))
        view_sizer.Add(self.icon_btn, 0, wx.ALL, 5)
        
        self.small_icon_btn = wx.Button(self, label="&Small Icon View")
        self.small_icon_btn.Bind(wx.EVT_BUTTON, lambda e: self._switch_view("SmallIcon"))
        view_sizer.Add(self.small_icon_btn, 0, wx.ALL, 5)
        
        main_sizer.Add(view_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # Create ListCtrl (start in Report view)
        self.list_ctrl = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_SUNKEN | wx.LC_EDIT_LABELS
        )
        
        # Set image lists for icon views
        self.list_ctrl.SetImageList(self.image_list, wx.IMAGE_LIST_NORMAL)
        self.list_ctrl.SetImageList(self.image_list, wx.IMAGE_LIST_SMALL)
        
        # Initial setup in Report view
        self._setup_report_view()
        
        # Bind events
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated)
        self.list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_click)
        self.list_ctrl.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        main_sizer.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 10)
        
        # Status info
        self.info_label = wx.StaticText(
            self,
            label=f"View: {self.current_view} | Total items: {len(self.tasks)}"
        )
        main_sizer.Add(self.info_label, 0, wx.ALL, 10)
        
        self.SetSizer(main_sizer)
        
    def GetName(self):
        return self.tab_name
        
    def _create_icons(self):
        """Create simple colored icons for Icon/Small Icon views.
        
        Creates visual indicators for different priorities:
        - High: Red circle
        - Medium: Yellow circle
        - Low: Green circle
        
        In a real app, would use actual icon files or art provider.
        """
        colors = {
            'High': wx.RED,
            'Medium': wx.Colour(255, 165, 0),  # Orange
            'Low': wx.GREEN,
            'Critical': wx.Colour(139, 0, 0)  # Dark red
        }
        
        for priority, color in colors.items():
            bmp = wx.Bitmap(32, 32)
            dc = wx.MemoryDC(bmp)
            dc.SetBackground(wx.Brush(wx.WHITE))
            dc.Clear()
            dc.SetBrush(wx.Brush(color))
            dc.SetPen(wx.Pen(color))
            dc.DrawCircle(16, 16, 12)
            dc.SelectObject(wx.NullBitmap)
            self.image_list.Add(bmp)
            
    def _get_priority_icon_index(self, priority):
        """Map priority to icon index.
        
        Returns:
            int: Icon index in image list (0-3)
        """
        priority_map = {'High': 0, 'Medium': 1, 'Low': 2, 'Critical': 3}
        return priority_map.get(priority, 2)  # Default to Low (green)
        
    def _setup_report_view(self):
        """Setup Report view (multi-column table).
        
        Report view features:
        - Multiple columns with headers
        - Sortable by clicking headers
        - Cell navigation with arrows
        - Best for detailed data
        
        Screen readers announce:
        - Column headers
        - Row position
        - Cell values
        """
        self.list_ctrl.ClearAll()
        
        # Add columns
        self.list_ctrl.AppendColumn("Task", width=250)
        self.list_ctrl.AppendColumn("Assignee", width=150)
        self.list_ctrl.AppendColumn("Priority", width=80)
        self.list_ctrl.AppendColumn("Status", width=120)
        self.list_ctrl.AppendColumn("Due Date", width=100)
        
        # Populate with data
        for idx, task in enumerate(self.tasks):
            icon_idx = self._get_priority_icon_index(task['priority'])
            index = self.list_ctrl.InsertItem(idx, task['task'], icon_idx)
            self.list_ctrl.SetItem(index, 1, task['assignee'])
            self.list_ctrl.SetItem(index, 2, task['priority'])
            self.list_ctrl.SetItem(index, 3, task['status'])
            self.list_ctrl.SetItem(index, 4, task['due_date'])
            self.list_ctrl.SetItemData(index, idx)
            
    def _setup_list_view(self):
        """Setup List view (single column, vertical).
        
        List view features:
        - Single column (labels only)
        - Simple vertical list
        - Compact display
        - Best for simple item selection
        
        Screen readers announce:
        - Item label
        - Position (e.g., "3 of 50")
        """
        self.list_ctrl.ClearAll()
        
        # No columns in List view, just items
        for idx, task in enumerate(self.tasks):
            icon_idx = self._get_priority_icon_index(task['priority'])
            # Show task name and assignee in label
            label = f"{task['task']} - {task['assignee']}"
            index = self.list_ctrl.InsertItem(idx, label, icon_idx)
            self.list_ctrl.SetItemData(index, idx)
            
    def _setup_icon_view(self):
        """Setup Icon view (large icons with labels).
        
        Icon view features:
        - Large icons (32x32 or larger)
        - Text labels below icons
        - Grid layout (wraps like icons on desktop)
        - Best for visual browsing
        
        Screen readers announce:
        - Item label
        - Icon description (if available)
        - Grid position
        """
        self.list_ctrl.ClearAll()
        
        for idx, task in enumerate(self.tasks):
            icon_idx = self._get_priority_icon_index(task['priority'])
            # Shorter label for icon view
            label = f"{task['task'][:30]}..."
            index = self.list_ctrl.InsertItem(idx, label, icon_idx)
            self.list_ctrl.SetItemData(index, idx)
            
    def _setup_small_icon_view(self):
        """Setup Small Icon view (small icons with labels).
        
        Small Icon view features:
        - Small icons (16x16)
        - Compact grid layout
        - More items visible
        - Best for browsing many items
        
        Screen readers announce:
        - Item label
        - Position
        """
        self.list_ctrl.ClearAll()
        
        for idx, task in enumerate(self.tasks):
            icon_idx = self._get_priority_icon_index(task['priority'])
            # Very short label for small icon view
            label = f"{task['task'][:20]}..."
            index = self.list_ctrl.InsertItem(idx, label, icon_idx)
            self.list_ctrl.SetItemData(index, idx)
            
    def _switch_view(self, view_name):
        """Switch ListCtrl view mode.
        
        View modes test different accessibility scenarios:
        - Report: Multi-column navigation, cell focus
        - List: Simple vertical list navigation
        - Icon: Grid navigation, spatial awareness
        - Small Icon: Dense grid navigation
        
        Args:
            view_name (str): "Report", "List", "Icon", or "SmallIcon"
        """
        self.current_view = view_name
        
        # Update control style
        if view_name == "Report":
            style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_EDIT_LABELS
            self._setup_report_view()
        elif view_name == "List":
            style = wx.LC_LIST | wx.LC_SINGLE_SEL
            self._setup_list_view()
        elif view_name == "Icon":
            style = wx.LC_ICON | wx.LC_SINGLE_SEL
            self._setup_icon_view()
        elif view_name == "SmallIcon":
            style = wx.LC_SMALL_ICON | wx.LC_SINGLE_SEL
            self._setup_small_icon_view()
            
        # Recreate control with new style
        # (wxPython requires recreating to change view style)
        parent = self.list_ctrl.GetParent()
        sizer = self.list_ctrl.GetContainingSizer()
        pos = sizer.GetItem(self.list_ctrl)
        
        self.list_ctrl.Destroy()
        
        self.list_ctrl = wx.ListCtrl(parent, style=style | wx.BORDER_SUNKEN)
        self.list_ctrl.SetImageList(self.image_list, wx.IMAGE_LIST_NORMAL)
        self.list_ctrl.SetImageList(self.image_list, wx.IMAGE_LIST_SMALL)
        
        # Rebind events
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated)
        self.list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_click)
        self.list_ctrl.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        # Re-setup view
        if view_name == "Report":
            self._setup_report_view()
        elif view_name == "List":
            self._setup_list_view()
        elif view_name == "Icon":
            self._setup_icon_view()
        elif view_name == "SmallIcon":
            self._setup_small_icon_view()
            
        # Replace in sizer
        sizer.Replace(pos.GetWindow(), self.list_ctrl)
        sizer.Layout()
        
        # Update status
        self.info_label.SetLabel(f"View: {self.current_view} | Total items: {len(self.tasks)}")
        
        self.main_frame.update_status_bar(
            f"Switched to {view_name} view",
            f"{len(self.tasks)} items",
            "Arrow keys to navigate"
        )
        
    def on_item_selected(self, event):
        """Handle item selection.
        
        Selection behavior varies by view:
        - Report: Selects entire row, shows all columns
        - List/Icon/SmallIcon: Selects single item
        
        Screen reader announcements differ by view mode.
        """
        item_index = event.GetIndex()
        task_index = self.list_ctrl.GetItemData(item_index)
        task = self.tasks[task_index]
        
        # Status varies by view mode
        if self.current_view == "Report":
            info = f"{task['task']} | {task['assignee']} | {task['priority']}"
        else:
            info = task['task']
            
        self.main_frame.update_status_bar(
            info,
            f"Item {item_index + 1} of {self.list_ctrl.GetItemCount()} in {self.current_view} view",
            "Enter for details, Arrow keys to navigate"
        )
        event.Skip()
        
    def on_item_activated(self, event):
        """Handle item activation (Enter or double-click).
        
        Shows full task details regardless of view mode.
        """
        item_index = event.GetIndex()
        task_index = self.list_ctrl.GetItemData(item_index)
        task = self.tasks[task_index]
        
        wx.MessageBox(
            f"Task: {task['task']}\n"
            f"Assignee: {task['assignee']}\n"
            f"Priority: {task['priority']}\n"
            f"Status: {task['status']}\n"
            f"Due: {task['due_date']}",
            f"Task Details ({self.current_view} View)",
            wx.OK | wx.ICON_INFORMATION
        )
        
    def on_column_click(self, event):
        """Handle column header click (Report view only).
        
        Column clicks only available in Report view.
        Other views don't have column headers.
        """
        if self.current_view != "Report":
            return
            
        col = event.GetColumn()
        col_names = ["Task", "Assignee", "Priority", "Status", "Due Date"]
        
        self.main_frame.update_status_bar(
            f"Column clicked: {col_names[col]}",
            "Sorting not implemented in demo",
            ""
        )
        
    def on_control_focus(self, event):
        """Handle control focus for status bar updates.
        
        Focus behavior varies by view mode:
        - Report: Focus on row, navigate cells with arrows
        - List: Focus on item, vertical navigation
        - Icon/SmallIcon: Focus on item, 2D grid navigation
        """
        selected = self.list_ctrl.GetFirstSelected()
        
        view_hints = {
            "Report": "Arrows: navigate cells, Enter: activate, F2: edit",
            "List": "Up/Down: navigate, Enter: activate",
            "Icon": "Arrows: navigate grid, Enter: activate",
            "SmallIcon": "Arrows: navigate grid, Enter: activate"
        }
        
        if selected != -1:
            task_index = self.list_ctrl.GetItemData(selected)
            task = self.tasks[task_index]
            
            self.main_frame.update_status_bar(
                f"ListCtrl ({self.current_view} view)",
                f"Role: List, Item {selected + 1} of {self.list_ctrl.GetItemCount()}: {task['task'][:40]}",
                view_hints.get(self.current_view, "Arrow keys to navigate")
            )
        else:
            self.main_frame.update_status_bar(
                f"ListCtrl ({self.current_view} view)",
                f"Role: List, {self.list_ctrl.GetItemCount()} items",
                view_hints.get(self.current_view, "Arrow keys to navigate")
            )
        event.Skip()
        
    # State management
    def save_state(self):
        """Save tab state to JSON-serializable dictionary.
        
        Captures:
        - Current view mode
        - Selected item index (if any)
        
        Returns:
            dict: State dictionary for JSON serialization
        """
        selected = self.list_ctrl.GetFirstSelected()
        return {
            "view_mode": self.current_view,
            "selected_index": selected if selected != -1 else None
        }
        
    def load_state(self, state):
        """Load tab state from saved dictionary.
        
        Restores:
        - View mode
        - Selected item
        
        Args:
            state (dict): State dictionary from JSON
        """
        if "view_mode" in state:
            self._switch_view(state["view_mode"])
            
        if "selected_index" in state and state["selected_index"] is not None:
            if state["selected_index"] < self.list_ctrl.GetItemCount():
                self.list_ctrl.Select(state["selected_index"])
                self.list_ctrl.EnsureVisible(state["selected_index"])
                
    def reset_to_defaults(self):
        """Reset to default state.
        
        Restores:
        - Report view (default)
        - No selection
        """
        self._switch_view("Report")
        self.list_ctrl.Select(self.list_ctrl.GetFirstSelected(), False)
