import customtkinter as ctk
from tkinter import messagebox
from typing import Dict

# Configuration constants
WINDOW_SIZE = "1000x700"
TITLE = "Testing Application"
THEME = "dark-blue"
APPEARANCE = "dark"
FONT = ("Arial", 18)

# Field configurations
FIELDS = {
    "Username": {"width": 300, "required": True, "show": None},
    "Password": {"width": 300, "required": True, "show": "*"},
    "URL": {"width": 500, "required": True, "show": None},
    "Testing file path": {"width": 500, "required": True, "show": None},
    "Testing file name": {"width": 300, "required": True, "show": None},
    "Test results header (if you want only questions that are not Pass)": {"width": 400, "required": False, "show": None}
}

BROWSER_OPTIONS = ['1', '2', '3', '4']


def setup_window() -> tuple[ctk.CTk, ctk.CTkFrame]:
    """Configure and return the main window and frame."""
    ctk.set_appearance_mode(APPEARANCE)
    ctk.set_default_color_theme(THEME)

    root = ctk.CTk()
    root.geometry(WINDOW_SIZE)
    root.title(TITLE)

    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    return root, frame


def create_entry_fields(frame: ctk.CTkFrame) -> Dict[str, ctk.CTkEntry]:
    """Create and return entry fields based on configuration."""
    entries = {}
    for field, config in FIELDS.items():
        entry = ctk.CTkEntry(
            master=frame,
            placeholder_text=field,
            width=config["width"],
            show=config["show"]
        )
        entry.pack(pady=12, padx=10)
        entries[field] = entry
    return entries


def create_browser_selector(frame: ctk.CTkFrame) -> ctk.CTkComboBox:
    """Create and return the browser sessions selector."""
    ctk.CTkLabel(
        master=frame,
        text="Number of browser sessions",
        font=FONT
    ).pack(pady=12, padx=10)

    selector = ctk.CTkComboBox(
        master=frame,
        values=BROWSER_OPTIONS,
        width=300
    )
    selector.pack(pady=12, padx=10)
    return selector


def validate_inputs(entries: Dict[str, ctk.CTkEntry]) -> bool:
    """Validate required input fields."""
    for field, config in FIELDS.items():
        if config["required"] and not entries[field].get():
            messagebox.showerror("Error", f"Please enter the {field}.")
            return False
    return True


def create_submit_button(frame: ctk.CTkFrame, submit_handler: callable) -> None:
    """Create the submit button."""
    ctk.CTkButton(
        master=frame,
        text="Start",
        command=submit_handler
    ).pack(pady=12, padx=10)


def handle_submit(entries: Dict[str, ctk.CTkEntry], browser_selector: ctk.CTkComboBox) -> None:
    """Handle form submission and initiate testing."""
    if not validate_inputs(entries):
        return

    try:
        import initiate_testing
        initiate_testing.start_testing(
            entries["Username"].get(),
            entries["Password"].get(),
            entries["URL"].get(),
            entries["Testing file path"].get(),
            entries["Testing file name"].get(),
            entries["Test results header (if you want only questions that are not Pass)"].get(),
            browser_selector.get()
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def create_ui(frame: ctk.CTkFrame) -> tuple[Dict[str, ctk.CTkEntry], ctk.CTkComboBox]:
    """Create the user interface elements."""
    # Title
    ctk.CTkLabel(
        master=frame,
        text="Login System",
        font=FONT
    ).pack(pady=12, padx=10)

    # Create entry fields
    entries = create_entry_fields(frame)

    # Create browser selector
    browser_selector = create_browser_selector(frame)

    return entries, browser_selector


def main():
    """Main function to run the application."""
    root, frame = setup_window()
    entries, browser_selector = create_ui(frame)

    # Create submit button with closure over entries and browser_selector
    create_submit_button(
        frame,
        lambda: handle_submit(entries, browser_selector)
    )

    root.mainloop()


if __name__ == "__main__":
    main()

