"""Advanced Controls 3 Tab.

Tests for HtmlWindow, GenericDirCtrl, StyledTextCtrl, and embedded Notebook.
Demonstrates HTML navigation, directory browsing, code editing, and nested tabbing.
"""

import wx
import wx.html
import wx.stc
import os
from pathlib import Path
from state_manager import TabStateHelper


class AdvancedControls3Tab(wx.Panel, TabStateHelper):
    """Tab containing advanced controls for accessibility testing."""
    
    def __init__(self, parent, main_frame):
        """Initialize advanced controls 3 tab and build UI controls."""
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Advanced Controls 3"
        
        # Main scrolled window
        scroll = wx.ScrolledWindow(self)
        scroll.SetScrollRate(10, 10)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Instructions
        inst_text = wx.StaticText(
            scroll,
            label="Advanced controls: HtmlWindow (HTML navigation), GenericDirCtrl (directory tree), "
                  "StyledTextCtrl (code editor), and embedded Notebook (nested tabs). "
                  "Test keyboard navigation, screen reader announcements, and nested focus management."
        )
        inst_text.Wrap(800)
        main_sizer.Add(inst_text, 0, wx.ALL | wx.EXPAND, 10)
        
        # Create control groups
        main_sizer.Add(self._create_html_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_dirctr_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_stc_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_notebook_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        
        scroll.SetSizer(main_sizer)
        
        # Outer sizer
        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        outer_sizer.Add(scroll, 1, wx.EXPAND)
        self.SetSizer(outer_sizer)
        
    def GetName(self):
        """Return human-readable tab name."""
        return self.tab_name
        
    def _create_html_group(self, parent):
        """Create HtmlWindow group.
        
        Tests HTML rendering and navigation:
        - Hyperlink navigation with keyboard
        - HTML structure (headings, lists, tables)
        - Screen reader HTML semantics
        - Tab key for link navigation
        """
        box = wx.StaticBox(parent, label="HTML Window (Tab for links, Enter to activate)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        self.html = wx.html.HtmlWindow(parent, size=(700, 200))
        self.html.SetPage("""
            <html>
            <head><title>Sample HTML Content</title></head>
            <body>
                <h1>HTML Window Accessibility Test</h1>
                <p>This control displays <strong>formatted HTML</strong> content. 
                Screen readers should announce HTML structure including headings, lists, and links.</p>
                
                <h2>Features</h2>
                <ul>
                    <li>Tab key navigates between hyperlinks</li>
                    <li>Enter or Space activates links</li>
                    <li>Screen readers announce semantic HTML elements</li>
                    <li>Supports basic HTML formatting (bold, italic, lists, tables)</li>
                </ul>
                
                <h2>Sample Links</h2>
                <p>Test keyboard navigation:</p>
                <ul>
                    <li><a href="https://www.wxpython.org">wxPython Official Site</a></li>
                    <li><a href="https://www.w3.org/WAI/WCAG22/quickref/">WCAG 2.2 Guidelines</a></li>
                    <li><a href="https://www.nvaccess.org">NVDA Screen Reader</a></li>
                </ul>
                
                <h2>Accessibility Notes</h2>
                <table border="1" cellpadding="5">
                    <tr>
                        <th>Element</th>
                        <th>Expected Announcement</th>
                    </tr>
                    <tr>
                        <td>Heading</td>
                        <td>Level and text (e.g., "Heading Level 1: HTML Window")</td>
                    </tr>
                    <tr>
                        <td>Link</td>
                        <td>Link text and destination</td>
                    </tr>
                    <tr>
                        <td>List</td>
                        <td>List type and item position</td>
                    </tr>
                </table>
            </body>
            </html>
        """)
        self.html.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.on_html_link)
        self.html.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        sizer.Add(self.html, 1, wx.ALL | wx.EXPAND, 5)
        
        self.html_label = wx.StaticText(parent, label="Click or press Enter on a link to navigate")
        sizer.Add(self.html_label, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_dirctr_group(self, parent):
        """Create GenericDirCtrl group.
        
        Tests directory tree navigation:
        - Hierarchical folder/file structure
        - Arrow key navigation (expand/collapse)
        - Type-ahead search
        - Screen reader announcements of folders vs files
        """
        box = wx.StaticBox(parent, label="Directory Control (Arrow keys to navigate, * to expand all)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        # Start at user's home directory or current directory
        start_dir = str(Path.home())
        
        self.dirctrl = wx.GenericDirCtrl(
            parent,
            dir=start_dir,
            size=(700, 250),
            style=wx.DIRCTRL_DIR_ONLY | wx.DIRCTRL_SELECT_FIRST
        )
        self.dirctrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_dir_selected)
        
        # Get the underlying tree control for focus events
        tree = self.dirctrl.GetTreeCtrl()
        if tree:
            tree.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        sizer.Add(self.dirctrl, 1, wx.ALL | wx.EXPAND, 5)
        
        self.dir_label = wx.StaticText(parent, label=f"Selected: {start_dir}")
        sizer.Add(self.dir_label, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_stc_group(self, parent):
        """Create StyledTextCtrl group.
        
        Tests code editor accessibility:
        - Syntax highlighting
        - Line numbers
        - Code folding
        - Multiple cursor positions
        - Standard editing shortcuts (Ctrl+C/V/X/Z/Y)
        """
        box = wx.StaticBox(parent, label="Styled Text Control (Code Editor with syntax highlighting)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        self.stc = wx.stc.StyledTextCtrl(parent, size=(700, 200))
        
        # Configure for Python syntax
        self.stc.SetLexer(wx.stc.STC_LEX_PYTHON)
        
        # Set up syntax highlighting
        self.stc.StyleSetSpec(wx.stc.STC_P_DEFAULT, "fore:#000000")
        self.stc.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:#007F00,italic")
        self.stc.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:#007F7F")
        self.stc.StyleSetSpec(wx.stc.STC_P_STRING, "fore:#7F007F")
        self.stc.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:#7F007F")
        self.stc.StyleSetSpec(wx.stc.STC_P_WORD, "fore:#00007F,bold")
        self.stc.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:#7F0000")
        self.stc.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000")
        self.stc.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:#0000FF,bold")
        self.stc.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:#007F7F,bold")
        self.stc.StyleSetSpec(wx.stc.STC_P_OPERATOR, "fore:#000000,bold")
        
        # Set Python keywords
        self.stc.SetKeyWords(0, "and as assert break class continue def del elif else except "
                                 "finally for from global if import in is lambda not or pass "
                                 "raise return try while with yield True False None")
        
        # Enable line numbers
        self.stc.SetMarginType(0, wx.stc.STC_MARGIN_NUMBER)
        self.stc.SetMarginWidth(0, 40)
        
        # Enable folding
        self.stc.SetMarginType(1, wx.stc.STC_MARGIN_SYMBOL)
        self.stc.SetMarginMask(1, wx.stc.STC_MASK_FOLDERS)
        self.stc.SetMarginWidth(1, 16)
        self.stc.SetProperty("fold", "1")
        
        # Set sample Python code
        sample_code = '''# Python Code Editor Accessibility Test
"""This is a docstring with syntax highlighting."""

def calculate_total(items, tax_rate=0.08):
    """Calculate total with tax.
    
    Args:
        items: List of prices
        tax_rate: Tax rate (default 8%)
    
    Returns:
        Total amount including tax
    """
    subtotal = sum(items)
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    # Print results
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax: ${tax:.2f}")
    print(f"Total: ${total:.2f}")
    
    return total

# Test the function
prices = [10.99, 25.50, 8.75, 15.00]
result = calculate_total(prices)
'''
        self.stc.SetText(sample_code)
        
        # Bind events
        self.stc.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        sizer.Add(self.stc, 1, wx.ALL | wx.EXPAND, 5)
        
        info = wx.StaticText(
            parent,
            label="Keyboard: Standard editing shortcuts (Ctrl+C/V/X/Z/Y), "
                  "Home/End for line start/end, Ctrl+Home/End for document"
        )
        info.Wrap(680)
        sizer.Add(info, 0, wx.ALL, 5)
        
        return sizer
        
    def _create_notebook_group(self, parent):
        """Create embedded Notebook group.
        
        Tests nested tabbing accessibility:
        - Ctrl+Tab to switch between notebook tabs
        - Tab key to navigate within tab content
        - Screen reader announces current tab
        - Focus management between parent and child tab controls
        """
        box = wx.StaticBox(parent, label="Embedded Notebook (Ctrl+Tab for tabs, Tab for controls)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        self.notebook = wx.Notebook(parent, size=(700, 200))
        
        # Tab 1: Text controls
        panel1 = wx.Panel(self.notebook)
        p1_sizer = wx.BoxSizer(wx.VERTICAL)
        p1_sizer.Add(wx.StaticText(panel1, label="First nested tab with text controls:"), 0, wx.ALL, 5)
        self.nested_text1 = wx.TextCtrl(panel1, value="Text in nested tab 1")
        p1_sizer.Add(self.nested_text1, 0, wx.ALL | wx.EXPAND, 5)
        self.nested_check1 = wx.CheckBox(panel1, label="Checkbox in nested tab 1")
        p1_sizer.Add(self.nested_check1, 0, wx.ALL, 5)
        panel1.SetSizer(p1_sizer)
        self.notebook.AddPage(panel1, "Text Controls")
        
        # Tab 2: Buttons
        panel2 = wx.Panel(self.notebook)
        p2_sizer = wx.BoxSizer(wx.VERTICAL)
        p2_sizer.Add(wx.StaticText(panel2, label="Second nested tab with buttons:"), 0, wx.ALL, 5)
        self.nested_btn1 = wx.Button(panel2, label="Button 1")
        p2_sizer.Add(self.nested_btn1, 0, wx.ALL, 5)
        self.nested_btn2 = wx.Button(panel2, label="Button 2")
        p2_sizer.Add(self.nested_btn2, 0, wx.ALL, 5)
        panel2.SetSizer(p2_sizer)
        self.notebook.AddPage(panel2, "Buttons")
        
        # Tab 3: List
        panel3 = wx.Panel(self.notebook)
        p3_sizer = wx.BoxSizer(wx.VERTICAL)
        p3_sizer.Add(wx.StaticText(panel3, label="Third nested tab with list:"), 0, wx.ALL, 5)
        self.nested_list = wx.ListBox(panel3, choices=[f"Item {i+1}" for i in range(10)])
        p3_sizer.Add(self.nested_list, 1, wx.ALL | wx.EXPAND, 5)
        panel3.SetSizer(p3_sizer)
        self.notebook.AddPage(panel3, "List")
        
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_notebook_changed)
        
        sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 5)
        
        self.notebook_label = wx.StaticText(parent, label="Selected tab: Text Controls")
        sizer.Add(self.notebook_label, 0, wx.ALL, 5)
        
        return sizer
        
    # Event handlers
    def on_html_link(self, event):
        """Handle HTML link clicks."""
        link = event.GetLinkInfo().GetHref()
        self.html_label.SetLabel(f"Link clicked: {link}")
        self.main_frame.update_status_bar(
            "HTML Link",
            f"Link: {link}",
            "Would open in browser"
        )
        # Note: event.Skip() would try to open in browser
        # We don't skip to prevent actual navigation in this test app
        
    def on_dir_selected(self, event):
        """Handle directory selection."""
        path = self.dirctrl.GetPath()
        self.dir_label.SetLabel(f"Selected: {path}")
        self.main_frame.update_status_bar(
            "Directory",
            path,
            "Arrow keys to navigate, Enter to select"
        )
        
    def on_notebook_changed(self, event):
        """Handle notebook tab change."""
        sel = self.notebook.GetSelection()
        page_text = self.notebook.GetPageText(sel)
        self.notebook_label.SetLabel(f"Selected tab: {page_text}")
        self.main_frame.update_status_bar(
            "Nested Notebook",
            f"Tab: {page_text}",
            "Ctrl+Tab to switch tabs, Tab for controls"
        )
        event.Skip()
        
    def on_control_focus(self, event):
        """Handle focus events."""
        ctrl = event.GetEventObject()
        
        if isinstance(ctrl, wx.html.HtmlWindow):
            self.main_frame.update_status_bar(
                "HTML Window",
                "HTML content with links and formatting",
                "Tab for links, Enter to activate, Screen reader announces HTML structure"
            )
        elif isinstance(ctrl, wx.stc.StyledTextCtrl):
            line = ctrl.GetCurrentLine() + 1
            col = ctrl.GetColumn(ctrl.GetCurrentPos()) + 1
            self.main_frame.update_status_bar(
                "Code Editor",
                f"Line {line}, Column {col}",
                "Standard editing shortcuts: Ctrl+C/V/X/Z/Y, Home/End, Ctrl+Home/End"
            )
        elif hasattr(ctrl, 'GetClassName') and 'TreeCtrl' in ctrl.GetClassName():
            self.main_frame.update_status_bar(
                "Directory Control",
                "Folder/file tree navigation",
                "Arrow keys to navigate, * to expand all, Type to search"
            )
        
        event.Skip()
        
    # State management
    def save_state(self):
        """Save tab state."""
        return {
            "html_content": self.html.ToText(),
            "dir_path": self.dirctrl.GetPath(),
            "stc_text": self.stc.GetText(),
            "stc_cursor": self.stc.GetCurrentPos(),
            "notebook_selection": self.notebook.GetSelection(),
            "nested_text1": self.nested_text1.GetValue(),
            "nested_check1": self.nested_check1.GetValue(),
            "nested_list_selection": self.nested_list.GetSelection()
        }
        
    def load_state(self, state):
        """Load tab state."""
        if "dir_path" in state and os.path.exists(state["dir_path"]):
            self.dirctrl.SetPath(state["dir_path"])
            
        if "stc_text" in state:
            self.stc.SetText(state["stc_text"])
            
        if "stc_cursor" in state:
            pos = state["stc_cursor"]
            if 0 <= pos <= self.stc.GetLength():
                self.stc.SetCurrentPos(pos)
                self.stc.SetSelection(pos, pos)
                
        if "notebook_selection" in state:
            sel = state["notebook_selection"]
            if 0 <= sel < self.notebook.GetPageCount():
                self.notebook.SetSelection(sel)
                
        if "nested_text1" in state:
            self.nested_text1.SetValue(state["nested_text1"])
            
        if "nested_check1" in state:
            self.nested_check1.SetValue(state["nested_check1"])
            
        if "nested_list_selection" in state:
            sel = state["nested_list_selection"]
            if 0 <= sel < self.nested_list.GetCount():
                self.nested_list.SetSelection(sel)
                
    def reset_to_defaults(self):
        """Reset tab to default state."""
        self.dirctrl.SetPath(str(Path.home()))
        self.stc.SetText("")
        self.notebook.SetSelection(0)
        self.nested_text1.SetValue("Text in nested tab 1")
        self.nested_check1.SetValue(False)
        self.nested_list.SetSelection(0)
