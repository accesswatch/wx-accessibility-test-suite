"""wxPython Accessibility Test Suite.

Comprehensive test application for validating keyboard navigation and
screen reader accessibility of wxPython controls according to WCAG 2.2
AA guidelines.

Target: Windows with NVDA/JAWS/Narrator
Python: 3.10-3.13
wxPython: Latest (4.2.x+)
"""

import wx
import sys
import json
from pathlib import Path
import logging

# Configure basic logging so modules using logging emit to console by default
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s'
)

# Import tab modules (will be created)
from tabs.basic_controls_tab import BasicControlsTab
from tabs.listctrl_tab import ListCtrlTab
from tabs.listctrl_views_tab import ListCtrlViewsTab
from tabs.treectrl_tab import TreeCtrlTab
from tabs.grid_tab import GridTab
from tabs.advanced_controls_tab import AdvancedControlsTab
from tabs.validation_tab import ValidationTab
from tabs.media_controls_tab import MediaControlsTab
from tabs.buttons_toolbar_tab import ButtonsToolbarTab
from tabs.advanced_controls2_tab import AdvancedControls2Tab
from tabs.advanced_media_tab import AdvancedMediaTab
from tabs.advanced_controls3_tab import AdvancedControls3Tab

from state_manager import StateManager


class AccessibilityTestFrame(wx.Frame):
    """Main application frame with tabbed interface for control testing."""
    
    def __init__(self):
        """Initialize the main application frame and build the UI.

        Sets up menu, status bar, notebook tabs, and loads saved state.
        """
        super().__init__(
            parent=None,
            title="wxPython Accessibility Test Suite - WCAG 2.2 AA Validation",
            size=(1200, 800)
        )
        
        self.state_manager = StateManager()
        self.tabs = []
        
        # Set up UI
        self._create_menu_bar()
        self._create_status_bar()
        self._create_notebook()
        
        # Window events
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        # Load saved state
        self.state_manager.load_state(self)
        
        self.Centre()
        self.Show()
        
    def _create_menu_bar(self):
        """Create application menu bar with keyboard mnemonics.
        
        Menu provides keyboard shortcuts for common operations:
        - Save/Load state for testing state persistence
        - Reset to defaults for reproducible testing
        - Exit with auto-save to preserve work
        
        All menu items have mnemonics (underlined letters) for keyboard access.
        Screen readers will announce menu structure and shortcuts.
        """
        menu_bar = wx.MenuBar()
        
        # File menu - contains state management and exit options
        file_menu = wx.Menu()
        
        save_item = file_menu.Append(
            wx.ID_SAVE,
            "&Save State\tCtrl+S",
            "Save current state of all controls"
        )
        self.Bind(wx.EVT_MENU, self.on_save_state, save_item)
        
        load_item = file_menu.Append(
            wx.ID_OPEN,
            "&Load State\tCtrl+O",
            "Load previously saved state"
        )
        self.Bind(wx.EVT_MENU, self.on_load_state, load_item)
        
        reset_item = file_menu.Append(
            wx.ID_CLEAR,
            "&Reset to Defaults\tCtrl+R",
            "Reset all controls to default test data"
        )
        self.Bind(wx.EVT_MENU, self.on_reset_state, reset_item)
        
        file_menu.AppendSeparator()
        
        exit_item = file_menu.Append(
            wx.ID_EXIT,
            "E&xit\tAlt+F4",
            "Exit application (auto-saves state)"
        )
        self.Bind(wx.EVT_MENU, self.on_close, exit_item)
        
        menu_bar.Append(file_menu, "&File")
        
        # Help menu
        help_menu = wx.Menu()
        
        about_item = help_menu.Append(
            wx.ID_ABOUT,
            "&About\tF1",
            "About this application"
        )
        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        
        menu_bar.Append(help_menu, "&Help")
        
        self.SetMenuBar(menu_bar)
        
    def _create_status_bar(self):
        """Create status bar with 3 fields: control info, role/state, keyboard hint.
        
        Status bar provides contextual information about focused controls:
        - Field 0 (40%): Control name and description
        - Field 1 (40%): Role, state, and value (for verifying screen reader output)
        - Field 2 (20%): Keyboard shortcuts and navigation hints
        
        Tabs update these fields when controls receive focus, helping testers
        verify that assistive technologies are receiving correct information.
        """
        self.status_bar = self.CreateStatusBar(3)
        # Use negative widths for proportional sizing (-2:-2:-1 = 40%:40%:20%)
        self.status_bar.SetStatusWidths([-2, -2, -1])
        self.SetStatusText("Ready - Use Tab to navigate controls", 0)
        self.SetStatusText("", 1)
        self.SetStatusText("Press F1 for help", 2)
        
    def _create_notebook(self):
        """Create notebook with test tabs.
        
        Tabs are ordered from simple to complex:
        1. Basic controls (buttons, text, checkboxes)
        2-4. Complex lists/trees/grids with embedded checkboxes
        5-9. Advanced controls (pickers, media, toolbars, etc.)
        10. Validation checklist and documentation
        
        Each tab inherits from TabStateHelper to support state persistence.
        """
        self.notebook = wx.Notebook(self, style=wx.NB_TOP)
        
        # Create tabs in logical progression
        self.tabs.append(BasicControlsTab(self.notebook, self))
        self.tabs.append(ListCtrlTab(self.notebook, self))
        self.tabs.append(ListCtrlViewsTab(self.notebook, self))  # Multiple view modes, no checkboxes
        self.tabs.append(TreeCtrlTab(self.notebook, self))
        self.tabs.append(GridTab(self.notebook, self))
        self.tabs.append(AdvancedControlsTab(self.notebook, self))
        self.tabs.append(MediaControlsTab(self.notebook, self))
        self.tabs.append(ButtonsToolbarTab(self.notebook, self))
        self.tabs.append(AdvancedControls2Tab(self.notebook, self))
        self.tabs.append(AdvancedMediaTab(self.notebook, self))
        self.tabs.append(AdvancedControls3Tab(self.notebook, self))
        self.tabs.append(ValidationTab(self.notebook, self))
        
        # Add tabs to notebook
        for tab in self.tabs:
            self.notebook.AddPage(tab, tab.GetName())
            
        # Notebook events
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_changed)
        
    def update_status_bar(self, control_info="", role_state="", keyboard_hint=""):
        """Update status bar fields with current control information.
        
        Args:
            control_info: Control name and description
            role_state: Role, state, and value information (for screen reader verification)
            keyboard_hint: Keyboard shortcut hints
        """
        if control_info:
            self.SetStatusText(control_info, 0)
        if role_state:
            self.SetStatusText(role_state, 1)
        if keyboard_hint:
            self.SetStatusText(keyboard_hint, 2)
            
    def on_tab_changed(self, event):
        """Handle tab selection change."""
        selection = self.notebook.GetSelection()
        if selection != wx.NOT_FOUND:
            page = self.notebook.GetPage(selection)
            self.update_status_bar(
                f"Tab: {page.GetName()}",
                "",
                "Tab/Shift+Tab to navigate"
            )
        event.Skip()
        
    def on_save_state(self, event):
        """Manually save application state."""
        self.state_manager.save_state(self)
        wx.MessageBox(
            "Application state saved successfully.",
            "State Saved",
            wx.OK | wx.ICON_INFORMATION
        )
        
    def on_load_state(self, event):
        """Manually load application state."""
        result = wx.MessageBox(
            "Load saved state? Current changes will be lost.",
            "Load State",
            wx.YES_NO | wx.ICON_QUESTION
        )
        if result == wx.YES:
            self.state_manager.load_state(self)
            wx.MessageBox(
                "Application state loaded successfully.",
                "State Loaded",
                wx.OK | wx.ICON_INFORMATION
            )
            
    def on_reset_state(self, event):
        """Reset all controls to default test data."""
        result = wx.MessageBox(
            "Reset all controls to default test data? Current changes will be lost.",
            "Reset to Defaults",
            wx.YES_NO | wx.ICON_WARNING
        )
        if result == wx.YES:
            for tab in self.tabs:
                tab.reset_to_defaults()
            wx.MessageBox(
                "All controls reset to default test data.",
                "Reset Complete",
                wx.OK | wx.ICON_INFORMATION
            )
            
    def on_about(self, event):
        """Show about dialog."""
        info = wx.adv.AboutDialogInfo()
        info.SetName("wxPython Accessibility Test Suite")
        info.SetVersion("1.0")
        info.SetDescription(
            "Comprehensive test application for validating keyboard navigation "
            "and screen reader accessibility of wxPython controls.\n\n"
            "Designed for WCAG 2.2 AA compliance testing with:\n"
            "• NVDA\n"
            "• JAWS\n"
            "• Microsoft Narrator\n\n"
            "All controls support keyboard-only operation with proper "
            "name/role/state exposure for assistive technologies."
        )
        info.SetWebSite("https://www.wxpython.org")
        info.AddDeveloper("Accessibility Testing Team")
        
        wx.adv.AboutBox(info)
        
    def on_close(self, event):
        """Handle window close event with auto-save.
        
        Auto-saves state to enable testing workflows:
        - Modify controls, close app, reopen to verify state restoration
        - Test long workflows across multiple sessions
        - Compare state files before/after changes
        
        State includes window geometry, all control values, and selections.
        """
        # Auto-save state before closing (no confirmation needed)
        self.state_manager.save_state(self)
        
        # Destroy window and exit application
        self.Destroy()


def main():
    """Application entry point."""
    app = wx.App(False)
    frame = AccessibilityTestFrame()
    app.MainLoop()


if __name__ == "__main__":
    main()
