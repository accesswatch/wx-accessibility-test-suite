# wxPython Accessibility Test Suite

Comprehensive test application for validating keyboard navigation and screen reader accessibility of wxPython controls according to WCAG 2.2 AA guidelines.

## Purpose

This application provides a complete testing environment for assessing how well screen readers (NVDA, JAWS, Microsoft Narrator) work with wxPython UI elements. Each control type is isolated on its own tab with realistic test data, enabling systematic verification of:

- Keyboard-only operation (no mouse required)
- Proper name/role/state exposure for assistive technologies
- WCAG 2.2 AA compliance
- Focus visibility and navigation order
- Screen reader announcement accuracy

## Requirements

- **Python**: 3.10 - 3.13
- **wxPython**: Latest version (4.2.x+)
- **Platform**: Windows (for NVDA/JAWS/Narrator testing)

## Installation

```powershell
# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install wxPython
pip install wxPython

# Run the application
python main.py
```

## Application Structure

```text
glen/
├── main.py                 # Main application entry point
├── test_data.py           # Sample data generators
├── state_manager.py       # State persistence manager
├── README.md              # This file
├── tabs/                  # Control test tabs
│   ├── __init__.py
│   ├── basic_controls_tab.py       # Buttons, TextCtrl, CheckBox, RadioBox, Choice, ListBox
│   ├── listctrl_tab.py             # ListCtrl with embedded checkboxes (100+ rows)
│   ├── listctrl_views_tab.py      # ListCtrl view modes (Report, List, Icon, Small Icon)
│   ├── treectrl_tab.py             # TreeCtrl with checkboxes and tri-state parents
│   ├── grid_tab.py                 # Grid with checkbox cells, mixed types
│   ├── advanced_controls_tab.py    # ToggleButton, Pickers, Spinners, Sliders, Containers
│   ├── media_controls_tab.py       # HyperlinkCtrl, SearchCtrl, Pickers, CalendarCtrl
│   ├── buttons_toolbar_tab.py      # BitmapButton, Toolbar, InfoBar, ScrollBar
│   ├── advanced_controls2_tab.py   # SpinCtrlDouble, AuiNotebook
│   ├── advanced_media_tab.py       # RichTextCtrl, PropertyGrid, DataViewCtrl, MediaCtrl
│   ├── advanced_controls3_tab.py   # HtmlWindow, GenericDirCtrl, StyledTextCtrl, Notebook
│   ├── advanced_controls4_tab.py   # SplitterWindow, Listbook, Choicebook, ActivityIndicator, EditableListBox, RearrangeCtrl
│   ├── advanced_controls5_tab.py   # Treebook, Toolbook, AnimationCtrl, CommandLinkButton, HtmlListBox, FileCtrl
│   └── validation_tab.py           # WCAG validation checklist and documentation
├── state/                 # Application state (auto-generated)
│   └── app_state.json    # Saved control states
└── logs/                  # Event logs (auto-generated)
    └── keyboard_events.json
```

## Features

### Tab Order & Progression

1. **Basic Controls Tab** – Foundational widgets (buttons, text inputs, choice controls).
2. **Buttons & Toolbar Tab** – Bitmap buttons, toolbars, infobars, and scrollbars that expand on core activation tests.
3. **ListCtrl with Checkboxes Tab** – Large data list with checkbox column for bulk selection scenarios.
4. **ListCtrl View Modes Tab** – Same dataset rendered in Report/List/Icon/Small Icon modes to verify view-specific semantics.
5. **TreeCtrl with Checkboxes Tab** – Hierarchical navigation with tri-state parents and checkbox propagation.
6. **Grid with Checkbox Cells Tab** – Spreadsheet-style editing across mixed cell editors.
7. **Media & Link Controls Tab** – Hyperlinks, search, pickers, and calendar/time controls.
8. **Advanced Media & Data Tab** – RichTextCtrl, PropertyGrid, DataViewCtrl, and MediaCtrl.
9. **Advanced Controls Tab** – Toggle buttons, sliders, gauges, and collapsible containers.
10. **Advanced Controls 2 Tab** – SpinCtrlDouble plus AuiNotebook drag-reorder testing.
11. **Advanced Controls 3 Tab** – HtmlWindow, GenericDirCtrl, StyledTextCtrl, and embedded Notebook.
12. **Advanced Controls 4 Tab** – SplitterWindow, alternative notebooks, ActivityIndicator, and specialized lists.
13. **Advanced Controls 5 Tab** – Treebook, Toolbook, AnimationCtrl, CommandLinkButton, HtmlListBox, and FileCtrl.
14. **Validation & Documentation Tab** – WCAG checklist, documentation links, and workflow guidance.

