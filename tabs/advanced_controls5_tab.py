"""Advanced Controls 5 Tab - Final Missing Controls.

Tests for Treebook, Toolbook, AnimationCtrl, CommandLinkButton, HtmlListBox, FileCtrl.
Completes comprehensive wxPython control coverage.
"""

import wx
import wx.adv
import wx.html
from state_manager import TabStateHelper
from pathlib import Path


class AdvancedControls5Tab(wx.Panel, TabStateHelper):
    """Tab containing final missing controls for complete accessibility testing."""
    
    def __init__(self, parent, main_frame):
        """Initialize advanced controls 5 tab and build UI."""
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Advanced Controls 5"
        
        scroll = wx.ScrolledWindow(self, style=wx.VSCROLL)
        scroll.SetScrollRate(0, 20)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Instructions
        inst_text = wx.StaticText(
            scroll,
            label="Final missing controls: Treebook (hierarchical navigation), Toolbook (toolbar navigation), "
                  "AnimationCtrl (animated GIFs), CommandLinkButton (modern Windows buttons), "
                  "HtmlListBox (HTML-formatted list items), and FileCtrl (file browser). "
                  "These complete comprehensive wxPython control coverage for accessibility testing."
        )
        inst_text.Wrap(800)
        main_sizer.Add(inst_text, 0, wx.ALL | wx.EXPAND, 10)
        
        # Add control groups
        main_sizer.Add(self._create_hierarchical_books_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_animation_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_command_link_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_htmllistbox_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(self._create_filectrl_group(scroll), 0, wx.ALL | wx.EXPAND, 10)
        
        scroll.SetSizer(main_sizer)
        
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(scroll, 1, wx.EXPAND)
        self.SetSizer(panel_sizer)
        
    def GetName(self):
        """Return human-readable tab name."""
        return self.tab_name
    
    def _create_hierarchical_books_group(self, parent):
        """Create Treebook and Toolbook controls group.
        
        Tests hierarchical navigation patterns:
        - Treebook: Tree-based page navigation (hierarchical structure)
        - Toolbook: Toolbar-based page navigation (icon-based)
        """
        box = wx.StaticBox(parent, label="Hierarchical Book Controls (Arrow keys to navigate)")
        sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        # Treebook - hierarchical navigation
        treebook_panel = wx.Panel(parent)
        treebook_sizer = wx.BoxSizer(wx.VERTICAL)
        treebook_sizer.Add(wx.StaticText(treebook_panel, label="Treebook (tree navigation):"), 0, wx.ALL, 5)
        
        self.treebook = wx.Treebook(treebook_panel, size=(400, 250))
        
        # Root pages with children
        # Chapter 1
        chapter1 = wx.Panel(self.treebook)
        wx.StaticText(chapter1, label="Chapter 1: Getting Started", pos=(10, 10))
        self.treebook_text1 = wx.TextCtrl(chapter1, value="Introduction text", pos=(10, 40), size=(300, 60), style=wx.TE_MULTILINE)
        self.treebook.AddPage(chapter1, "Chapter 1: Introduction")
        
        # Chapter 1 subsections
        section1_1 = wx.Panel(self.treebook)
        wx.StaticText(section1_1, label="Section 1.1: Installation", pos=(10, 10))
        self.treebook_check1 = wx.CheckBox(section1_1, label="Prerequisites completed", pos=(10, 40))
        self.treebook.AddSubPage(section1_1, "1.1 Installation")
        
        section1_2 = wx.Panel(self.treebook)
        wx.StaticText(section1_2, label="Section 1.2: Configuration", pos=(10, 10))
        self.treebook_spin1 = wx.SpinCtrl(section1_2, value="10", pos=(10, 40), min=1, max=100)
        self.treebook.AddSubPage(section1_2, "1.2 Configuration")
        
        # Chapter 2
        chapter2 = wx.Panel(self.treebook)
        wx.StaticText(chapter2, label="Chapter 2: Advanced Topics", pos=(10, 10))
        wx.TextCtrl(chapter2, value="Advanced content", pos=(10, 40), size=(300, 60), style=wx.TE_MULTILINE)
        self.treebook.AddPage(chapter2, "Chapter 2: Advanced")
        
        # Chapter 2 subsections
        section2_1 = wx.Panel(self.treebook)
        wx.StaticText(section2_1, label="Section 2.1: Performance", pos=(10, 10))
        self.treebook_slider = wx.Slider(section2_1, value=50, minValue=0, maxValue=100, pos=(10, 40), size=(250, -1))
        self.treebook.AddSubPage(section2_1, "2.1 Performance")
        
        section2_2 = wx.Panel(self.treebook)
        wx.StaticText(section2_2, label="Section 2.2: Security", pos=(10, 10))
        self.treebook_radio = wx.RadioBox(section2_2, label="Security Level", choices=["Low", "Medium", "High"], pos=(10, 40))
        self.treebook.AddSubPage(section2_2, "2.2 Security")
        
        # Chapter 3
        chapter3 = wx.Panel(self.treebook)
        wx.StaticText(chapter3, label="Chapter 3: Reference", pos=(10, 10))
        wx.StaticText(chapter3, label="API documentation and examples", pos=(10, 40))
        self.treebook.AddPage(chapter3, "Chapter 3: Reference")
        
        self.treebook.Bind(wx.EVT_TREEBOOK_PAGE_CHANGED, self.on_treebook_changed)
        self.treebook.SetToolTip("Hierarchical page navigation - Arrow keys to navigate tree, Enter to activate")
        
        treebook_sizer.Add(self.treebook, 1, wx.ALL | wx.EXPAND, 5)
        
        # Selection display
        self.treebook_label = wx.StaticText(treebook_panel, label="Selected: Chapter 1: Introduction")
        treebook_sizer.Add(self.treebook_label, 0, wx.ALL, 5)
        
        treebook_panel.SetSizer(treebook_sizer)
        sizer.Add(treebook_panel, 1, wx.ALL | wx.EXPAND, 5)
        
        # Toolbook - toolbar navigation
        toolbook_panel = wx.Panel(parent)
        toolbook_sizer = wx.BoxSizer(wx.VERTICAL)
        toolbook_sizer.Add(wx.StaticText(toolbook_panel, label="Toolbook (toolbar navigation):"), 0, wx.ALL, 5)
        
        self.toolbook = wx.Toolbook(toolbook_panel, size=(400, 250))
        
        # Get image list for icons
        il = wx.ImageList(16, 16)
        il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16, 16)))
        il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, (16, 16)))
        il.Add(wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_TOOLBAR, (16, 16)))
        il.Add(wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, (16, 16)))
        self.toolbook.AssignImageList(il)
        
        # Add pages with icons
        page1 = wx.Panel(self.toolbook)
        wx.StaticText(page1, label="Open/Import Content", pos=(10, 10))
        self.toolbook_text1 = wx.TextCtrl(page1, value="File path", pos=(10, 40), size=(300, -1))
        self.toolbook_btn1 = wx.Button(page1, label="Browse...", pos=(320, 38))
        self.toolbook.AddPage(page1, "Open", imageId=0)
        
        page2 = wx.Panel(self.toolbook)
        wx.StaticText(page2, label="Save/Export Content", pos=(10, 10))
        self.toolbook_check2 = wx.CheckBox(page2, label="Create backup", pos=(10, 40))
        self.toolbook_check3 = wx.CheckBox(page2, label="Compress", pos=(10, 70))
        self.toolbook.AddPage(page2, "Save", imageId=1)
        
        page3 = wx.Panel(self.toolbook)
        wx.StaticText(page3, label="Print Settings", pos=(10, 10))
        self.toolbook_choice = wx.Choice(page3, choices=["Portrait", "Landscape"], pos=(10, 40))
        self.toolbook_choice.SetSelection(0)
        self.toolbook.AddPage(page3, "Print", imageId=2)
        
        page4 = wx.Panel(self.toolbook)
        wx.StaticText(page4, label="Help & Documentation", pos=(10, 10))
        wx.StaticText(page4, label="Version 1.0 - Accessibility Test Suite", pos=(10, 40))
        self.toolbook.AddPage(page4, "Help", imageId=3)
        
        self.toolbook.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.on_toolbook_changed)
        self.toolbook.SetToolTip("Icon-based page navigation - Tab to toolbar, Arrow keys to navigate")
        
        toolbook_sizer.Add(self.toolbook, 1, wx.ALL | wx.EXPAND, 5)
        
        # Selection display
        self.toolbook_label = wx.StaticText(toolbook_panel, label="Selected: Open")
        toolbook_sizer.Add(self.toolbook_label, 0, wx.ALL, 5)
        
        toolbook_panel.SetSizer(toolbook_sizer)
        sizer.Add(toolbook_panel, 1, wx.ALL | wx.EXPAND, 5)
        
        return sizer
    
    def _create_animation_group(self, parent):
        """Create AnimationCtrl group.
        
        Tests animated image display:
        - Loading and playing animated GIFs
        - Start/Stop controls
        """
        box = wx.StaticBox(parent, label="Animation Control (Animated GIF playback)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="AnimationCtrl for displaying animated GIFs (throbbers, progress indicators):"
            ),
            0, wx.ALL, 5
        )
        
        # Animation control
        self.animation = wx.adv.AnimationCtrl(parent, size=(100, 100))
        self.animation.SetToolTip("Animated image control - Can display animated GIFs")
        
        # Create a simple animation programmatically (since we may not have GIF files)
        # Note: In real usage, you'd load from file: animation.LoadFile("spinner.gif")
        sizer.Add(self.animation, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        
        # Status label
        self.anim_status = wx.StaticText(parent, label="Status: No animation loaded")
        sizer.Add(self.anim_status, 0, wx.ALL, 5)
        
        # Control buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.anim_play_btn = wx.Button(parent, label="&Play")
        self.anim_play_btn.Bind(wx.EVT_BUTTON, self.on_animation_play)
        self.anim_play_btn.SetToolTip("Start animation playback")
        btn_sizer.Add(self.anim_play_btn, 0, wx.ALL, 5)
        
        self.anim_stop_btn = wx.Button(parent, label="&Stop")
        self.anim_stop_btn.Bind(wx.EVT_BUTTON, self.on_animation_stop)
        self.anim_stop_btn.SetToolTip("Stop animation playback")
        btn_sizer.Add(self.anim_stop_btn, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        
        # Note about usage
        note = wx.StaticText(
            parent,
            label="Note: To use animations, load GIF files with LoadFile(). "
                  "Commonly used for loading indicators and progress throbbers."
        )
        note.Wrap(700)
        sizer.Add(note, 0, wx.ALL, 5)
        
        return sizer
    
    def _create_command_link_group(self, parent):
        """Create CommandLinkButton group.
        
        Tests Windows Vista+ style command link buttons:
        - Main text with supplementary note
        - Modern Windows UI pattern
        """
        box = wx.StaticBox(parent, label="Command Link Buttons (Vista+ style buttons)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="CommandLinkButton provides Windows Vista+ style buttons with main label and note:"
            ),
            0, wx.ALL, 5
        )
        
        # Command Link Buttons
        self.cmd_link1 = wx.adv.CommandLinkButton(
            parent,
            label="Create New Project",
            note="Start a new project from scratch with default settings"
        )
        self.cmd_link1.Bind(wx.EVT_BUTTON, self.on_command_link)
        self.cmd_link1.SetToolTip("Command link button - Space/Enter to activate")
        sizer.Add(self.cmd_link1, 0, wx.ALL | wx.EXPAND, 5)
        
        self.cmd_link2 = wx.adv.CommandLinkButton(
            parent,
            label="Open Existing Project",
            note="Browse and open a previously saved project file"
        )
        self.cmd_link2.Bind(wx.EVT_BUTTON, self.on_command_link)
        self.cmd_link2.SetToolTip("Command link button - Space/Enter to activate")
        sizer.Add(self.cmd_link2, 0, wx.ALL | wx.EXPAND, 5)
        
        self.cmd_link3 = wx.adv.CommandLinkButton(
            parent,
            label="Import from Template",
            note="Create a new project based on an existing template or example"
        )
        self.cmd_link3.Bind(wx.EVT_BUTTON, self.on_command_link)
        self.cmd_link3.SetToolTip("Command link button - Space/Enter to activate")
        sizer.Add(self.cmd_link3, 0, wx.ALL | wx.EXPAND, 5)
        
        # Action display
        self.cmd_link_label = wx.StaticText(parent, label="Click a command link to see action")
        sizer.Add(self.cmd_link_label, 0, wx.ALL, 5)
        
        return sizer
    
    def _create_htmllistbox_group(self, parent):
        """Create HtmlListBox group.
        
        Tests HTML-formatted list items:
        - Rich text formatting in list items
        - Bold, italic, colors in list
        """
        box = wx.StaticBox(parent, label="HTML List Box (Arrow keys to navigate, Space to select)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="HtmlListBox allows HTML formatting in list items (bold, italic, colors, etc.):"
            ),
            0, wx.ALL, 5
        )
        
        # Custom HtmlListBox class
        class MyHtmlListBox(wx.html.HtmlListBox):
            """Custom HtmlListBox with formatted items."""
            
            def __init__(self, parent):
                """Initialize with sample items."""
                super().__init__(parent, size=(700, 200))
                self.items = [
                    "<b>Critical Alert:</b> <font color='red'>System requires immediate attention</font>",
                    "<b>Warning:</b> <font color='orange'>Disk space running low (15% remaining)</font>",
                    "<b>Information:</b> <font color='blue'>New updates are available for installation</font>",
                    "<b>Success:</b> <font color='green'>Backup completed successfully at 3:45 PM</font>",
                    "<i>Task:</i> Review <b>quarterly report</b> by <u>Friday</u>",
                    "<b>Email from:</b> John Smith - <i>Re: Meeting Schedule</i>",
                    "<font color='purple'><b>Event:</b> Team meeting at 2:00 PM in Conference Room A</font>",
                    "Plain text item without any HTML formatting",
                    "<b>File:</b> <font face='Courier New'>document.pdf</font> (Size: 2.5 MB)",
                    "<b>Status:</b> <font color='darkgreen'>Online</font> - Last seen: Just now"
                ]
                self.SetItemCount(len(self.items))
                
            def OnGetItem(self, n):
                """Return HTML for item n."""
                return self.items[n]
        
        self.htmllistbox = MyHtmlListBox(parent)
        self.htmllistbox.SetToolTip("List with HTML formatting - Arrow keys to navigate, Space to select")
        self.htmllistbox.Bind(wx.EVT_LISTBOX, self.on_htmllistbox_select)
        sizer.Add(self.htmllistbox, 1, wx.ALL | wx.EXPAND, 5)
        
        # Selection display
        self.htmllistbox_label = wx.StaticText(parent, label="Selected: (none)")
        sizer.Add(self.htmllistbox_label, 0, wx.ALL, 5)
        
        return sizer
    
    def _create_filectrl_group(self, parent):
        """Create FileCtrl group.
        
        Tests file browser control:
        - File system navigation
        - File filtering
        - File selection
        """
        box = wx.StaticBox(parent, label="File Control (Arrow keys to navigate, Enter to select)")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        sizer.Add(
            wx.StaticText(
                parent,
                label="FileCtrl provides file system browsing with filtering support:"
            ),
            0, wx.ALL, 5
        )
        
        # Start in user's home directory
        start_dir = str(Path.home())
        
        # File control with wildcard filter
        self.filectrl = wx.FileCtrl(
            parent,
            defaultDirectory=start_dir,
            wildCard="All files (*.*)|*.*|"
                     "Python files (*.py)|*.py|"
                     "Text files (*.txt)|*.txt|"
                     "Documents (*.doc;*.docx;*.pdf)|*.doc;*.docx;*.pdf",
            style=wx.FC_OPEN | wx.FC_MULTIPLE,
            size=(700, 250)
        )
        self.filectrl.SetToolTip("File browser - Arrow keys to navigate, Enter to select, Type to filter")
        self.filectrl.Bind(wx.EVT_FILECTRL_SELECTIONCHANGED, self.on_file_selected)
        self.filectrl.Bind(wx.EVT_FILECTRL_FILEACTIVATED, self.on_file_activated)
        self.filectrl.Bind(wx.EVT_FILECTRL_FOLDERCHANGED, self.on_folder_changed)
        
        sizer.Add(self.filectrl, 1, wx.ALL | wx.EXPAND, 5)
        
        # Current path display
        self.file_path_label = wx.StaticText(parent, label=f"Current directory: {start_dir}")
        self.file_path_label.Wrap(700)
        sizer.Add(self.file_path_label, 0, wx.ALL, 5)
        
        # Selected file display
        self.file_select_label = wx.StaticText(parent, label="Selected: (none)")
        sizer.Add(self.file_select_label, 0, wx.ALL, 5)
        
        return sizer
    
    # Event handlers
    
    def on_treebook_changed(self, event):
        """Handle Treebook page change."""
        page_idx = self.treebook.GetSelection()
        if page_idx != wx.NOT_FOUND:
            page_text = self.treebook.GetPageText(page_idx)
            self.treebook_label.SetLabel(f"Selected: {page_text}")
        event.Skip()
    
    def on_toolbook_changed(self, event):
        """Handle Toolbook page change."""
        page_idx = self.toolbook.GetSelection()
        if page_idx != wx.NOT_FOUND:
            page_text = self.toolbook.GetPageText(page_idx)
            self.toolbook_label.SetLabel(f"Selected: {page_text}")
        event.Skip()
    
    def on_animation_play(self, event):
        """Play animation."""
        if self.animation.IsOk():
            self.animation.Play()
            self.anim_status.SetLabel("Status: Playing")
        else:
            self.anim_status.SetLabel("Status: No animation loaded (load GIF file with LoadFile())")
    
    def on_animation_stop(self, event):
        """Stop animation."""
        if self.animation.IsOk():
            self.animation.Stop()
            self.anim_status.SetLabel("Status: Stopped")
    
    def on_command_link(self, event):
        """Handle command link button clicks."""
        btn = event.GetEventObject()
        label = btn.GetLabel()
        self.cmd_link_label.SetLabel(f"Action: {label}")
        self.main_frame.update_status_bar(
            f"Command Link: {label}",
            "Command link activated",
            "Space/Enter to activate"
        )
    
    def on_htmllistbox_select(self, event):
        """Handle HtmlListBox selection."""
        sel = self.htmllistbox.GetSelection()
        if sel != wx.NOT_FOUND:
            # Get plain text version (strip HTML)
            html_text = self.htmllistbox.items[sel]
            import re
            plain_text = re.sub('<[^<]+?>', '', html_text)
            self.htmllistbox_label.SetLabel(f"Selected: {plain_text}")
    
    def on_file_selected(self, event):
        """Handle file selection change."""
        paths = self.filectrl.GetPaths()
        if paths:
            if len(paths) == 1:
                self.file_select_label.SetLabel(f"Selected: {paths[0]}")
            else:
                self.file_select_label.SetLabel(f"Selected: {len(paths)} files")
        else:
            self.file_select_label.SetLabel("Selected: (none)")
    
    def on_file_activated(self, event):
        """Handle file activation (double-click or Enter)."""
        paths = self.filectrl.GetPaths()
        if paths:
            self.main_frame.update_status_bar(
                f"File activated: {Path(paths[0]).name}",
                f"Full path: {paths[0]}",
                "Double-click or Enter to activate"
            )
    
    def on_folder_changed(self, event):
        """Handle folder navigation."""
        path = self.filectrl.GetDirectory()
        self.file_path_label.SetLabel(f"Current directory: {path}")
    
    # State management
    
    def save_state(self):
        """Save control states."""
        state = {
            # Treebook
            "treebook_selection": self.treebook.GetSelection(),
            "treebook_text1": self.treebook_text1.GetValue(),
            "treebook_check1": self.treebook_check1.GetValue(),
            "treebook_spin1": self.treebook_spin1.GetValue(),
            "treebook_slider": self.treebook_slider.GetValue(),
            "treebook_radio": self.treebook_radio.GetSelection(),
            
            # Toolbook
            "toolbook_selection": self.toolbook.GetSelection(),
            "toolbook_text1": self.toolbook_text1.GetValue(),
            "toolbook_check2": self.toolbook_check2.GetValue(),
            "toolbook_check3": self.toolbook_check3.GetValue(),
            "toolbook_choice": self.toolbook_choice.GetSelection(),
            
            # HtmlListBox
            "htmllistbox_selection": self.htmllistbox.GetSelection(),
            
            # FileCtrl
            "filectrl_directory": self.filectrl.GetDirectory(),
            "filectrl_filter": self.filectrl.GetFilterIndex(),
        }
        return state
    
    def load_state(self, state):
        """Load control states."""
        if not state:
            return
        
        # Treebook
        if "treebook_selection" in state and state["treebook_selection"] != wx.NOT_FOUND:
            self.treebook.SetSelection(state["treebook_selection"])
        if "treebook_text1" in state:
            self.treebook_text1.SetValue(state["treebook_text1"])
        if "treebook_check1" in state:
            self.treebook_check1.SetValue(state["treebook_check1"])
        if "treebook_spin1" in state:
            self.treebook_spin1.SetValue(state["treebook_spin1"])
        if "treebook_slider" in state:
            self.treebook_slider.SetValue(state["treebook_slider"])
        if "treebook_radio" in state:
            self.treebook_radio.SetSelection(state["treebook_radio"])
        
        # Toolbook
        if "toolbook_selection" in state and state["toolbook_selection"] != wx.NOT_FOUND:
            self.toolbook.SetSelection(state["toolbook_selection"])
        if "toolbook_text1" in state:
            self.toolbook_text1.SetValue(state["toolbook_text1"])
        if "toolbook_check2" in state:
            self.toolbook_check2.SetValue(state["toolbook_check2"])
        if "toolbook_check3" in state:
            self.toolbook_check3.SetValue(state["toolbook_check3"])
        if "toolbook_choice" in state:
            self.toolbook_choice.SetSelection(state["toolbook_choice"])
        
        # HtmlListBox
        if "htmllistbox_selection" in state and state["htmllistbox_selection"] != wx.NOT_FOUND:
            self.htmllistbox.SetSelection(state["htmllistbox_selection"])
        
        # FileCtrl
        if "filectrl_directory" in state:
            try:
                self.filectrl.SetDirectory(state["filectrl_directory"])
            except:
                pass  # Directory may no longer exist
        if "filectrl_filter" in state:
            self.filectrl.SetFilterIndex(state["filectrl_filter"])
    
    def reset_to_defaults(self):
        """Reset all controls to default values."""
        # Treebook
        self.treebook.SetSelection(0)
        self.treebook_text1.SetValue("Introduction text")
        self.treebook_check1.SetValue(False)
        self.treebook_spin1.SetValue(10)
        self.treebook_slider.SetValue(50)
        self.treebook_radio.SetSelection(0)
        
        # Toolbook
        self.toolbook.SetSelection(0)
        self.toolbook_text1.SetValue("File path")
        self.toolbook_check2.SetValue(False)
        self.toolbook_check3.SetValue(False)
        self.toolbook_choice.SetSelection(0)
        
        # HtmlListBox
        self.htmllistbox.SetSelection(wx.NOT_FOUND)
        
        # FileCtrl
        self.filectrl.SetDirectory(str(Path.home()))
        self.filectrl.SetFilterIndex(0)
