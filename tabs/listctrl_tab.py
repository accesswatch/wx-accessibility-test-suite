"""
ListCtrl Tab
============
Tests for wx.ListCtrl with embedded checkboxes in report view.
Demonstrates multi-column lists with checkbox selection and keyboard navigation.
"""

import wx
from state_manager import TabStateHelper
from test_data import generate_task_list


class ListCtrlTab(wx.Panel, TabStateHelper):
    """Tab containing ListCtrl with checkboxes for accessibility testing."""
    
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "ListCtrl with Checkboxes"
        self.tasks = generate_task_list(100)
        
        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Instructions
        inst_text = wx.StaticText(
            self,
            label="ListCtrl in report view with checkbox column. "
                  "Arrow keys to navigate, Space to toggle checkboxes, "
                  "Ctrl+Space for multi-select, Click column headers to sort."
        )
        inst_text.Wrap(800)
        main_sizer.Add(inst_text, 0, wx.ALL | wx.EXPAND, 10)
        
        # Create ListCtrl
        self.list_ctrl = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_SUNKEN
        )
        
        # Add columns
        self.list_ctrl.AppendColumn("ID", width=50)
        self.list_ctrl.AppendColumn("✓", width=40)  # Checkbox column
        self.list_ctrl.AppendColumn("Task", width=200)
        self.list_ctrl.AppendColumn("Assignee", width=150)
        self.list_ctrl.AppendColumn("Priority", width=80)
        self.list_ctrl.AppendColumn("Status", width=120)
        self.list_ctrl.AppendColumn("Due Date", width=100)
        
        # Populate list
        self._populate_list()
        
        # Bind events
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated)
        self.list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_click)
        self.list_ctrl.Bind(wx.EVT_CHAR, self.on_char)
        self.list_ctrl.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        main_sizer.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 10)
        
        # Status info
        self.info_label = wx.StaticText(
            self,
            label=f"Total tasks: {len(self.tasks)}, Checked: {sum(1 for t in self.tasks if t['checked'])}"
        )
        main_sizer.Add(self.info_label, 0, wx.ALL, 10)
        
        # Action buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.check_all_btn = wx.Button(self, label="Check &All")
        self.check_all_btn.Bind(wx.EVT_BUTTON, self.on_check_all)
        btn_sizer.Add(self.check_all_btn, 0, wx.ALL, 5)
        
        self.uncheck_all_btn = wx.Button(self, label="&Uncheck All")
        self.uncheck_all_btn.Bind(wx.EVT_BUTTON, self.on_uncheck_all)
        btn_sizer.Add(self.uncheck_all_btn, 0, wx.ALL, 5)
        
        self.toggle_btn = wx.Button(self, label="&Toggle Selected")
        self.toggle_btn.Bind(wx.EVT_BUTTON, self.on_toggle_selected)
        btn_sizer.Add(self.toggle_btn, 0, wx.ALL, 5)
        
        main_sizer.Add(btn_sizer, 0, wx.ALL, 10)
        
        self.SetSizer(main_sizer)
        
    def GetName(self):
        return self.tab_name
        
    def _populate_list(self):
        """Populate ListCtrl with task data.
        
        Creates multi-column list with:
        - ID column (numeric identifier)
        - Checkbox column (☑/☐ visual indicators)
        - Task details (task, assignee, priority, status, due date)
        
        Uses SetItemData to map visual row to data array index.
        This allows rows to be sorted/filtered while maintaining
        correct data associations.
        """
        self.list_ctrl.DeleteAllItems()
        
        for task in self.tasks:
            # Insert new row with ID in first column
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(task['id']))
            # Checkbox column uses Unicode box characters
            self.list_ctrl.SetItem(index, 1, "☑" if task['checked'] else "☐")
            # Task detail columns
            self.list_ctrl.SetItem(index, 2, task['task'])
            self.list_ctrl.SetItem(index, 3, task['assignee'])
            self.list_ctrl.SetItem(index, 4, task['priority'])
            self.list_ctrl.SetItem(index, 5, task['status'])
            self.list_ctrl.SetItem(index, 6, task['due_date'])
            
            # Store task index in item data for data lookup
            self.list_ctrl.SetItemData(index, task['id'] - 1)
            
    def _update_checkbox_display(self, item_index):
        """Update checkbox display for an item."""
        task_index = self.list_ctrl.GetItemData(item_index)
        checked = self.tasks[task_index]['checked']
        self.list_ctrl.SetItem(item_index, 1, "☑" if checked else "☐")
        
    def _update_info_label(self):
        """Update status label with current counts."""
        checked_count = sum(1 for t in self.tasks if t['checked'])
        self.info_label.SetLabel(f"Total tasks: {len(self.tasks)}, Checked: {checked_count}")
        
    def on_item_selected(self, event):
        """Handle item selection.
        
        Triggered by:
        - Arrow key navigation
        - Mouse click
        - Tab key focus
        
        Updates status bar with task details and current position.
        Screen readers should announce:
        - Row position (e.g., "3 of 100")
        - Task name
        - Checkbox state
        - Column values
        """
        item_index = event.GetIndex()
        # Map visual row to data array index
        task_index = self.list_ctrl.GetItemData(item_index)
        task = self.tasks[task_index]
        
        checked_status = "Checked" if task['checked'] else "Unchecked"
        
        self.main_frame.update_status_bar(
            f"Task {task['id']}: {task['task']}",
            f"Row {item_index + 1} of {self.list_ctrl.GetItemCount()}, Status: {checked_status}",
            "Space to toggle checkbox, Arrows to navigate"
        )
        event.Skip()
        
    def on_item_activated(self, event):
        """Handle item activation (Enter or double-click).
        
        Activation triggers:
        - Enter key on selected row
        - Double-click on row
        
        Opens dialog with full task details.
        Screen readers should announce "Task Details dialog" when opened.
        
        Common pattern: Activation shows detail view or edit dialog.
        """
        item_index = event.GetIndex()
        task_index = self.list_ctrl.GetItemData(item_index)
        task = self.tasks[task_index]
        
        # Display all task fields in dialog
        wx.MessageBox(
            f"Task: {task['task']}\n"
            f"Assignee: {task['assignee']}\n"
            f"Priority: {task['priority']}\n"
            f"Status: {task['status']}\n"
            f"Due: {task['due_date']}\n"
            f"Checked: {'Yes' if task['checked'] else 'No'}",
            "Task Details",
            wx.OK | wx.ICON_INFORMATION
        )
        
    def on_column_click(self, event):
        """Handle column header click for sorting.
        
        Column headers in LC_REPORT view are clickable.
        Standard behavior: Click to sort, click again to reverse.
        
        Implementation notes:
        - Would typically sort self.tasks array
        - Then call _populate_list() to rebuild display
        - Use sort indicators (▲/▼) in column headers
        
        Screen readers should announce:
        - Column name
        - Sort direction (ascending/descending)
        
        Keyboard access: Tab to headers, Enter to activate.
        """
        col = event.GetColumn()
        col_names = ["ID", "Checked", "Task", "Assignee", "Priority", "Status", "Due Date"]
        
        self.main_frame.update_status_bar(
            f"Sorting by column: {col_names[col]}",
            "",
            ""
        )
        
        # Simple sort demonstration (in real app, would sort and rebuild)
        wx.MessageBox(
            f"Sort by {col_names[col]} (not fully implemented in demo)",
            "Sort",
            wx.OK | wx.ICON_INFORMATION
        )
        
    def on_char(self, event):
        """Handle keyboard input.
        
        Custom keyboard handlers:
        - Space: Toggle checkbox for selected item
        
        All other keys (arrows, Enter, etc.) handled by
        default ListCtrl behavior via event.Skip().
        
        Note: This is a custom checkbox implementation.
        Real checkbox columns would use wx.LC_VIRTUAL with
        custom drawing or wx.dataview.DataViewCtrl.
        
        Screen readers should announce state change when
        checkbox is toggled.
        """
        keycode = event.GetKeyCode()
        
        # Space key toggles checkbox on selected item
        if keycode == wx.WXK_SPACE:
            selected = self.list_ctrl.GetFirstSelected()
            if selected != -1:
                # Toggle checked state in data
                task_index = self.list_ctrl.GetItemData(selected)
                self.tasks[task_index]['checked'] = not self.tasks[task_index]['checked']
                # Update visual checkbox indicator
                self._update_checkbox_display(selected)
                self._update_info_label()
                
                checked_status = "Checked" if self.tasks[task_index]['checked'] else "Unchecked"
                self.main_frame.update_status_bar(
                    f"Task {self.tasks[task_index]['id']}",
                    f"Checkbox {checked_status}",
                    "Space to toggle"
                )
        else:
            # Let default handler process other keys
            event.Skip()
            
    def on_control_focus(self, event):
        """Handle focus event."""
        selected = self.list_ctrl.GetFirstSelected()
        if selected != -1:
            task_index = self.list_ctrl.GetItemData(selected)
            task = self.tasks[task_index]
            checked_status = "Checked" if task['checked'] else "Unchecked"
            
            self.main_frame.update_status_bar(
                f"ListCtrl: {self.list_ctrl.GetItemCount()} items",
                f"Role: List, Item {selected + 1} of {self.list_ctrl.GetItemCount()}, {checked_status}",
                "Arrows to navigate, Space to toggle checkbox"
            )
        else:
            self.main_frame.update_status_bar(
                f"ListCtrl: {self.list_ctrl.GetItemCount()} items",
                "Role: List",
                "Arrows to navigate, Space to toggle checkbox"
            )
        event.Skip()
        
    def on_check_all(self, event):
        """Check all checkboxes."""
        for task in self.tasks:
            task['checked'] = True
        for i in range(self.list_ctrl.GetItemCount()):
            self._update_checkbox_display(i)
        self._update_info_label()
        
        self.main_frame.update_status_bar(
            "All tasks checked",
            f"{len(self.tasks)} items checked",
            ""
        )
        
    def on_uncheck_all(self, event):
        """Uncheck all checkboxes."""
        for task in self.tasks:
            task['checked'] = False
        for i in range(self.list_ctrl.GetItemCount()):
            self._update_checkbox_display(i)
        self._update_info_label()
        
        self.main_frame.update_status_bar(
            "All tasks unchecked",
            "0 items checked",
            ""
        )
        
    def on_toggle_selected(self, event):
        """Toggle checkbox on selected item."""
        selected = self.list_ctrl.GetFirstSelected()
        if selected != -1:
            task_index = self.list_ctrl.GetItemData(selected)
            self.tasks[task_index]['checked'] = not self.tasks[task_index]['checked']
            self._update_checkbox_display(selected)
            self._update_info_label()
            
    # State management
    def save_state(self):
        """Save tab state."""
        return {
            "tasks": self.tasks,
            "selected": self.list_ctrl.GetFirstSelected()
        }
        
    def load_state(self, state):
        """Load tab state."""
        if "tasks" in state:
            self.tasks = state["tasks"]
            self._populate_list()
            self._update_info_label()
            
        if "selected" in state and state["selected"] != -1:
            if state["selected"] < self.list_ctrl.GetItemCount():
                self.list_ctrl.Select(state["selected"])
                self.list_ctrl.EnsureVisible(state["selected"])
                
    def reset_to_defaults(self):
        """Reset to default test data."""
        self.tasks = generate_task_list(100)
        self._populate_list()
        self._update_info_label()
        if self.list_ctrl.GetItemCount() > 0:
            self.list_ctrl.Select(0)