### 1. Basic Controls Tab

Tests fundamental input controls:

- **Buttons**: Standard, default, disabled (click counter)
- **TextCtrl**: Single-line, multi-line, password, read-only
- **CheckBox**: 2-state, 3-state (checked/unchecked/indeterminate)
- **RadioBox/RadioButton**: Groups with mutual exclusivity
- **Choice/ComboBox**: Dropdown selection (20+ items)
- **ListBox**: Single/multi-select (50 items)
- **CheckListBox**: List with integrated checkboxes

### 2. ListCtrl with Checkboxes Tab

Tests multi-column list with checkbox column:

- 100+ task rows with sortable columns (ID, Task, Assignee, Priority, Status, Due Date)
- Checkbox column with Space key toggling
- Multi-select support with Ctrl+Space
- Column header sorting demonstration
- Row selection and activation

### 3. TreeCtrl with Checkboxes Tab

Tests hierarchical tree with checkboxes:

- 3-level file/folder hierarchy (50+ nodes)
- Per-node checkbox states
- **Tri-state parent nodes** (checked/unchecked/mixed based on children)
- Expand/collapse with arrow keys
- Space key checkbox toggling
- Parent-child state propagation

### 4. Grid with Checkbox Cells Tab

Tests spreadsheet-like grid:

- 20 rows × 10 columns
- **Mixed cell types**:
  - Read-only ID column
  - Text entry (Employee, Department, Notes)
  - **Checkbox cells** (Completed column) - toggleable with Space
  - Choice cells (Priority, Status) - dropdown editors
  - Numeric cells (Hours, Cost)
  - Date cells
- F2 or Enter to edit, Arrow keys to navigate
- Cell-by-cell state persistence

### 5. Advanced Controls Tab

Tests Tier 2 controls:

- **ToggleButton**: Press/release states (Bold, Italic, Underline)
- **Pickers**: Date, Color, File (with keyboard dialog access)
- **SpinCtrl**: Integer value with arrow key adjustment
- **Slider**: Value adjustment with arrows and Page Up/Down
- **Gauge**: Progress bar (adjustable with buttons)
- **CollapsiblePane**: Expandable section (Space to toggle)
- **StaticBox**: Grouped controls with accessible labels

### 6. Media & Link Controls Tab

Tests media, hyperlink, and specialized pickers:

- **HyperlinkCtrl**: External links with Enter activation (3 sample links)
- **SearchCtrl**: Search box with cancel button, optional menu filter
- **DirPickerCtrl**: Directory/folder browser dialog
- **FontPickerCtrl**: Font selection dialog with live preview
- **TimePickerCtrl**: Time selection with arrow key adjustment
- **CalendarCtrl**: Full calendar view with arrow key navigation (Page Up/Down for months)

### 7. Buttons & Toolbar Tab

Tests button variants and toolbar controls:

- **BitmapButton**: Buttons with icons (Save, Open, Print, Help)
- **Toolbar**: Full toolbar with tools, separators, toggle tools (11 tools)
- **InfoBar**: Notification bars (Information, Warning, Error types)
- **ScrollBar**: Horizontal and vertical scrollbar controls

