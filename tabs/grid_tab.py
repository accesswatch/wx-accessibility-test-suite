"""Grid Tab.

Tests for wx.grid.Grid with embedded checkbox cells.
Demonstrates spreadsheet-like navigation with mixed cell types.
"""

import wx
import wx.grid
from state_manager import TabStateHelper
from test_data import generate_grid_data, PRIORITIES, STATUSES


class GridTab(wx.Panel, TabStateHelper):
    """Tab containing Grid with checkbox cells for accessibility testing."""
    
    def __init__(self, parent, main_frame):
        """Initialize grid tab and build grid UI controls."""
        super().__init__(parent)
        self.main_frame = main_frame
        self.tab_name = "Grid with Checkbox Cells"
        self.grid_data = generate_grid_data(20, 10)
        
        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Instructions
        inst_text = wx.StaticText(
            self,
            label="Grid control with mixed cell types including checkboxes. "
                  "Arrow keys to navigate cells, F2 or Enter to edit, "
                  "Space to toggle checkboxes, Tab to move to next cell."
        )
        inst_text.Wrap(800)
        main_sizer.Add(inst_text, 0, wx.ALL | wx.EXPAND, 10)
        
        # Create Grid
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(20, 10)
        
        # Set column labels from header row
        headers = self.grid_data[0]
        for col, header in enumerate(headers):
            self.grid.SetColLabelValue(col, header)
            
        # Configure column attributes
        self._setup_columns()
        
        # Populate grid
        self._populate_grid()
        
        # Bind events
        self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.on_cell_select)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGING, self.on_cell_changing)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.on_cell_changed)
        self.grid.Bind(wx.EVT_SET_FOCUS, self.on_control_focus)
        
        # Auto-size columns
        self.grid.AutoSizeColumns()
        
        main_sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 10)
        
        # Status info
        self.info_label = wx.StaticText(self, label="")
        self._update_info_label()
        main_sizer.Add(self.info_label, 0, wx.ALL, 10)
        
        self.SetSizer(main_sizer)
        
    def GetName(self):
        """Return human-readable tab name."""
        return self.tab_name
        
    def _setup_columns(self):
        """Configure column types, editors, and renderers.
        
        Grid supports multiple cell types in same grid:
        - Text: Default editor (single-line text)
        - Number: Text with right alignment
        - Bool: Checkbox (Space/click to toggle)
        - Choice: Dropdown (F4 or click to open)
        - Date: Could use date picker editor
        - Custom: Can implement custom editors/renderers
        
        Each column gets GridCellAttr defining:
        - Editor: How cell is edited (text/bool/choice/custom)
        - Renderer: How cell is displayed (text/checkbox/custom)
        - Alignment: LEFT/CENTER/RIGHT for horizontal and vertical
        - Read-only: Prevents editing
        - Background/foreground colors: Visual styling
        
        Screen readers should announce:
        - Cell position (row, column)
        - Column header
        - Cell value
        - Cell type (edit, checkbox, dropdown)
        """
        # Column 0: ID (read-only, numeric)
        # Right-aligned for numbers, locked to prevent changes
        attr = wx.grid.GridCellAttr()
        attr.SetReadOnly(True)
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        self.grid.SetColAttr(0, attr)
        
        # Column 1: Employee (text)
        # Default text editor, wider column for names
        self.grid.SetColSize(1, 150)
        
        # Column 2: Department (text)
        # Default text editor
        self.grid.SetColSize(2, 120)
        
        # Column 3: Completed (checkbox)
        # Boolean editor: Space/click toggles, shows checkbox
        attr = wx.grid.GridCellAttr()
        attr.SetEditor(wx.grid.GridCellBoolEditor())
        attr.SetRenderer(wx.grid.GridCellBoolRenderer())
        attr.SetAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.grid.SetColAttr(3, attr)
        
        # Column 4: Priority (choice)
        attr = wx.grid.GridCellAttr()
        attr.SetEditor(wx.grid.GridCellChoiceEditor(PRIORITIES))
        self.grid.SetColAttr(4, attr)
        
        # Column 5: Hours (numeric)
        attr = wx.grid.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        self.grid.SetColAttr(5, attr)
        
        # Column 6: Cost (numeric)
        attr = wx.grid.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        self.grid.SetColAttr(6, attr)
        
        # Column 7: Due Date (text, could use date picker)
        self.grid.SetColSize(7, 100)
        
        # Column 8: Status (choice)
        attr = wx.grid.GridCellAttr()
        attr.SetEditor(wx.grid.GridCellChoiceEditor(STATUSES))
        self.grid.SetColAttr(8, attr)
        
        # Column 9: Notes (text)
        self.grid.SetColSize(9, 200)
        
    def _populate_grid(self):
        """Populate grid with generated data.
        
        Data format:
        - Row 0: Headers (already used for column labels)
        - Rows 1+: Data rows
        
        Special handling for checkbox column:
        - GridCellBoolRenderer expects "1" for checked
        - Empty string or "0" for unchecked
        - Cannot use True/False directly
        
        All other values converted to strings for display.
        Grid stores everything as strings internally.
        """
        # Start from row 1 (row 0 is headers in data array)
        for row_idx in range(1, len(self.grid_data)):
            row_data = self.grid_data[row_idx]
            for col_idx, value in enumerate(row_data):
                if col_idx == 3:  # Completed checkbox column
                    # Boolean renderer requires "1" or empty string
                    # Cannot use "True"/"False" strings
                    self.grid.SetCellValue(row_idx - 1, col_idx, "1" if value else "")
                else:
                    # All other values as strings
                    self.grid.SetCellValue(row_idx - 1, col_idx, str(value))
                    
    def _update_info_label(self):
        """Update status label with grid statistics.
        
        Counts checked checkboxes in Completed column (col 3).
        Demonstrates reading cell values programmatically.
        
        Note: Checkbox cells have value "1" when checked,
        empty string when unchecked.
        """
        completed_count = 0
        # Scan all rows in Completed column (index 3)
        for row in range(self.grid.GetNumberRows()):
            if self.grid.GetCellValue(row, 3) == "1":
                completed_count += 1
                
        self.info_label.SetLabel(
            f"Grid: {self.grid.GetNumberRows()} rows × {self.grid.GetNumberCols()} columns, "
            f"Completed tasks: {completed_count}"
        )
        
    def on_cell_select(self, event):
        """Handle cell selection."""
        row = event.GetRow()
        col = event.GetCol()
        
        col_name = self.grid.GetColLabelValue(col)
        value = self.grid.GetCellValue(row, col)
        
        # Special handling for checkbox column
        if col == 3:  # Completed column
            state = "Checked" if value == "1" else "Unchecked"
            value_display = state
        else:
            value_display = value if value else "(empty)"
            
        # Determine if cell is editable
        is_readonly = self.grid.IsReadOnly(row, col)
        readonly_text = ", Read-only" if is_readonly else ", Editable"
        
        self.main_frame.update_status_bar(
            f"Cell: {col_name}",
            f"Row {row + 1}, Column {col + 1}, Value: {value_display}{readonly_text}",
            "F2 or Enter to edit, Arrow keys to navigate, Tab for next cell"
        )
        
        event.Skip()
        
    def on_cell_changing(self, event):
                """Handle a cell value that is about to change.

                Contract:
                - Input: EVT_GRID_CELL_CHANGING event. Use `event.GetRow()`, `event.GetCol()`,
                    and `event.GetString()` to inspect the proposed value.
                - Output: Optionally call `event.Veto()` to reject the change, or
                    allow the event to continue by calling `event.Skip()`.

                Accessibility / keyboard notes:
                - Editors are typically opened with F2 or Enter. Validation here should not
                    block keyboard navigation; if vetoing, provide a brief status message
                    via `main_frame.update_status_bar` so screen-reader users receive feedback.

                Edge cases:
                - The checkbox column edits may provide string values like "1" or empty string.
                - Avoid raising exceptions during validation; gracefully veto and report.
                """
                row = event.GetRow()
                col = event.GetCol()
                new_value = event.GetString()

                # Could add validation here
                event.Skip()
        
    def on_cell_changed(self, event):
                """Handle a cell value that has changed.

                Responsibilities:
                - Persist the new value into the in-memory `self.grid_data` representation.
                - Update UI state (info label / status bar) so keyboard and screen-reader users
                    get immediate feedback.

                Contract:
                - Input: EVT_GRID_CELL_CHANGED event.
                - This method should not raise; if persisting fails, record the error and
                    update the UI so a human tester can investigate.

                Accessibility notes:
                - After a checkbox change (Space or click), call `_update_info_label` so
                    screen readers receive the updated counts and focus remains on the cell.
                - When non-editable cells are changed programmatically, call
                    `main_frame.update_status_bar` to announce the change.
                """
                row = event.GetRow()
                col = event.GetCol()

                # Update grid data
                if col == 3:  # Checkbox column
                        self.grid_data[row + 1][col] = (self.grid.GetCellValue(row, col) == "1")
                else:
                        self.grid_data[row + 1][col] = self.grid.GetCellValue(row, col)

                self._update_info_label()

                col_name = self.grid.GetColLabelValue(col)
                self.main_frame.update_status_bar(
                        f"Cell updated: {col_name}",
                        f"Row {row + 1}, Column {col + 1}",
                        ""
                )

                event.Skip()
        
    def on_control_focus(self, event):
                """Handle focus events routed to the grid control.

                Purpose:
                - When the grid gains focus (or focus moves within the grid), announce a
                    concise, contextual status via `main_frame.update_status_bar` describing
                    the focused cell and relevant keyboard hints.

                Accessibility behavior expected:
                - Screen readers should announce the cell role ("grid cell"), column
                    header, row/column position, and current cell value.
                - Keyboard users should immediately be able to navigate with arrow keys,
                    press Space to toggle checkboxes, and use F2/Enter to edit.

                Edge cases:
                - If the grid has no rows or columns, avoid out-of-range cursor calls.
                """
                row = self.grid.GetGridCursorRow()
                col = self.grid.GetGridCursorCol()

                if row >= 0 and col >= 0:
                        col_name = self.grid.GetColLabelValue(col)
                        value = self.grid.GetCellValue(row, col)

                        if col == 3:  # Checkbox column
                                state = "Checked" if value == "1" else "Unchecked"
                                value_display = state
                        else:
                                value_display = value if value else "(empty)"

                        self.main_frame.update_status_bar(
                                f"Grid: {self.grid.GetNumberRows()}×{self.grid.GetNumberCols()}",
                                f"Role: Grid cell, Row {row + 1}, Col {col + 1} ({col_name}): {value_display}",
                                "Arrow keys to navigate, F2 to edit, Space for checkboxes"
                        )
                event.Skip()
        
    # State management
    def save_state(self):
        """Save tab state for persistence between runs.

        Returns a JSON-serializable dict describing the tab state. Schema:
        {
            "grid_data": <original generated data structure, list of rows>,
            "cell_values": [[str,...], ...],  # actual string values from visible cells
            "cursor_row": int,
            "cursor_col": int
        }

        Notes / choices:
        - `grid_data` preserves the higher-level dataset used to populate the grid
          (useful for re-generating or diffing rows).
        - `cell_values` are saved as strings, since wx.Grid represents values as strings.
        - Consumers should validate the returned dict before writing to disk.

        Error modes:
        - If an exception occurs while reading cells (rare), the method should
          raise to the caller so state save can be retried or aborted safely.
        """
        # Save all cell values
        cell_values = []
        for row in range(self.grid.GetNumberRows()):
            row_values = []
            for col in range(self.grid.GetNumberCols()):
                value = self.grid.GetCellValue(row, col)
                row_values.append(value)
            cell_values.append(row_values)
            
        return {
            "grid_data": self.grid_data,
            "cell_values": cell_values,
            "cursor_row": self.grid.GetGridCursorRow(),
            "cursor_col": self.grid.GetGridCursorCol()
        }
        
    def load_state(self, state):
        """Load tab state previously returned by `save_state`.

        Expected input: the same schema described in `save_state`.

        Behavior:
        - Restore `self.grid_data` when present, then write `cell_values` into
          the visible grid cells when sizes match.
        - Restore the grid cursor and make the cell visible.

        Robustness:
        - This method performs bounds checks before writing into the grid.
        - If the saved state contains more rows/columns than the current grid,
          excess values are ignored. If fewer, missing cells are left unchanged.

        Accessibility:
        - After restoring state, `_update_info_label` is called so the information
          shown to screen readers reflects the restored state.
        """
        if "grid_data" in state:
            self.grid_data = state["grid_data"]

        if "cell_values" in state:
            for row, row_values in enumerate(state["cell_values"]):
                for col, value in enumerate(row_values):
                    if row < self.grid.GetNumberRows() and col < self.grid.GetNumberCols():
                        self.grid.SetCellValue(row, col, value)

        if "cursor_row" in state and "cursor_col" in state:
            row = state["cursor_row"]
            col = state["cursor_col"]
            if row >= 0 and col >= 0:
                if row < self.grid.GetNumberRows() and col < self.grid.GetNumberCols():
                    self.grid.SetGridCursor(row, col)
                    self.grid.MakeCellVisible(row, col)

        self._update_info_label()

    def reset_to_defaults(self):
        """Reset the tab to default generated test data.

        This restores `self.grid_data` with freshly generated data, repopulates
        the visible grid, updates computed labels, and sets the focus cursor
        to the first cell. Useful for returning to a known baseline during tests.

        Notes:
        - Callers should ensure that any unsaved state is persisted before calling
          this method.
        """
        self.grid_data = generate_grid_data(20, 10)
        self._populate_grid()
        self._update_info_label()
        if self.grid.GetNumberRows() > 0 and self.grid.GetNumberCols() > 0:
            self.grid.SetGridCursor(0, 0)
