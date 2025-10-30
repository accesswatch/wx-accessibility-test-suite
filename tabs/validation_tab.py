"""Validation Tab.

WCAG 2.2 AA validation checklist and testing documentation.
Allows testers to mark criteria as validated with notes.
"""

import wx
from state_manager import TabStateHelper
from test_data import WCAG_CRITERIA
from datetime import datetime


class ValidationTab(wx.Panel, TabStateHelper):
    """Tab for WCAG validation checklist and documentation."""
    
    def __init__(self, parent, main_frame):
        """Initialize validation tab and build checklist/documentation UI."""
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Validation & Documentation"
        
        # Validation state
        self.validation_states = {}
        self.notes = {}
        
        # Create splitter
        splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        
        # Left panel: WCAG checklist
        left_panel = self._create_checklist_panel(splitter)
        
        # Right panel: Documentation
        right_panel = self._create_documentation_panel(splitter)
        
        splitter.SplitVertically(left_panel, right_panel)
        splitter.SetSashPosition(600)
        
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
    def GetName(self):
        """Return human-readable tab name."""
        return self.tab_name
        
    def _create_checklist_panel(self, parent):
        """Create WCAG checklist panel."""
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Header
        header = wx.StaticText(
            panel,
            label="WCAG 2.2 AA Validation Checklist"
        )
        font = header.GetFont()
        font.PointSize += 2
        font = font.Bold()
        header.SetFont(font)
        sizer.Add(header, 0, wx.ALL, 10)
        
        # Tester info
        info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        info_sizer.Add(wx.StaticText(panel, label="&Tester Name:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.tester_name = wx.TextCtrl(panel, size=(200, -1))
        info_sizer.Add(self.tester_name, 0, wx.ALL, 5)
        sizer.Add(info_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # Scrolled area for checklist
        scroll = wx.ScrolledWindow(panel, style=wx.VSCROLL)
        scroll.SetScrollRate(0, 20)
        
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Group criteria by first digit (category)
        categories = {}
        for criterion in WCAG_CRITERIA:
            category = criterion['id'].split('.')[0]
            if category not in categories:
                categories[category] = []
            categories[category].append(criterion)
            
        category_names = {
            "1": "Perceivable",
            "2": "Operable",
            "3": "Understandable",
            "4": "Robust"
        }
        
        self.checkboxes = {}
        
        for category_num in sorted(categories.keys()):
            category_label = f"{category_num}. {category_names.get(category_num, 'Other')}"
            
            # Category header
            box = wx.StaticBox(scroll, label=category_label)
            box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            
            for criterion in categories[category_num]:
                criterion_id = criterion['id']
                
                # Create checkbox with criterion
                label_text = f"{criterion['id']} - {criterion['name']} (Level {criterion['level']})"
                if criterion.get('critical', False):
                    label_text += " ⚠ CRITICAL"
                if criterion.get('new_in_2_2', False):
                    label_text += " 🆕 NEW in 2.2"
                    
                cb = wx.CheckBox(scroll, label=label_text)
                cb.SetToolTip(criterion['description'])
                cb.Bind(wx.EVT_CHECKBOX, lambda e, cid=criterion_id: self.on_criterion_check(e, cid))
                
                self.checkboxes[criterion_id] = cb
                self.validation_states[criterion_id] = False
                self.notes[criterion_id] = ""
                
                box_sizer.Add(cb, 0, wx.ALL, 3)
                
                # Notes button
                notes_btn = wx.Button(scroll, label=f"Notes for {criterion['id']}", size=(120, -1))
                notes_btn.Bind(wx.EVT_BUTTON, lambda e, cid=criterion_id: self.on_edit_notes(e, cid))
                box_sizer.Add(notes_btn, 0, wx.LEFT | wx.BOTTOM, 20)
                
            scroll_sizer.Add(box_sizer, 0, wx.ALL | wx.EXPAND, 5)
            
        scroll.SetSizer(scroll_sizer)
        sizer.Add(scroll, 1, wx.ALL | wx.EXPAND, 10)
        
        # Summary
        self.summary_label = wx.StaticText(panel, label="")
        self._update_summary()
        sizer.Add(self.summary_label, 0, wx.ALL, 10)
        
        # Export button
        export_btn = wx.Button(panel, label="&Export Validation Report")
        export_btn.Bind(wx.EVT_BUTTON, self.on_export_report)
        sizer.Add(export_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        panel.SetSizer(sizer)
        return panel
        
    def _create_documentation_panel(self, parent):
        """Create documentation panel."""
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Header
        header = wx.StaticText(panel, label="Keyboard Shortcuts & Testing Guide")
        font = header.GetFont()
        font.PointSize += 2
        font = font.Bold()
        header.SetFont(font)
        sizer.Add(header, 0, wx.ALL, 10)
        
        # Text control for documentation
        doc_text = self._generate_documentation()
        
        self.doc_ctrl = wx.TextCtrl(
            panel,
            value=doc_text,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP
        )
        sizer.Add(self.doc_ctrl, 1, wx.ALL | wx.EXPAND, 10)
        
        panel.SetSizer(sizer)
        return panel
        
    def _generate_documentation(self):
        """Generate documentation text."""
        return """KEYBOARD SHORTCUTS REFERENCE
============================

UNIVERSAL NAVIGATION
-------------------
Tab / Shift+Tab: Navigate forward/backward through controls
Arrow Keys: Navigate within complex controls (lists, trees, grids, menus)
Space: Activate buttons, toggle checkboxes, select in lists
Enter: Activate default button, confirm selections
Escape: Cancel operations, close dialogs
Context Menu Key (or Shift+F10): Open context menu

TEXT CONTROLS
-------------
Ctrl+A: Select all text
Ctrl+C/X/V: Copy/Cut/Paste
Home/End: Beginning/End of line
Ctrl+Home/End: Beginning/End of document
Shift+Arrows: Select text

LISTS & TREES
-------------
Arrow Up/Down: Navigate items
Space: Toggle selection (multi-select mode)
Ctrl+Space: Toggle individual item without changing other selections
Shift+Arrows: Range selection
Ctrl+A: Select all
Page Up/Down: Scroll by page
Home/End: First/Last item
Type letters: Jump to item starting with that letter

TREE CONTROLS
-------------
Arrow Right: Expand node / Move to first child
Arrow Left: Collapse node / Move to parent
* (numpad): Expand all children
Backspace: Move to parent

GRID CONTROLS
-------------
Arrow Keys: Navigate cells
Tab: Move to next cell (or out of grid)
F2 or Enter: Begin editing cell
Escape: Cancel editing
Ctrl+Home/End: First/Last cell
Page Up/Down: Scroll page

MENUS
-----
Alt or F10: Activate menu bar
Alt+Letter: Access menu by mnemonic
Arrow Keys: Navigate menus
Enter: Activate menu item
Escape: Close menu

EXPECTED SCREEN READER ANNOUNCEMENTS
====================================

For each control type, screen readers should announce:

1. ROLE: The control type (button, checkbox, list, tree, grid, etc.)
2. NAME: The label or accessible name
3. STATE: Current state (checked, unchecked, selected, expanded, collapsed, pressed, etc.)
4. VALUE: Current value (for inputs, sliders, selections)
5. POSITION: Position in lists/trees ("Item 5 of 20")
6. LEVEL: Depth in hierarchies (tree nodes)

EXAMPLES:
---------
Button: "Save Button"
Checkbox: "Enable notifications Checkbox Checked"
ListCtrl: "Task Name, Row 5 of 100, Checkbox Unchecked"
TreeCtrl: "Documents Folder, Level 1, Expanded, Checkbox Mixed (2 of 5 checked)"
Grid: "Row 3, Column 4, Completed Checkbox Checked, Editable"
Radio Button: "High Radio Button Checked, 3 of 4"

TESTING PROCEDURE
=================

1. KEYBOARD NAVIGATION
   - Verify Tab/Shift+Tab moves through all controls
   - Confirm no keyboard traps (can always Tab out)
   - Check focus indicator is clearly visible
   - Ensure focus order is logical

2. CONTROL OPERATION
   - Test all controls with keyboard only
   - Verify Space/Enter activate appropriately
   - Test arrow key navigation in complex controls
   - Confirm checkboxes toggle with Space

3. SCREEN READER TESTING
   - Enable NVDA, JAWS, or Narrator
   - Verify role is announced correctly
   - Check name/label is read
   - Confirm state is announced (checked/unchecked/selected)
   - Verify position is announced in lists/trees
   - Test that state changes are announced

4. COMPLEX CONTROLS
   ListCtrl:
   - Navigate rows with arrows
   - Toggle checkboxes with Space
   - Verify column headers are announced
   - Test multi-select with Ctrl+Space
   
   TreeCtrl:
   - Expand/collapse with arrows
   - Navigate hierarchy levels
   - Toggle checkboxes (including tri-state for parents)
   - Verify level is announced
   
   Grid:
   - Navigate cells with arrows
   - Edit cells with F2
   - Toggle checkbox cells with Space
   - Verify row/column headers announced

5. VALIDATION MARKING
   - Check each criterion in the checklist
   - Add notes for any issues found
   - Mark criteria as validated when tested
   - Export report when complete

STATE PERSISTENCE
================

All control states, checkbox values, text entries, and validation
progress are automatically saved when the application closes and
restored when reopened.

State files are saved in: state/app_state.json
Logs are saved in: logs/keyboard_events.json

Use File > Save State to manually save at any time.
Use File > Reset to Defaults to restore initial test data.
"""
        
    def _update_summary(self):
        """Update validation summary."""
        total = len(WCAG_CRITERIA)
        checked = sum(1 for v in self.validation_states.values() if v)
        percent = (checked / total * 100) if total > 0 else 0
        
        self.summary_label.SetLabel(
            f"Validation Progress: {checked} of {total} criteria validated ({percent:.1f}%)"
        )
        
    def on_criterion_check(self, event, criterion_id):
        """Handle criterion checkbox change."""
        cb = self.checkboxes[criterion_id]
        self.validation_states[criterion_id] = cb.GetValue()
        self._update_summary()
        
        state = "Validated" if cb.GetValue() else "Not validated"
        self.main_frame.update_status_bar(
            f"WCAG {criterion_id}",
            state,
            ""
        )
        
    def on_edit_notes(self, event, criterion_id):
        """Open dialog to edit notes for a criterion."""
        # Find the criterion info
        criterion = next((c for c in WCAG_CRITERIA if c['id'] == criterion_id), None)
        if not criterion:
            return
            
        dlg = wx.TextEntryDialog(
            self,
            f"Notes for {criterion['id']} - {criterion['name']}:\n\n{criterion['description']}\n\nEnter your testing notes:",
            "Edit Notes",
            value=self.notes.get(criterion_id, ""),
            style=wx.OK | wx.CANCEL | wx.TE_MULTILINE
        )
        dlg.SetSize((500, 400))
        
        if dlg.ShowModal() == wx.ID_OK:
            self.notes[criterion_id] = dlg.GetValue()
            
        dlg.Destroy()
        
    def on_export_report(self, event):
        """Export validation report."""
        report = self._generate_report()
        
        dlg = wx.FileDialog(
            self,
            "Save Validation Report",
            defaultFile=f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            wildcard="Text files (*.txt)|*.txt|All files (*.*)|*.*",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(report)
                    
                wx.MessageBox(
                    f"Validation report exported successfully to:\n{path}",
                    "Export Complete",
                    wx.OK | wx.ICON_INFORMATION
                )
            except Exception as e:
                wx.MessageBox(
                    f"Error exporting report: {e}",
                    "Export Error",
                    wx.OK | wx.ICON_ERROR
                )
                
        dlg.Destroy()
        
    def _generate_report(self):
        """Generate validation report text."""
        report = []
        report.append("=" * 80)
        report.append("WCAG 2.2 AA VALIDATION REPORT")
        report.append("wxPython Accessibility Test Suite")
        report.append("=" * 80)
        report.append("")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Tester: {self.tester_name.GetValue() or '(not specified)'}")
        report.append("")
        
        total = len(WCAG_CRITERIA)
        checked = sum(1 for v in self.validation_states.values() if v)
        percent = (checked / total * 100) if total > 0 else 0
        
        report.append(f"Validation Progress: {checked} of {total} criteria validated ({percent:.1f}%)")
        report.append("")
        report.append("=" * 80)
        report.append("")
        
        # Group by category
        categories = {}
        for criterion in WCAG_CRITERIA:
            category = criterion['id'].split('.')[0]
            if category not in categories:
                categories[category] = []
            categories[category].append(criterion)
            
        category_names = {
            "1": "Perceivable",
            "2": "Operable",
            "3": "Understandable",
            "4": "Robust"
        }
        
        for category_num in sorted(categories.keys()):
            report.append(f"PRINCIPLE {category_num}: {category_names.get(category_num, 'Other')}")
            report.append("-" * 80)
            report.append("")
            
            for criterion in categories[category_num]:
                cid = criterion['id']
                status = "✓ VALIDATED" if self.validation_states.get(cid, False) else "☐ NOT VALIDATED"
                
                report.append(f"{status} - {cid} {criterion['name']} (Level {criterion['level']})")
                report.append(f"    Description: {criterion['description']}")
                
                if criterion.get('critical', False):
                    report.append("    ⚠ CRITICAL CRITERION")
                if criterion.get('new_in_2_2', False):
                    report.append("    🆕 NEW in WCAG 2.2")
                    
                notes = self.notes.get(cid, "").strip()
                if notes:
                    report.append(f"    Notes: {notes}")
                    
                report.append("")
                
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)
        
    # State management
    def save_state(self):
        """Save validation state."""
        return {
            "tester_name": self.tester_name.GetValue(),
            "validation_states": self.validation_states,
            "notes": self.notes
        }
        
    def load_state(self, state):
        """Load validation state."""
        if "tester_name" in state:
            self.tester_name.SetValue(state["tester_name"])
            
        if "validation_states" in state:
            self.validation_states = state["validation_states"]
            for criterion_id, is_checked in self.validation_states.items():
                if criterion_id in self.checkboxes:
                    self.checkboxes[criterion_id].SetValue(is_checked)
                    
        if "notes" in state:
            self.notes = state["notes"]
            
        self._update_summary()
        
    def reset_to_defaults(self):
        """Reset validation state."""
        self.tester_name.SetValue("")
        
        for criterion_id in self.validation_states:
            self.validation_states[criterion_id] = False
            if criterion_id in self.checkboxes:
                self.checkboxes[criterion_id].SetValue(False)
                
        for criterion_id in self.notes:
            self.notes[criterion_id] = ""
            
        self._update_summary()