### 8. Advanced Controls 2 Tab

Tests specialized advanced controls:

- **SpinCtrlDouble**: Floating-point spinners (Price, Percentage, Temperature)
- **AuiNotebook**: Advanced tabbed interface with drag-to-reorder, closeable tabs

### 9. Advanced Media & Data Tab

Tests specialized media and data controls:

- **RichTextCtrl**: Formatted text editor with bold, italic, colors (Ctrl+B/I/U)
- **PropertyGrid**: Property sheet editor with categories, bool/string/int/color/font/enum properties
- **DataViewCtrl**: High-performance virtual list with 50 rows, sorting, multi-select
- **MediaCtrl**: Audio/video player with load/play/pause/stop/volume controls

### 10. Advanced Controls 3 Tab

Tests HTML rendering, directory navigation, code editing, and nested tabbing:

- **HtmlWindow**: HTML content rendering with keyboard link navigation
  - Tab key navigates between hyperlinks
  - Enter/Space to activate links
  - Screen reader announces HTML semantics (headings, lists, tables, links)
  - Demonstrates accessible HTML structure
- **GenericDirCtrl**: Directory tree browser
  - Arrow keys to navigate folder hierarchy
  - Right arrow to expand, left to collapse
  - Type-ahead search for quick navigation
  - Screen reader distinguishes folders from files
  - Starts at user's home directory
- **StyledTextCtrl**: Code editor with syntax highlighting
  - Python syntax highlighting (keywords, strings, comments, functions)
  - Line numbers in margin
  - Code folding support
  - Standard editing shortcuts (Ctrl+C/V/X/Z/Y)
  - Home/End for line navigation, Ctrl+Home/End for document
  - Cursor position announced (line and column)
- **Embedded wx.Notebook**: Nested tabbed interface
  - Tests nested tab navigation (Ctrl+Tab to switch tabs)
  - Tab key to navigate controls within nested tabs
  - Verifies focus management between parent and child tab controls
  - Three sample tabs: Text Controls, Buttons, List
  - Screen reader announces current nested tab

### 11. Advanced Controls 4 Tab

Tests container and specialized controls:

- **SplitterWindow**: Resizable split panels with nested splitters (3 instances - vertical and horizontal)
- **Listbook**: List-based sidebar page navigation (4 pages)
- **Choicebook**: Dropdown-based page navigation (4 pages)
- **ActivityIndicator**: Animated loading spinner with start/stop controls
- **EditableListBox**: List with New/Edit/Delete buttons for item management
- **RearrangeCtrl**: List with checkboxes and Move Up/Down buttons for reordering

### 12. Advanced Controls 5 Tab

Tests final missing controls for complete coverage:

- **Treebook**: Hierarchical tree-based page navigation (7 pages in chapters with subsections)
- **Toolbook**: Toolbar icon-based page navigation (4 pages with icons)
- **AnimationCtrl**: Animated GIF playback control with play/stop buttons
- **CommandLinkButton**: Windows Vista+ style buttons with main text and descriptive notes (3 instances)
- **HtmlListBox**: List box with HTML-formatted items (10 items with bold, italic, colors)
- **FileCtrl**: Embedded file system browser with filtering and multi-select support

### 13. Validation & Documentation Tab

Testing checklist and reference:

- **WCAG 2.2 AA criteria checklist** (19 criteria)
  - Grouped by principle (Perceivable, Operable, Understandable, Robust)
  - Critical criteria marked (2.1.1 Keyboard, 4.1.2 Name/Role/Value, etc.)
  - New WCAG 2.2 criteria highlighted (2.4.11, 2.5.7, 2.5.8, 3.3.7, 3.3.8)
- Per-criterion notes field for recording test results
- Tester name and timestamp tracking
- **Export validation report** to text file
- **Keyboard shortcuts reference** with expected screen reader announcements
- Testing procedure guide

## Test Data

All controls are pre-populated with realistic test data:

