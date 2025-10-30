"""
Test Data Fixtures
==================
Sample data for populating all controls in the accessibility test suite.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


# Person names for list/grid data
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Andrew", "Emily", "Paul", "Donna", "Joshua", "Michelle",
    "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
    "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Angela", "Eric", "Shirley", "Jonathan", "Anna", "Stephen", "Brenda",
    "Larry", "Pamela", "Justin", "Emma", "Scott", "Nicole", "Brandon", "Helen",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Raymond", "Christine", "Gregory", "Debra",
    "Frank", "Rachel", "Alexander", "Carolyn", "Patrick", "Janet", "Raymond", "Catherine",
    "Jack", "Maria", "Dennis", "Heather", "Jerry", "Diane", "Tyler", "Ruth"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers"
]

CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle",
    "Denver", "Washington", "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City",
    "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore", "Milwaukee", "Albuquerque",
    "Tucson", "Fresno", "Mesa", "Sacramento", "Atlanta", "Kansas City", "Colorado Springs",
    "Omaha", "Raleigh", "Miami", "Long Beach", "Virginia Beach", "Oakland", "Minneapolis",
    "Tulsa", "Tampa", "Arlington", "New Orleans"
]

STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

DEPARTMENTS = [
    "Engineering", "Sales", "Marketing", "Human Resources", "Finance",
    "Operations", "Customer Support", "Legal", "IT", "Research & Development",
    "Product Management", "Quality Assurance", "Administration", "Procurement"
]

TASK_NAMES = [
    "Review documentation", "Update requirements", "Fix critical bug", "Implement feature",
    "Code review", "Write unit tests", "Deploy to staging", "Security audit",
    "Performance optimization", "Database migration", "UI/UX improvements", "API integration",
    "Accessibility testing", "Localization updates", "Backup verification", "Server maintenance",
    "User training", "Documentation update", "Sprint planning", "Retrospective meeting",
    "Architecture design", "Load testing", "Regression testing", "Bug triage",
    "Release preparation", "Customer demo", "Data analysis", "Compliance review"
]

PRIORITIES = ["Low", "Medium", "High", "Critical"]

STATUSES = ["Not Started", "In Progress", "Blocked", "Completed", "Cancelled"]

FILE_EXTENSIONS = [".txt", ".doc", ".pdf", ".xls", ".ppt", ".jpg", ".png", ".zip", ".xml", ".json"]


def generate_person_name() -> str:
    """Generate a random full name.
    
    Uses realistic US names for natural-sounding test data.
    Names are repeated across multiple calls to simulate real-world
    scenarios where different people share common names.
    """
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def generate_email(name: str) -> str:
    """Generate email from name."""
    parts = name.lower().split()
    return f"{parts[0]}.{parts[1]}@example.com"


def generate_phone() -> str:
    """Generate a random phone number."""
    return f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"


def generate_address() -> str:
    """Generate a random address.
    
    Creates US-format addresses with realistic components:
    - Street numbers (100-9999)
    - Common street names
    - Real US cities and states
    - 5-digit ZIP codes
    
    Format matches typical address parsing expectations.
    """
    street_num = random.randint(100, 9999)
    street_names = ["Main St", "Oak Ave", "Maple Dr", "Park Ln", "Cedar Rd", "Pine St", "Elm Ave"]
    city = random.choice(CITIES)
    state = random.choice(STATES)
    zip_code = random.randint(10000, 99999)
    return f"{street_num} {random.choice(street_names)}, {city}, {state} {zip_code}"


def generate_date(days_offset: int = 0) -> datetime:
    """Generate a date relative to today.
    
    Used for testing date controls and due date calculations.
    Offset allows creating past/future dates for realistic scenarios:
    - Negative offset: past dates (completed tasks, historical data)
    - Zero offset: today (current tasks)
    - Positive offset: future dates (upcoming deadlines)
    """
    return datetime.now() + timedelta(days=days_offset)


def generate_people_list(count: int = 100) -> List[Dict[str, Any]]:
    """Generate list of people with details for ListCtrl.
    
    Creates realistic employee/contact records with:
    - Sequential IDs for easy reference
    - Names, emails derived from names
    - Phone numbers, addresses, departments
    
    Used to populate ListCtrl with enough data to test:
    - Scrolling behavior
    - Search/filter functionality
    - Sorting by different columns
    - Selection of multiple items
    """
    people = []
    for i in range(count):
        name = generate_person_name()
        people.append({
            "id": i + 1,
            "name": name,
            "email": generate_email(name),
            "phone": generate_phone(),
            "department": random.choice(DEPARTMENTS),
            "checked": random.choice([True, False]),
            "active": random.choice([True, False])
        })
    return people


def generate_task_list(count: int = 100) -> List[Dict[str, Any]]:
    """Generate list of tasks for ListCtrl.
    
    Creates project management-style task records with:
    - Task descriptions (from realistic project activities)
    - Assignees (randomly assigned team members)
    - Priority levels (High/Medium/Low)
    - Status tracking (Not Started/In Progress/Completed/Blocked)
    - Due dates (mix of past, current, and future)
    - Checkbox states (random for testing tri-state scenarios)
    
    Mixed checkbox/completed states test:
    - Sorting with checkbox column
    - Filtering completed vs. active tasks
    - Bulk operations (check all incomplete, etc.)
    """
    tasks = []
    for i in range(count):
        tasks.append({
            "id": i + 1,  # Sequential ID for tracking
            "task": random.choice(TASK_NAMES),  # Realistic task description
            "assignee": generate_person_name(),  # Team member
            "priority": random.choice(PRIORITIES),  # High/Medium/Low
            "status": random.choice(STATUSES),  # Workflow state
            "due_date": generate_date(random.randint(-30, 90)).strftime("%Y-%m-%d"),  # ±3 months
            "checked": random.choice([True, False]),  # Checkbox state
            "completed": random.choice([True, False])  # Completion flag
        })
    return tasks


def generate_file_tree() -> Dict[str, Any]:
    """Generate hierarchical file/folder structure for TreeCtrl.
    
    Creates 3-level tree with folders and files:
    - Level 1: Root container
    - Level 2: Main folders (Documents, Pictures, Downloads)
    - Level 3: Files within folders
    
    Structure tests:
    - Tri-state parent checkboxes (mixed when children partially checked)
    - Expand/collapse operations
    - Parent-child selection propagation
    - Tree navigation (arrow keys, Home/End)
    
    Each node has:
    - name: Display text
    - type: 'folder' or 'file' (affects icon/behavior)
    - checked: Boolean checkbox state
    - children: Nested nodes (folders only)
    """
    return {
        "name": "Root",
        "type": "folder",
        "checked": False,  # Parent tri-state calculated dynamically
        "children": [
            {
                "name": "Documents",
                "type": "folder",
                "checked": False,
                "children": [
                    {"name": "Resume.pdf", "type": "file", "checked": True},
                    {"name": "CoverLetter.doc", "type": "file", "checked": True},
                    {
                        "name": "Projects",
                        "type": "folder",
                        "checked": False,
                        "children": [
                            {"name": "ProjectA.doc", "type": "file", "checked": False},
                            {"name": "ProjectB.doc", "type": "file", "checked": True},
                            {"name": "Budget.xls", "type": "file", "checked": False}
                        ]
                    },
                    {"name": "Notes.txt", "type": "file", "checked": False}
                ]
            },
            {
                "name": "Pictures",
                "type": "folder",
                "checked": False,
                "children": [
                    {
                        "name": "Vacation 2024",
                        "type": "folder",
                        "checked": True,
                        "children": [
                            {"name": "Beach.jpg", "type": "file", "checked": True},
                            {"name": "Sunset.jpg", "type": "file", "checked": True},
                            {"name": "Family.jpg", "type": "file", "checked": True}
                        ]
                    },
                    {"name": "Profile.png", "type": "file", "checked": False},
                    {"name": "Screenshot.png", "type": "file", "checked": False}
                ]
            },
            {
                "name": "Downloads",
                "type": "folder",
                "checked": False,
                "children": [
                    {"name": "Setup.exe", "type": "file", "checked": False},
                    {"name": "Documentation.pdf", "type": "file", "checked": True},
                    {"name": "Archive.zip", "type": "file", "checked": False}
                ]
            },
            {
                "name": "Music",
                "type": "folder",
                "checked": False,
                "children": [
                    {"name": "Playlist1.m3u", "type": "file", "checked": False},
                    {"name": "Song1.mp3", "type": "file", "checked": False},
                    {"name": "Song2.mp3", "type": "file", "checked": True}
                ]
            },
            {
                "name": "Videos",
                "type": "folder",
                "checked": False,
                "children": [
                    {"name": "Tutorial.mp4", "type": "file", "checked": True},
                    {"name": "Presentation.mp4", "type": "file", "checked": False}
                ]
            }
        ]
    }


def generate_grid_data(rows: int = 20, cols: int = 10) -> List[List[Any]]:
    """Generate spreadsheet-like data for Grid control."""
    headers = [
        "ID", "Employee", "Department", "Completed", "Priority", 
        "Hours", "Cost", "Due Date", "Status", "Notes"
    ]
    
    data = [headers]
    
    for i in range(rows):
        row = [
            i + 1,  # ID
            generate_person_name(),  # Employee
            random.choice(DEPARTMENTS),  # Department
            random.choice([True, False]),  # Completed (checkbox)
            random.choice(PRIORITIES),  # Priority (choice)
            round(random.uniform(0.5, 40.0), 1),  # Hours
            round(random.uniform(100, 10000), 2),  # Cost
            generate_date(random.randint(-30, 90)).strftime("%Y-%m-%d"),  # Due Date
            random.choice(STATUSES),  # Status (choice)
            f"Note for task {i + 1}"  # Notes
        ]
        data.append(row)
    
    return data


def get_color_names() -> List[str]:
    """Get list of color names for combo boxes."""
    return [
        "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Pink", "Brown",
        "Black", "White", "Gray", "Cyan", "Magenta", "Lime", "Navy", "Teal",
        "Olive", "Maroon", "Aqua", "Fuchsia", "Silver", "Gold", "Indigo", "Violet"
    ]


def get_country_names() -> List[str]:
    """Get list of country names for list boxes."""
    return [
        "United States", "Canada", "Mexico", "United Kingdom", "France", "Germany",
        "Italy", "Spain", "Portugal", "Netherlands", "Belgium", "Switzerland",
        "Austria", "Sweden", "Norway", "Denmark", "Finland", "Poland", "Czech Republic",
        "Hungary", "Greece", "Turkey", "Russia", "China", "Japan", "South Korea",
        "India", "Australia", "New Zealand", "Brazil", "Argentina", "Chile",
        "Colombia", "Peru", "Egypt", "South Africa", "Nigeria", "Kenya",
        "Saudi Arabia", "United Arab Emirates", "Israel", "Singapore", "Thailand",
        "Vietnam", "Philippines", "Indonesia", "Malaysia", "Pakistan", "Bangladesh"
    ]


def get_sample_text() -> str:
    """Get sample text for text controls."""
    return (
        "This is sample text content for testing text controls. "
        "It demonstrates multi-line text entry, word wrapping, "
        "and screen reader navigation through text content. "
        "Users can navigate by character, word, or line using arrow keys."
    )


def get_sample_password() -> str:
    """Get sample password for password controls."""
    return "SecureP@ssw0rd123"


# Default checkbox states for various scenarios
DEFAULT_CHECKBOX_STATES = {
    "all_checked": True,
    "all_unchecked": False,
    "mixed": None,  # For random/mixed states
}


# WCAG 2.2 AA Criteria for validation checklist
WCAG_CRITERIA = [
    {
        "id": "1.1.1",
        "level": "A",
        "name": "Non-text Content",
        "description": "All non-text content has text alternatives"
    },
    {
        "id": "1.3.1",
        "level": "A",
        "name": "Info and Relationships",
        "description": "Information, structure, and relationships can be programmatically determined"
    },
    {
        "id": "1.3.2",
        "level": "A",
        "name": "Meaningful Sequence",
        "description": "Correct reading sequence can be programmatically determined"
    },
    {
        "id": "1.4.1",
        "level": "A",
        "name": "Use of Color",
        "description": "Color is not used as the only visual means of conveying information"
    },
    {
        "id": "1.4.3",
        "level": "AA",
        "name": "Contrast (Minimum)",
        "description": "Text has contrast ratio of at least 4.5:1"
    },
    {
        "id": "1.4.11",
        "level": "AA",
        "name": "Non-text Contrast",
        "description": "UI components have contrast ratio of at least 3:1"
    },
    {
        "id": "2.1.1",
        "level": "A",
        "name": "Keyboard",
        "description": "All functionality available from keyboard",
        "critical": True
    },
    {
        "id": "2.1.2",
        "level": "A",
        "name": "No Keyboard Trap",
        "description": "Keyboard focus can be moved away from component",
        "critical": True
    },
    {
        "id": "2.4.3",
        "level": "A",
        "name": "Focus Order",
        "description": "Components receive focus in order that preserves meaning",
        "critical": True
    },
    {
        "id": "2.4.7",
        "level": "AA",
        "name": "Focus Visible",
        "description": "Keyboard focus indicator is visible",
        "critical": True
    },
    {
        "id": "2.4.11",
        "level": "AA",
        "name": "Focus Not Obscured (Minimum)",
        "description": "Focused item is not completely hidden",
        "new_in_2_2": True
    },
    {
        "id": "2.5.7",
        "level": "AA",
        "name": "Dragging Movements",
        "description": "Dragging functions have single pointer alternative",
        "new_in_2_2": True
    },
    {
        "id": "2.5.8",
        "level": "AA",
        "name": "Target Size (Minimum)",
        "description": "Target size is at least 24x24 CSS pixels",
        "new_in_2_2": True
    },
    {
        "id": "3.2.1",
        "level": "A",
        "name": "On Focus",
        "description": "Component does not initiate change of context on focus",
        "critical": True
    },
    {
        "id": "3.2.2",
        "level": "A",
        "name": "On Input",
        "description": "Changing setting does not automatically cause change of context",
        "critical": True
    },
    {
        "id": "3.3.7",
        "level": "A",
        "name": "Redundant Entry",
        "description": "Information previously entered is auto-populated or available",
        "new_in_2_2": True
    },
    {
        "id": "3.3.8",
        "level": "AA",
        "name": "Accessible Authentication (Minimum)",
        "description": "Cognitive function test not required for authentication",
        "new_in_2_2": True
    },
    {
        "id": "4.1.2",
        "level": "A",
        "name": "Name, Role, Value",
        "description": "Name, role, and value can be programmatically determined",
        "critical": True
    },
    {
        "id": "4.1.3",
        "level": "AA",
        "name": "Status Messages",
        "description": "Status messages can be programmatically determined"
    }
]
