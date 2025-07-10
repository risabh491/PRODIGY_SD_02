import random
import threading
import time
import customtkinter as ctk
from PIL import Image, ImageTk

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NumberGuessingGame:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🎯 Number Guessing Game")
        self.root.geometry("500x700")
        self.root.resizable(False, False)

        # Game state
        self.target_number = None
        self.attempts = 0
        self.min_range = 1
        self.max_range = 100
        self.game_active = False

        self.setup_ui()
        self.start_new_game()

    def setup_ui(self):
        # Main layout
        main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🎯 Guess My Number!",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=("#2CC985", "#2FA572")
        )
        title_label.pack(pady=(0, 10))

        # Info label
        self.info_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=16),
            text_color=("gray70", "gray30"),
            wraplength=400
        )
        self.info_label.pack(pady=(0, 30))

        # Game frame
        self.game_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=20,
            fg_color=("gray90", "gray13"),
            border_width=2,
            border_color=("gray70", "gray25")
        )
        self.game_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Input section
        input_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        input_frame.pack(pady=30, padx=30, fill="x")

        guess_label = ctk.CTkLabel(
            input_frame,
            text="Enter your guess:",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("gray20", "gray90")
        )
        guess_label.pack(pady=(0, 15))

        self.guess_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text=f"Number between {self.min_range} and {self.max_range}",
            font=ctk.CTkFont(size=16),
            height=45,
            border_width=2,
            corner_radius=10
        )
        self.guess_entry.pack(fill="x", pady=(0, 20))
        self.guess_entry.bind("<Return>", lambda event: self.make_guess())

        # Feedback label
        self.feedback_label = ctk.CTkLabel(
            self.game_frame,
            text="",
            font=ctk.CTkFont(size=16),
            text_color=("gray20", "gray80")
        )
        self.feedback_label.pack(pady=(0, 10))

        # Stats
        self.stats_label = ctk.CTkLabel(
            self.game_frame,
            text="Attempts: 0",
            font=ctk.CTkFont(size=14)
        )
        self.stats_label.pack()

        self.progress_bar = ctk.CTkProgressBar(self.game_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(10, 20), fill="x", padx=20)

        # Image (placeholder)
        self.image_label = ctk.CTkLabel(self.game_frame, text="")
        self.image_label.pack(pady=(10, 10))
        self.set_image("https://via.placeholder.com/100")  # You can change this to a local path

        # Buttons
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        self.guess_button = ctk.CTkButton(
            button_frame,
            text="🎯 Make Guess",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=40,
            corner_radius=10,
            command=self.make_guess,
            hover_color=("#1166aa", "#14487f")
        )
        self.guess_button.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.new_game_button = ctk.CTkButton(
            button_frame,
            text="🔄 New Game",
            command=self.start_new_game
        )
        self.new_game_button.pack(side="left", expand=True, fill="x")

    def set_image(self, path):
        try:
            from urllib.request import urlopen
            import io
            if path.startswith("http"):
                image_bytes = urlopen(path).read()
                img = Image.open(io.BytesIO(image_bytes))
            else:
                img = Image.open(path)
            img = img.resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        except Exception as e:
            print(f"Image load failed: {e}")

    def start_new_game(self):
        self.target_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_active = True

        self.info_label.configure(
            text=f"I'm thinking of a number between {self.min_range} and {self.max_range}. Can you guess what it is?"
        )
        self.feedback_label.configure(
            text="👀 Ready when you are! Enter your first guess above.",
            text_color=("gray20", "gray80")
        )
        self.stats_label.configure(text="Attempts: 0")
        self.progress_bar.set(0)
        self.guess_entry.focus()

    def make_guess(self):
        if not self.game_active:
            return

        guess = self.guess_entry.get()
        try:
            guess = int(guess)
        except ValueError:
            self.feedback_label.configure(text="❌ Please enter a valid number.")
            return

        self.attempts += 1
        self.stats_label.configure(text=f"Attempts: {self.attempts}")
        self.progress_bar.set(min(self.attempts / 10, 1.0))

        if guess < self.target_number:
            self.feedback_label.configure(text="🔼 Too low! Try again.")
        elif guess > self.target_number:
            self.feedback_label.configure(text="🔽 Too high! Try again.")
        else:
            self.feedback_label.configure(text="🎉 Correct! You guessed it!")
            self.game_active = False

        self.guess_entry.delete(0, 'end')

if __name__ == "__main__":
    app = NumberGuessingGame()
    app.root.mainloop()