- **People**: 100+ generated names with emails, phones, addresses, departments
- **Tasks**: 100+ tasks with assignees, priorities, statuses, due dates, mixed checkbox states
- **File Tree**: 3-level hierarchy with Documents/Pictures/Downloads folders, 40+ files
- **Grid Data**: 20 rows of employee/task data with mixed types and checkbox states
- **Choices**: 20+ colors, 50 countries, departments, priorities, statuses

### Data Characteristics

- **Mixed checkbox states**: Pre-set combinations of checked/unchecked for testing
- **Tri-state tree parents**: Automatically calculated based on children
- **Realistic variety**: Sufficient diversity to test sorting, filtering, scrolling

## State Persistence

**All application state is automatically saved and restored:**

### Saved State Includes

- Window size, position, maximized state
- Active tab selection
- All text entry values (including multi-line and password fields)
- All checkbox states (including 3-state checkboxes)
- Radio button selections
- Dropdown/choice selections
- List selections (single and multi-select)
- **ListCtrl**: All 100+ row checkbox states, selected row, sort order
- **TreeCtrl**: All node checkbox states (including tri-state), expansion states, selected node
- **Grid**: All 200 cell values including checkbox cells, cursor position
- Toggle button states
- Picker values (dates, colors, file paths)
- Spin/slider positions
- Gauge progress values
- Collapsible pane expansion state
- **HtmlWindow**: Current HTML content
- **GenericDirCtrl**: Selected directory path
- **StyledTextCtrl**: Code editor text and cursor position
- **Embedded Notebook**: Selected nested tab and control values
- **Validation progress**: Tester name, checked criteria, notes per criterion

### State Files

- **Location**: `state/app_state.json`
- **Format**: Human-readable JSON
- **Auto-save**: On application close
- **Auto-load**: On application startup
- **Manual save**: File > Save State (Ctrl+S)
- **Manual load**: File > Load State (Ctrl+O)
- **Reset**: File > Reset to Defaults (Ctrl+R)

## Keyboard Navigation

### Universal Shortcuts

- **Tab / Shift+Tab**: Navigate forward/backward through controls and control groups
- **Arrow Keys**: Navigate within complex controls (lists, trees, grids, menus, radio groups)
- **Space**: Activate buttons, toggle checkboxes/toggles, select in lists
  - ✅ **Works for**: Checkboxes (2-state, 3-state), ToggleButtons, Buttons
  - ⚠️ **Radio buttons**: Space may not work reliably - use Arrow keys instead
- **Enter**: Activate default button, confirm selections, activate focused button
- **Escape**: Cancel operations, close dialogs
- **Context Menu Key** (or Shift+F10): Open context menu

### Control-Specific Shortcuts

#### Radio Buttons (RadioBox, RadioButton groups)

