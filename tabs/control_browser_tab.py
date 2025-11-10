"""Control Browser Tab (A→Z).

MVP Control Browser that lists controls from `data/controls.json` and
provides a multi-line editable field containing descriptions and expectations.

User edits are persisted via the existing `StateManager` (saved into
`state/app_state.json` by `StateManager.save_state`).
"""

import wx
import json
from pathlib import Path
from state_manager import TabStateHelper


class ControlBrowserTab(wx.Panel, TabStateHelper):
    """A tab that lists available controls and shows/edit descriptions.

    By default the multi-line editor is populated with the concatenation
    of all control descriptions and expectations (one per control). The
    content is saved to the application's state file so edits persist
    across runs.
    """

    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Control Browser"

        # Load controls data
        self.controls_path = Path("data") / "controls.json"
        self.controls = self._load_controls()

        # Build UI
        self._build_ui()

        # Populate editor with all descriptions+expectations by default
        self._populate_all_descriptions()

    def GetName(self):
        return self.tab_name

    def _load_controls(self):
        if not self.controls_path.exists():
            return []
        try:
            with open(self.controls_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _build_ui(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left: Search + list
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.search = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.search.SetToolTip("Type to filter controls (press Enter to apply)")
        self.search.Bind(wx.EVT_TEXT, self.on_search)
        left_sizer.Add(self.search, 0, wx.EXPAND | wx.ALL, 6)

        names = [c.get('name', c.get('id', '')) for c in self.controls]
        self.listbox = wx.ListBox(self, choices=names, style=wx.LB_SINGLE)
        self.listbox.Bind(wx.EVT_LISTBOX, self.on_select)
        left_sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 6)

        # Right: Description editor + buttons
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        box = wx.StaticBox(self, label="Descriptions & Expectations")
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.editor = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.editor.SetMinSize((400, 300))
        self.editor.SetToolTip("Edit descriptions and expectations. Press Save to persist.")
        box_sizer.Add(self.editor, 1, wx.EXPAND | wx.ALL, 6)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.save_btn = wx.Button(self, label="Save")
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        btn_sizer.Add(self.save_btn, 0, wx.ALL, 6)

        self.reset_btn = wx.Button(self, label="Reset Editor")
        self.reset_btn.Bind(wx.EVT_BUTTON, self.on_reset_editor)
        btn_sizer.Add(self.reset_btn, 0, wx.ALL, 6)

        self.show_all_chk = wx.CheckBox(self, label="Show all descriptions")
        self.show_all_chk.SetValue(True)
        self.show_all_chk.Bind(wx.EVT_CHECKBOX, self.on_toggle_show_all)
        btn_sizer.Add(self.show_all_chk, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 6)

        box_sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT)
        right_sizer.Add(box_sizer, 1, wx.EXPAND | wx.ALL, 6)

        main_sizer.Add(left_sizer, 0, wx.EXPAND)
        main_sizer.Add(right_sizer, 1, wx.EXPAND)

        self.SetSizer(main_sizer)

    def _format_control_text(self, control):
        name = control.get('name', control.get('id', ''))
        desc = control.get('description', '')
        expect = control.get('expectations', '')
        return f"{name}\n---\n{desc}\n\nExpectations:\n{expect}\n\n"

    def _populate_all_descriptions(self):
        texts = [self._format_control_text(c) for c in self.controls]
        combined = "".join(texts)
        self.editor.SetValue(combined)

    # Event handlers
    def on_search(self, event):
        term = self.search.GetValue().strip().lower()
        choices = []
        for c in self.controls:
            name = c.get('name', '')
            tags = ' '.join(c.get('tags', []))
            if not term or term in name.lower() or term in tags.lower() or term in c.get('id', ''):
                choices.append(name)
        # update listbox while preserving selection index where possible
        sel = self.listbox.GetSelection()
        self.listbox.Set(choices)
        if sel != wx.NOT_FOUND and sel < self.listbox.GetCount():
            self.listbox.SetSelection(sel)

    def on_select(self, event):
        idx = self.listbox.GetSelection()
        # Map listbox selection back to control; when search filtered we match by name
        name = self.listbox.GetString(idx)
        control = next((c for c in self.controls if c.get('name') == name), None)
        if control:
            text = self._format_control_text(control)
            # If show_all is checked, keep full content but move caret to this control's section
            if self.show_all_chk.GetValue():
                # Ensure editor contains all; if not, refill
                if not self.editor.GetValue():
                    self._populate_all_descriptions()
                # Find the control section and place caret at start
                pos = self.editor.GetValue().find(text)
                if pos >= 0:
                    self.editor.SetInsertionPoint(pos)
                else:
                    # Append control text if missing
                    self.editor.AppendText(text)
            else:
                # Replace editor content with only this control's text
                self.editor.SetValue(text)

    def on_save(self, event):
        # Save the current editor content to state; actual file write done by StateManager
        wx.MessageBox("Editor content saved to application state (when you Save State from File menu).", "Info", wx.OK | wx.ICON_INFORMATION)

    def on_reset_editor(self, event):
        # Reset to combined original descriptions from data/controls.json
        self._populate_all_descriptions()
        self.show_all_chk.SetValue(True)

    def on_toggle_show_all(self, event):
        if self.show_all_chk.GetValue():
            # show all
            if not self.editor.GetValue():
                self._populate_all_descriptions()
        else:
            # show only selected control if any
            sel = self.listbox.GetSelection()
            if sel != wx.NOT_FOUND:
                self.on_select(None)

    # State management
    def save_state(self):
        return {
            "all_descriptions": self.editor.GetValue(),
            "show_all": bool(self.show_all_chk.GetValue())
        }

    def load_state(self, state):
        if not state:
            return
        if "all_descriptions" in state:
            try:
                self.editor.SetValue(state["all_descriptions"])
            except Exception:
                # defensive: ignore problems restoring
                pass
        if "show_all" in state:
            try:
                self.show_all_chk.SetValue(bool(state.get("show_all", True)))
            except Exception:
                pass

    def reset_to_defaults(self):
        self._populate_all_descriptions()
        self.show_all_chk.SetValue(True)
