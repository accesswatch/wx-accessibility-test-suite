"""TreeCtrl Tab.

Tests for wx.TreeCtrl with checkboxes (including tri-state for parent nodes).
Demonstrates hierarchical navigation with checkbox support.
"""

import wx
from state_manager import TabStateHelper
from test_data import generate_file_tree


class TreeCtrlTab(wx.Panel, TabStateHelper):
    """Tab containing TreeCtrl with checkboxes for accessibility testing."""
    
    def __init__(self, parent, main_frame):
        """Initialize TreeCtrl tab and populate tree controls."""
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "TreeCtrl with Checkboxes"
        self.tree_data = generate_file_tree()
        
        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Instructions
        inst_text = wx.StaticText(
            self,
            label="TreeCtrl with checkboxes. Arrow keys: Up/Down (siblings), "
                  "Right (expand/child), Left (collapse/parent). "
                  "Space to toggle checkboxes. Parent nodes show tri-state when children are mixed."
        )
        inst_text.Wrap(800)
        main_sizer.Add(inst_text, 0, wx.ALL | wx.EXPAND, 10)
        
        # Create TreeCtrl
        self.tree = wx.TreeCtrl(
            self,
            style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS | wx.BORDER_SUNKEN
        )
        
        # Create image list for checkboxes
        self.image_list = wx.ImageList(16, 16)
        self.idx_unchecked = self.image_list.Add(self._create_checkbox_bitmap(False, False))
        self.idx_checked = self.image_list.Add(self._create_checkbox_bitmap(True, False))
        self.idx_mixed = self.image_list.Add(self._create_checkbox_bitmap(False, True))
        self.tree.AssignImageList(self.image_list)
        
        # Populate tree
        self._populate_tree()
        
        # Bind events
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_sel_changed)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_item_activated)
        self.tree.Bind(wx.EVT_CHAR, self.on_char)
        self.tree.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        main_sizer.Add(self.tree, 1, wx.ALL | wx.EXPAND, 10)
        
        # Status info
        self.info_label = wx.StaticText(self, label="")
        self._update_info_label()
        main_sizer.Add(self.info_label, 0, wx.ALL, 10)
        
        # Action buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.expand_all_btn = wx.Button(self, label="&Expand All")
        self.expand_all_btn.Bind(wx.EVT_BUTTON, self.on_expand_all)
        btn_sizer.Add(self.expand_all_btn, 0, wx.ALL, 5)
        
        self.collapse_all_btn = wx.Button(self, label="&Collapse All")
        self.collapse_all_btn.Bind(wx.EVT_BUTTON, self.on_collapse_all)
        btn_sizer.Add(self.collapse_all_btn, 0, wx.ALL, 5)
        
        self.check_all_btn = wx.Button(self, label="Check &All")
        self.check_all_btn.Bind(wx.EVT_BUTTON, self.on_check_all)
        btn_sizer.Add(self.check_all_btn, 0, wx.ALL, 5)
        
        self.uncheck_all_btn = wx.Button(self, label="&Uncheck All")
        self.uncheck_all_btn.Bind(wx.EVT_BUTTON, self.on_uncheck_all)
        btn_sizer.Add(self.uncheck_all_btn, 0, wx.ALL, 5)
        
        main_sizer.Add(btn_sizer, 0, wx.ALL, 10)
        
        self.SetSizer(main_sizer)
        
    def GetName(self):
        """Return human-readable tab name."""
        return self.tab_name
        
    def _create_checkbox_bitmap(self, checked, mixed):
        """Create a checkbox bitmap for tree items.
        
        Creates three checkbox states:
        - Unchecked: Empty box (white)
        - Checked: Green checkmark
        - Mixed: Gray minus (for parent nodes with some children checked)
        
        Note: TreeCtrl doesn't have built-in checkbox support like
        CheckListBox. We implement it using custom images.
        
        Args:
            checked (bool): True for checked state
            mixed (bool): True for indeterminate/mixed state
            
        Returns:
            wx.Bitmap: 16x16 checkbox image
        """
        bmp = wx.Bitmap(16, 16)
        dc = wx.MemoryDC(bmp)
        
        # Background (matches window color for seamless integration)
        dc.SetBackground(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)))
        dc.Clear()
        
        # Draw checkbox border (12x12 box)
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        dc.DrawRectangle(2, 2, 12, 12)
        
        if checked:
            # Draw checkmark (green, classic check shape)
            dc.SetPen(wx.Pen(wx.Colour(0, 120, 0), 2))
            dc.DrawLine(4, 8, 7, 11)  # Short stroke
            dc.DrawLine(7, 11, 12, 4)  # Long stroke
        elif mixed:
            # Draw minus for mixed state (gray horizontal line)
            # Indicates parent has some (not all) children checked
            dc.SetPen(wx.Pen(wx.Colour(128, 128, 128), 2))
            dc.DrawLine(5, 8, 11, 8)
            
        dc.SelectObject(wx.NullBitmap)
        return bmp
        
    def _populate_tree(self):
        """Populate tree with file/folder hierarchical data.
        
        Creates a 3-level file system tree:
        - Root folder
        - Subfolders and files
        - Nested subfolders and files
        
        Each node stores its data dict (name, type, checked state, children).
        Root is expanded by default for immediate visibility.
        
        TreeCtrl structure:
        - Root (always visible)
        - Level 1 children (visible after expand)
        - Level 2+ children (visible when parents expanded)
        """
        self.tree.DeleteAllItems()
        # Create root node
        root = self.tree.AddRoot(self.tree_data['name'])
        # Store data dict for state tracking
        self.tree.SetItemData(root, self.tree_data)
        # Set initial checkbox image
        self._update_item_checkbox(root, self.tree_data)
        
        # Recursively add all children
        self._add_tree_nodes(root, self.tree_data.get('children', []))
        # Expand root to show first level
        self.tree.Expand(root)
        
    def _add_tree_nodes(self, parent_item, children):
        """Recursively add tree nodes.
        
        Builds tree hierarchy by recursively processing children.
        For each node:
        1. Create tree item under parent
        2. Store data dict for state management
        3. Set checkbox image based on checked state
        4. Recursively add grandchildren (if folder)
        
        Args:
            parent_item: wx.TreeItemId of parent node
            children: List of child data dicts
        """
        for child_data in children:
            # Create child node under parent
            item = self.tree.AppendItem(parent_item, child_data['name'])
            # Store data for checkbox state tracking
            self.tree.SetItemData(item, child_data)
            # Set appropriate checkbox image
            self._update_item_checkbox(item, child_data)
            
            # Recursively add grandchildren for folders
            if 'children' in child_data and child_data['children']:
                self._add_tree_nodes(item, child_data['children'])
                
    def _update_item_checkbox(self, item, data):
        """Update checkbox image for an item based on its state.
        
        Implements tri-state checkboxes for folder nodes:
        - Unchecked: No children checked (empty box)
        - Checked: All children checked (checkmark)
        - Mixed: Some children checked (minus sign)
        
        Files always show checked or unchecked (no mixed state).
        
        This pattern is common in:
        - File managers (select files/folders)
        - Permission trees (grant access to resources)
        - Settings hierarchies (enable/disable features)
        
        Args:
            item: wx.TreeItemId to update
            data: Data dict with 'type', 'checked', 'children'
        """
        if data['type'] == 'folder':
            # Folder state depends on children states
            if 'children' in data and data['children']:
                checked_count = sum(1 for c in data['children'] if c['checked'])
                total_count = len(data['children'])
                
                if checked_count == 0:
                    # No children checked → unchecked
                    self.tree.SetItemImage(item, self.idx_unchecked)
                elif checked_count == total_count:
                    # All children checked → checked
                    self.tree.SetItemImage(item, self.idx_checked)
                else:
                    # Some children checked → mixed (indeterminate)
                    self.tree.SetItemImage(item, self.idx_mixed)
            else:
                img = self.idx_checked if data['checked'] else self.idx_unchecked
                self.tree.SetItemImage(item, img)
        else:
            img = self.idx_checked if data['checked'] else self.idx_unchecked
            self.tree.SetItemImage(item, img)
            
    def _get_checkbox_state_name(self, data):
        """Get human-readable checkbox state."""
        if data['type'] == 'folder' and 'children' in data and data['children']:
            checked_count = sum(1 for c in data['children'] if c['checked'])
            total_count = len(data['children'])
            
            if checked_count == 0:
                return "Unchecked"
            elif checked_count == total_count:
                return "Checked"
            else:
                return f"Mixed ({checked_count}/{total_count} checked)"
        else:
            return "Checked" if data['checked'] else "Unchecked"
            
    def _toggle_item_checkbox(self, item):
        """Toggle checkbox for an item and propagate to children."""
        data = self.tree.GetItemData(item)
        if not data:
            return
            
        # Toggle state
        data['checked'] = not data['checked']
        
        # If it's a folder, propagate to children
        if data['type'] == 'folder' and 'children' in data:
            self._set_children_checked(data['children'], data['checked'])
            
        # Update display
        self._update_tree_item_recursive(item)
        
        # Update parent states
        parent = self.tree.GetItemParent(item)
        while parent.IsOk():
            parent_data = self.tree.GetItemData(parent)
            if parent_data:
                self._update_item_checkbox(parent, parent_data)
            parent = self.tree.GetItemParent(parent)
            
        self._update_info_label()
        
    def _set_children_checked(self, children, checked):
        """Recursively set checked state for all children."""
        for child in children:
            child['checked'] = checked
            if 'children' in child:
                self._set_children_checked(child['children'], checked)
                
    def _update_tree_item_recursive(self, item):
        """Update item and all its children."""
        data = self.tree.GetItemData(item)
        if data:
            self._update_item_checkbox(item, data)
            
        child, cookie = self.tree.GetFirstChild(item)
        while child.IsOk():
            self._update_tree_item_recursive(child)
            child, cookie = self.tree.GetNextChild(item, cookie)
            
    def _count_checked_items(self, data):
        """Count total checked items in tree."""
        count = 1 if data.get('checked', False) and data['type'] == 'file' else 0
        if 'children' in data:
            for child in data['children']:
                count += self._count_checked_items(child)
        return count
        
    def _count_total_items(self, data):
        """Count total items in tree."""
        count = 1 if data['type'] == 'file' else 0
        if 'children' in data:
            for child in data['children']:
                count += self._count_total_items(child)
        return count
        
    def _update_info_label(self):
        """Update status label."""
        checked = self._count_checked_items(self.tree_data)
        total = self._count_total_items(self.tree_data)
        self.info_label.SetLabel(f"Files checked: {checked} of {total}")
        
    def on_sel_changed(self, event):
        """Handle selection change.
        
        Triggered by:
        - Arrow key navigation (Up/Down/Left/Right)
        - Mouse click
        - Programmatic selection
        
        Updates status bar with item details and keyboard hints.
        
        Screen readers should announce:
        - Item type (file/folder)
        - Item name
        - Level/depth in tree
        - Expanded/collapsed state (folders only)
        - Checkbox state
        """
        item = event.GetItem()
        if item.IsOk():
            data = self.tree.GetItemData(item)
            if data:
                state = self._get_checkbox_state_name(data)
                type_str = "Folder" if data['type'] == 'folder' else "File"
                
                self.main_frame.update_status_bar(
                    f"{type_str}: {data['name']}",
                    f"Checkbox: {state}",
                    "Arrow keys to navigate, Space to toggle, Right to expand, Left to collapse"
                )
        event.Skip()
        
    def on_item_activated(self, event):
        """Handle item activation (Enter or double-click).
        
        Activation behavior:
        - Folders: Toggle expand/collapse
        - Files: No default action (could open file dialog)
        
        Standard tree navigation:
        - Enter: Expand/collapse folders
        - Double-click: Same as Enter
        - Space: Toggle checkbox (custom handler)
        
        Screen readers should announce expand/collapse state change.
        """
        item = event.GetItem()
        if item.IsOk():
            # Only folders can be expanded/collapsed
            if self.tree.ItemHasChildren(item):
                if self.tree.IsExpanded(item):
                    self.tree.Collapse(item)
                else:
                    self.tree.Expand(item)
                    
    def on_char(self, event):
        """Handle keyboard input.
        
        Custom keyboard handlers:
        - Space: Toggle checkbox for selected item
        
        Default TreeCtrl navigation (via event.Skip()):
        - Up/Down: Previous/next sibling
        - Left: Collapse folder or move to parent
        - Right: Expand folder or move to first child
        - Home: First root item
        - End: Last visible item
        - Enter: Activate (expand/collapse folders)
        
        Checkbox toggle propagates:
        - Down: Checking parent checks all children
        - Up: Child state changes update parent's mixed/checked state
        
        Screen readers should announce new checkbox state after toggle.
        """
        keycode = event.GetKeyCode()
        
        # Space key toggles checkbox
        if keycode == wx.WXK_SPACE:
            item = self.tree.GetSelection()
            if item.IsOk():
                # Toggle and propagate to children/parents
                self._toggle_item_checkbox(item)
                
                data = self.tree.GetItemData(item)
                if data:
                    state = self._get_checkbox_state_name(data)
                    self.main_frame.update_status_bar(
                        f"{data['name']}",
                        f"Checkbox: {state}",
                        "Space to toggle"
                    )
        else:
            # Let default handler process other keys
            event.Skip()
            
    def on_control_focus(self, event):
        """Handle control focus for status bar updates.
        
        Updates status bar when tree receives focus to show:
        - Item type (file/folder)
        - Expected screen reader announcements
        - Keyboard shortcuts
        
        Helps testers verify that screen readers announce:
        - Tree role
        - Current item name and type
        - Level/depth in hierarchy
        - Expanded/collapsed state (folders)
        - Checkbox state
        - Position (e.g., "2 of 5" siblings)
        """
        item = self.tree.GetSelection()
        if item.IsOk():
            data = self.tree.GetItemData(item)
            if data:
                state = self._get_checkbox_state_name(data)
                type_str = "Folder" if data['type'] == 'folder' else "File"
                
                self.main_frame.update_status_bar(
                    f"TreeCtrl: {type_str}",
                    f"Role: Tree item, State: {state}",
                    "Arrows to navigate, Space to toggle, Right/Left to expand/collapse"
                )
        event.Skip()
        
    def on_expand_all(self, event):
        """Expand all tree nodes.
        
        Expands entire tree hierarchy for overview.
        Useful for:
        - Seeing all items at once
        - Testing screen reader navigation of deep trees
        - Verifying all items are accessible
        
        Screen readers should announce each level as user navigates.
        """
        self.tree.ExpandAll()
        
    def on_collapse_all(self, event):
        """Collapse all tree nodes (except root).
        
        Collapses to show only root's direct children.
        Useful for:
        - Resetting view to compact state
        - Testing expand/collapse with screen readers
        - Reducing visual clutter
        
        Root remains visible (can't collapse root node).
        """
        root = self.tree.GetRootItem()
        if root.IsOk():
            self.tree.CollapseAllChildren(root)
            
    def on_check_all(self, event):
        """Check all items in tree.
        
        Bulk operation:
        1. Update data model (all nodes checked=True)
        2. Update visual checkboxes (all show checkmark)
        3. Update info label (shows total checked count)
        
        Parent nodes show "checked" (not "mixed") when all
        children are checked.
        
        Tests screen reader announcement of state changes.
        """
        self._set_all_checked(self.tree_data, True)
        root = self.tree.GetRootItem()
        if root.IsOk():
            self._update_tree_item_recursive(root)
        self._update_info_label()
        
    def on_uncheck_all(self, event):
        """Uncheck all items in tree.
        
        Bulk operation:
        1. Update data model (all nodes checked=False)
        2. Update visual checkboxes (all show empty box)
        3. Update info label (shows 0 checked)
        
        Resets tree to initial unchecked state.
        Useful for testing bulk state changes.
        """
        self._set_all_checked(self.tree_data, False)
        root = self.tree.GetRootItem()
        if root.IsOk():
            self._update_tree_item_recursive(root)
        self._update_info_label()
        
    def _set_all_checked(self, data, checked):
        """Recursively set all items checked state.
        
        Updates data model for entire subtree.
        Recursive algorithm:
        1. Set current node's checked state
        2. For each child, recursively set its checked state
        3. Continue until all descendants processed
        
        Args:
            data: Node data dict (modified in place)
            checked (bool): Target checked state
        """
        data['checked'] = checked
        if 'children' in data:
            for child in data['children']:
                self._set_all_checked(child, checked)
                
    # State management
    def save_state(self):
        """Save tab state to JSON-serializable dictionary.
        
        Captures:
        - Checkbox states (stored in tree_data dict)
        - Expanded nodes (list of item names)
        - Selected item (by name)
        
        Expanded state preserves user's view:
        - Which folders are open
        - Which subtrees are visible
        
        Note: Stores names (not TreeItemIds) since item IDs
        are invalid after tree rebuild.
        
        Returns:
            dict: State dictionary for JSON serialization
        """
        # Save expanded state by collecting item names
        expanded_items = []
        
        def collect_expanded(item):
            """Recursively collect expanded item names."""
            if item.IsOk() and self.tree.IsExpanded(item):
                data = self.tree.GetItemData(item)
                if data:
                    expanded_items.append(data['name'])
                    
                child, cookie = self.tree.GetFirstChild(item)
                while child.IsOk():
                    collect_expanded(child)
                    child, cookie = self.tree.GetNextChild(item, cookie)
                    
        root = self.tree.GetRootItem()
        if root.IsOk():
            collect_expanded(root)
            
        # Save selected item
        selected_name = None
        sel_item = self.tree.GetSelection()
        if sel_item.IsOk():
            data = self.tree.GetItemData(sel_item)
            if data:
                selected_name = data['name']
                
        return {
            "tree_data": self.tree_data,
            "expanded_items": expanded_items,
            "selected_item": selected_name
        }
        
    def load_state(self, state):
        """Load tab state."""
        if "tree_data" in state:
            self.tree_data = state["tree_data"]
            self._populate_tree()
            self._update_info_label()
            
            # Restore expanded state
            if "expanded_items" in state:
                def restore_expanded(item):
                    if item.IsOk():
                        data = self.tree.GetItemData(item)
                        if data and data['name'] in state["expanded_items"]:
                            self.tree.Expand(item)
                            
                        child, cookie = self.tree.GetFirstChild(item)
                        while child.IsOk():
                            restore_expanded(child)
                            child, cookie = self.tree.GetNextChild(item, cookie)
                            
                root = self.tree.GetRootItem()
                if root.IsOk():
                    restore_expanded(root)
                    
            # Restore selection
            if "selected_item" in state:
                def find_and_select(item, name):
                    if item.IsOk():
                        data = self.tree.GetItemData(item)
                        if data and data['name'] == name:
                            self.tree.SelectItem(item)
                            return True
                            
                        child, cookie = self.tree.GetFirstChild(item)
                        while child.IsOk():
                            if find_and_select(child, name):
                                return True
                            child, cookie = self.tree.GetNextChild(item, cookie)
                    return False
                    
                root = self.tree.GetRootItem()
                if root.IsOk():
                    find_and_select(root, state["selected_item"])
                    
    def reset_to_defaults(self):
        """Reset to default test data."""
        self.tree_data = generate_file_tree()
        self._populate_tree()
        self._update_info_label()