- **Arrow Up/Down** (or Left/Right): Navigate AND select within radio group
- **Tab**: Move to radio group (focuses first/selected button), or Tab out to next control
- ⚠️ **You are "locked" in the group**: Must use Tab to exit (arrows won't leave group)
- **Space**: May activate selected radio, but Arrow keys are more reliable
- **Note**: Only the first radio button (or currently selected one) is a Tab stop

#### Text Controls

- **Ctrl+A**: Select all
- **Ctrl+C/X/V**: Copy/Cut/Paste
- **Home/End**: Line boundaries
- **Ctrl+Home/End**: Document boundaries

#### Lists (ListBox, CheckListBox, ListCtrl)

- **Arrow Up/Down**: Navigate items
- **Space**: Toggle selection (multi-select) or checkbox
- **Ctrl+Space**: Toggle item without changing other selections
- **Shift+Arrows**: Range selection
- **Ctrl+A**: Select all
- **Page Up/Down**: Scroll by page
- **Type letters**: Jump to matching item

#### Trees (TreeCtrl)

- **Arrow Right**: Expand node / Move to first child
- **Arrow Left**: Collapse node / Move to parent
- **Space**: Toggle checkbox
- **\* (numpad)**: Expand all children
- **Backspace**: Move to parent

#### Grids (wx.grid.Grid)

- **Arrow Keys**: Navigate cells
- **F2 or Enter**: Begin editing cell
- **Space**: Toggle checkbox cells
- **Tab**: Next cell (or exit grid)
- **Escape**: Cancel editing
- **Ctrl+Home/End**: First/Last cell

#### Menus

- **Alt or F10**: Activate menu bar
- **Alt+Letter**: Mnemonic access
- **Arrow Keys**: Navigate menus
- **Enter**: Activate item
- **Escape**: Close menu

#### HtmlWindow

- **Tab**: Navigate between hyperlinks
- **Shift+Tab**: Navigate backwards through links
- **Enter or Space**: Activate focused link
- **Arrow Keys**: Scroll content (in some implementations)

#### GenericDirCtrl (Directory Tree)

- **Arrow Up/Down**: Navigate folders/files
- **Arrow Right**: Expand folder / Move to first child
- **Arrow Left**: Collapse folder / Move to parent
- **\* (numpad)**: Expand all children
- **Type letters**: Jump to matching folder/file name

#### StyledTextCtrl (Code Editor)

- **Standard editing**: Ctrl+C/X/V/Z/Y (Copy/Cut/Paste/Undo/Redo)
- **Home/End**: Line start/end
- **Ctrl+Home/End**: Document start/end
- **Arrow Keys**: Navigate by character
- **Ctrl+Arrow**: Navigate by word
- **Page Up/Down**: Scroll by page

#### Embedded Notebook

- **Ctrl+Tab**: Switch to next nested tab
- **Ctrl+Shift+Tab**: Switch to previous nested tab
- **Tab**: Navigate controls within active nested tab
- **Shift+Tab**: Navigate backwards within nested tab

## Screen Reader Testing

### Expected Announcements

For each control, screen readers should announce:

1. **Role**: Control type (button, checkbox, list, tree, grid, etc.)
2. **Name**: Label or accessible name
3. **State**: Current state (checked, selected, expanded, pressed, etc.)
4. **Value**: Current value (text, selection, position)
5. **Position**: Location in lists/trees ("Item 5 of 20")
6. **Level**: Hierarchy depth (tree nodes)

### Examples

- **Button**: "Save Button"
- **Checkbox**: "Enable notifications Checkbox Checked"
- **Radio Button**: "High Radio Button Checked, 3 of 4" or "High, 3 of 4"
  - Note: Arrow keys should announce "High Radio Button Checked" when moving to it
- **ListCtrl Row**: "Row 5 of 100, Task column: Review documentation, Checkbox Unchecked"
- **TreeCtrl Node**: "Documents Folder, Level 1, Expanded, Checkbox Mixed (2 of 5 checked)"
- **Grid Cell**: "Row 3, Column 4 (Completed), Checkbox Checked, Editable"
- **HTML Link**: "Link, wxPython Official Site, https://www.wxpython.org"
- **Directory Tree**: "Folder, Documents, Collapsed, Level 2"
- **Code Editor**: "Edit, Line 15, Column 8, def calculate_total"
- **Nested Tab**: "Text Controls Tab, 1 of 3"

### Testing with NVDA

1. Start NVDA (Ctrl+Alt+N)
2. Tab through controls and verify announcements
3. Use NVDA+Tab to read focus
4. Use arrow keys in browse mode to verify structure
5. Test checkbox toggling (Space) - should announce new state
6. Test list/tree/grid navigation - should announce position and state

### Testing with JAWS

1. Start JAWS
2. Tab through controls
3. Use Insert+Tab for control information
4. Test complex controls (lists, trees, grids) with arrow keys
5. Verify table semantics in ListCtrl and Grid (column headers)

### Testing with Narrator

1. Start Narrator (Ctrl+Win+Enter)
2. Tab through controls
3. Use Caps Lock+Enter for more details
4. Test Scan Mode (Caps Lock+Space) for structure navigation
5. Verify announcements match expected output

## WCAG 2.2 AA Validation

The application tests compliance with 19 key success criteria:

### Critical Criteria (Must Pass)

- **2.1.1 Keyboard** (Level A): All functionality available via keyboard
- **2.1.2 No Keyboard Trap** (Level A): Can Tab out of every control
- **2.4.3 Focus Order** (Level A): Logical tab sequence
- **2.4.7 Focus Visible** (Level AA): Focus indicator clearly visible
- **3.2.1 On Focus** (Level A): No automatic context changes on focus
- **3.2.2 On Input** (Level A): No automatic submissions
- **4.1.2 Name, Role, Value** (Level A): Screen reader announces correctly

### New in WCAG 2.2

- **2.4.11 Focus Not Obscured (Minimum)** (Level AA): Focus scrolled into view
- **2.5.7 Dragging Movements** (Level AA): Keyboard alternatives to dragging
- **2.5.8 Target Size (Minimum)** (Level AA): 24×24 pixel minimum targets
- **3.3.7 Redundant Entry** (Level A): Auto-fill/copy previous entries
- **3.3.8 Accessible Authentication (Minimum)** (Level AA): No cognitive function tests

### Validation Workflow

1. Open **Validation & Documentation** tab
2. Enter your name in "Tester Name" field
3. Work through each criterion systematically
4. Test relevant controls for each criterion
5. Check the criterion when validated
6. Click "Notes" button to record findings
7. Use **Export Validation Report** to generate timestamped report

## Testing Procedure

### 1. Keyboard Navigation Test

- [ ] Tab through all controls in each tab
- [ ] Verify no keyboard traps (can always Tab out, including from radio groups)
- [ ] Test radio button groups: Tab into group, use arrows to select, Tab out
- [ ] Check focus indicator is visible on all controls
- [ ] Confirm focus order matches visual layout

### 2. Control Operation Test

- [ ] Operate all buttons with Space/Enter
- [ ] Toggle all checkboxes with Space (2-state and 3-state)
- [ ] Navigate radio button groups with Arrow keys (Space may not work)
- [ ] Verify Arrow keys select radio buttons (not just navigate)
- [ ] Navigate all lists with arrows
- [ ] Edit all text fields
- [ ] Open all dropdowns with Alt+Down
- [ ] Expand/collapse tree nodes with arrows
- [ ] Navigate grid cells with arrows
- [ ] Edit grid cells with F2

### 3. Checkbox-Specific Tests

#### ListCtrl

- [ ] Navigate rows with Arrow Up/Down
- [ ] Toggle checkbox with Space
- [ ] Verify checkbox state announced
- [ ] Test "Check All" / "Uncheck All" buttons
- [ ] Verify checkbox states persist through navigation

#### TreeCtrl

- [ ] Toggle file/folder checkboxes with Space
- [ ] Verify parent shows tri-state when children mixed
- [ ] Check parent checkbox - should check all children
- [ ] Uncheck one child - parent should show mixed state
- [ ] Verify expansion state doesn't affect checkbox state

#### Grid

- [ ] Navigate to checkbox column (Column 3: "Completed")
- [ ] Toggle checkbox cell with Space
- [ ] Navigate away and back - state should persist
- [ ] Edit other cells (F2) to verify mixed cell types work
- [ ] Verify checkbox cells have proper role/state announced

### 4. Screen Reader Test

- [ ] Start NVDA/JAWS/Narrator
- [ ] Verify role announced for each control type
- [ ] Check label/name is read correctly
- [ ] Confirm state is announced (checked, selected, etc.)
- [ ] Test position announcements in lists/trees ("Item 5 of 100")
- [ ] Verify tri-state tree parent announcements ("Mixed, 2 of 5 checked")
- [ ] Test grid cell announcements (row, column, value, state)
- [ ] Verify state change announcements (toggle checkbox)

### 5. State Persistence Test

- [ ] Modify various controls (text, checkboxes, selections)
- [ ] Toggle several checkboxes in ListCtrl, TreeCtrl, Grid
- [ ] Close application (auto-saves)
- [ ] Reopen application
- [ ] Verify all changes persisted correctly
- [ ] Test manual Save State (Ctrl+S) and Load State (Ctrl+O)

## Troubleshooting

### wxPython Installation Issues

```powershell
# If pip install wxPython fails, try:
pip install --upgrade pip setuptools wheel
pip install wxPython

# Or use pre-built wheel from wxPython.org
```

### State File Corruption

```powershell
# Delete state file to reset:
Remove-Item state\app_state.json

# Application will create new state file with defaults
```

### Screen Reader Not Announcing

- Verify screen reader is running and active
- Check Windows Settings > Accessibility > Narrator/Screen Reader
- Ensure focus is in the application window
- Try restarting screen reader
- Some controls may require specific wxPython versions for proper MSAA/UIA exposure

## Development Notes

### Adding New Tabs

1. Create new tab class in `tabs/` inheriting from `wx.Panel` and `TabStateHelper`
2. Implement `GetName()`, `save_state()`, `load_state()`, `reset_to_defaults()`
3. Add imports to `tabs/__init__.py`
4. Instantiate in `main.py` `_create_notebook()` method
5. Add to `self.tabs` list

### Adding Test Data

1. Add generators to `test_data.py`
2. Use in tab `__init__()` or `reset_to_defaults()`
3. Ensure data is serializable (JSON-compatible types)

### State Management

- All state must be JSON-serializable
- Complex objects (wx.DateTime, wx.Colour) must be converted to strings
- Tree/Grid structures should preserve enough info to rebuild UI state
- Test save/load cycle to verify serialization works

## License

This is a testing and demonstration application for accessibility validation.

## Contact

For issues or questions about wxPython accessibility, refer to:

- [wxPython documentation](https://docs.wxpython.org/)
- [wxPython forums](https://discuss.wxpython.org/)
- [NVDA documentation](https://www.nvaccess.org/files/nvda/documentation/userGuide.html)
- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)

## Version History

- **1.2** (2025-10-30): Complete control coverage
  - Added Advanced Controls 3 tab: HtmlWindow, GenericDirCtrl, StyledTextCtrl, embedded Notebook
  - Added Advanced Controls 4 tab: SplitterWindow, Listbook, Choicebook, ActivityIndicator, EditableListBox, RearrangeCtrl
  - Added Advanced Controls 5 tab: Treebook, Toolbook, AnimationCtrl, CommandLinkButton, HtmlListBox, FileCtrl
  - 13 tabs with 70+ control types (100% coverage of common wxPython controls)
  - All controls fully keyboard accessible with state persistence

- **1.1** (2025-10-30): Extended control coverage
  - Added Media & Link Controls tab: HyperlinkCtrl, SearchCtrl, pickers, CalendarCtrl
  - Added Buttons & Toolbar tab: BitmapButton, Toolbar, InfoBar, ScrollBar
  - Added Advanced Controls 2 tab: SpinCtrlDouble, AuiNotebook
  - Added Advanced Media & Data tab: RichTextCtrl, PropertyGrid, DataViewCtrl, MediaCtrl
  - Fixed Grid keyboard navigation (EnableEditing)
  - Fixed toolbar state save (IsToggled vs IsToggle)
  - Fixed PropertyGrid iteration (GetIterator vs GetPropertyCount)
  - 10 tabs with 64+ control types

- **1.0** (2025-10-29): Initial release
  - 11 tabs with 45+ control types
  - Embedded checkboxes in ListCtrl, TreeCtrl, Grid
  - Tri-state tree parent nodes
  - Full state persistence
  - WCAG 2.2 AA validation checklist
  - Comprehensive keyboard navigation
  - Screen reader testing documentation
