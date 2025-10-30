"""State Manager.

Handles serialization and deserialization of application state to JSON files.
"""

import json
from pathlib import Path
from typing import Dict, Any
import wx


class StateManager:
    """Manages loading and saving application state."""
    
    def __init__(self, state_dir: str = "state"):
        """Create a StateManager and ensure the state directory exists.

        Args:
            state_dir: Directory path where state files are stored.
        """
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)
        self.state_file = self.state_dir / "app_state.json"
        
    def save_state(self, frame):
        """Save complete application state to JSON.
        
        Captures all application state for reproducible testing:
        - Window geometry (size, position, maximized state)
        - Active tab selection
        - All control values from each tab (via tab.save_state())
        
        JSON format enables:
        - Human readability for debugging
        - Easy comparison between states (git diff)
        - External modification for test data generation
        
        Args:
            frame: AccessibilityTestFrame instance
        """
        state = {
            # Window state - restore exact testing environment
            "window": {
                "size": frame.GetSize().Get(),  # (width, height)
                "position": frame.GetPosition().Get(),  # (x, y)
                "maximized": frame.IsMaximized()  # Full screen state
            },
            # Notebook state - restore active tab
            "notebook": {
                "selected_tab": frame.notebook.GetSelection()  # Tab index
            },
            # Per-tab state - delegated to each tab's save_state() method
            "tabs": {}
        }
        
        # Save state from each tab
        # Each tab implements save_state() to return a dict of its control values
        # Tab names are used as keys (not indices) for stability across reordering
        for i, tab in enumerate(frame.tabs):
            tab_name = tab.GetName()
            # All tabs should implement save_state(), but check for safety
            if hasattr(tab, 'save_state'):
                state["tabs"][tab_name] = tab.save_state()
                
        # Write to file
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving state: {e}")
            
    def load_state(self, frame):
        """Load application state from JSON.
        
        Restores saved state if available, otherwise leaves defaults.
        Called after UI creation to apply saved values to controls.
        
        Gracefully handles:
        - Missing state file (first run)
        - Corrupted JSON (logs error, continues with defaults)
        - Missing tabs (skips restoration for removed tabs)
        - Changed control structure (tabs ignore unrecognized keys)
        
        Args:
            frame: AccessibilityTestFrame instance
        """
        # No state file on first run - use default test data
        if not self.state_file.exists():
            return
            
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                
            # Restore window state
            # Applied before tab restoration so controls are visible at correct size
            if "window" in state:
                win_state = state["window"]
                # Restore size before position to avoid off-screen windows
                if "size" in win_state:
                    frame.SetSize(win_state["size"])
                if "position" in win_state:
                    frame.SetPosition(win_state["position"])
                # Maximize last to override size/position if needed
                if win_state.get("maximized", False):
                    frame.Maximize()
                    
            # Restore notebook selection
            # Done last so the correct tab is active when window appears
            if "notebook" in state and "selected_tab" in state["notebook"]:
                sel = state["notebook"]["selected_tab"]
                # Validate selection is within range (tabs might have been added/removed)
                if 0 <= sel < frame.notebook.GetPageCount():
                    frame.notebook.SetSelection(sel)
                    
            # Restore tab states
            # Each tab's load_state() receives its saved dict and applies values to controls
            if "tabs" in state:
                for tab in frame.tabs:
                    tab_name = tab.GetName()
                    # Check if we have saved state for this tab (might be new)
                    # and tab implements load_state() (all should, but check for safety)
                    if tab_name in state["tabs"] and hasattr(tab, 'load_state'):
                        tab.load_state(state["tabs"][tab_name])
                        
        except Exception as e:
            print(f"Error loading state: {e}")


class TabStateHelper:
    """Helper mixin for tabs to implement state save/load.
    
    All tab classes should inherit from this mixin (along with wx.Panel)
    and implement these three methods for consistent state management:
    
    1. save_state() - Return dict of all control values
    2. load_state() - Apply dict values to controls
    3. reset_to_defaults() - Reset controls to initial test data
    
    This enables:
    - State persistence across application runs
    - Manual save/load for testing scenarios
    - Reproducible test data with reset functionality
    """
    
    def save_state(self) -> Dict[str, Any]:
        """Override in subclass to save tab-specific state.
        
        Returns:
            Dict containing all control values in JSON-serializable format.
            Use descriptive keys matching control purposes (not wx IDs).
            
        Example:
            return {
                "text_input": self.text_ctrl.GetValue(),
                "checkbox_checked": self.checkbox.IsChecked(),
                "selected_index": self.choice.GetSelection()
            }
        """
        return {}
        
    def load_state(self, state: Dict[str, Any]):
        """Override in subclass to load tab-specific state.
        
        Apply saved values to controls. Should gracefully handle:
        - Missing keys (control was added after state was saved)
        - Invalid values (validate and skip if needed)
        - Type mismatches (use defaults if conversion fails)
        
        Args:
            state: Dict of control values from save_state()
            
        Example:
            if "text_input" in state:
                self.text_ctrl.SetValue(state["text_input"])
            if "checkbox_checked" in state:
                self.checkbox.SetValue(state["checkbox_checked"])
        """
        pass
        
    def reset_to_defaults(self):
        """Override in subclass to reset controls to default test data.
        
        Should restore controls to initial state with realistic test data:
        - Clear user input, restore default values
        - Reset selections to initial choices
        - Restore checkbox states to test-ready configurations
        - Repopulate lists/grids with sample data
        
        Used for:
        - Starting fresh test runs
        - Reproducing bugs with known-good data
        - Demos and screenshots
        """
        pass
