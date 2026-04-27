from __future__ import annotations

import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from linkedin_poster import post_to_linkedin


def parse_scheduled_time(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M")


class LinkedInAutoPosterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("LinkedIn Auto Poster (Windows)")
        self.root.geometry("700x500")

        self.status_var = tk.StringVar(value="Ready")

        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Post text:").pack(anchor="w")
        self.post_text = tk.Text(container, height=10, wrap="word")
        self.post_text.pack(fill="x", pady=(4, 12))

        ttk.Label(container, text="Schedule (YYYY-MM-DD HH:MM):").pack(anchor="w")
        self.schedule_entry = ttk.Entry(container)
        self.schedule_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.schedule_entry.pack(fill="x", pady=(4, 12))

        ttk.Label(container, text="Chrome user data dir:").pack(anchor="w")
        self.user_data_dir = ttk.Entry(container)
        self.user_data_dir.insert(0, r"C:\Users\YOUR_USER\AppData\Local\Google\Chrome\User Data")
        self.user_data_dir.pack(fill="x", pady=(4, 12))

        ttk.Label(container, text="Chrome profile directory (Default/Profile 1/...):").pack(anchor="w")
        self.profile_dir = ttk.Entry(container)
        self.profile_dir.insert(0, "Default")
        self.profile_dir.pack(fill="x", pady=(4, 12))

        self.dry_run = tk.BooleanVar(value=False)
        ttk.Checkbutton(container, text="Dry run (open composer but do not click Post)", variable=self.dry_run).pack(
            anchor="w", pady=(0, 14)
        )

        ttk.Button(container, text="Schedule Post", command=self.on_schedule).pack(anchor="w")

        ttk.Separator(container).pack(fill="x", pady=16)
        ttk.Label(container, textvariable=self.status_var).pack(anchor="w")

    def on_schedule(self) -> None:
        text = self.post_text.get("1.0", "end").strip()
        if not text:
            messagebox.showerror("Validation", "Post text cannot be empty.")
            return

        try:
            scheduled_at = parse_scheduled_time(self.schedule_entry.get())
        except ValueError:
            messagebox.showerror("Validation", "Use schedule format: YYYY-MM-DD HH:MM")
            return

        if scheduled_at <= datetime.now():
            messagebox.showerror("Validation", "Schedule time must be in the future.")
            return

        user_data_dir = self.user_data_dir.get().strip()
        profile_dir = self.profile_dir.get().strip()
        if not user_data_dir or not profile_dir:
            messagebox.showerror("Validation", "Chrome profile settings are required.")
            return

        self.status_var.set(f"Scheduled for {scheduled_at:%Y-%m-%d %H:%M}. Keep this window open.")

        thread = threading.Thread(
            target=self._run_job,
            args=(text, scheduled_at, user_data_dir, profile_dir, self.dry_run.get()),
            daemon=True,
        )
        thread.start()

    def _run_job(
        self,
        post_text: str,
        scheduled_at: datetime,
        user_data_dir: str,
        profile_dir: str,
        dry_run: bool,
    ) -> None:
        self.status_var.set("Waiting for scheduled time...")

        while datetime.now() < scheduled_at:
            self.root.after(0, lambda: self.status_var.set(f"Waiting... ({datetime.now():%Y-%m-%d %H:%M:%S})"))
            import time

            time.sleep(1)

        self.root.after(0, lambda: self.status_var.set("Posting now..."))

        try:
            post_to_linkedin(
                post_text=post_text,
                user_data_dir=user_data_dir,
                profile_dir=profile_dir,
                dry_run=dry_run,
            )
            final_message = "Dry run complete." if dry_run else "Post published successfully."
            self.root.after(0, lambda: self.status_var.set(final_message))
        except Exception as exc:  # noqa: BLE001
            self.root.after(0, lambda: self.status_var.set(f"Failed: {exc}"))


def main() -> None:
    root = tk.Tk()
    LinkedInAutoPosterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
