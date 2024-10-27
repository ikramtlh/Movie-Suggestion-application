import collections.abc
import csv
from tkinter import *
import webbrowser

from models.film import Film
from models.preference_utilisateur import PreferenceUtilisateur

# 👇️ add attributes to `collections` module
# before you import the package that causes the issue
collections.Callable = collections.abc.Callable
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet

# 👇️ import the problematic module below
# import problematic_module

from experta import *

genre_preferee = ""
note_souhaitee = 0
date_preferee = 0
language_preferee = ""


class RecommandationFilm(KnowledgeEngine):
    @Rule(
        PreferenceUtilisateur(
            genre_preferee=MATCH.genre_preferee,
            note_souhaitee=MATCH.note_souhaitee,
            language_preferee=MATCH.language_preferee,
            date_preferee=MATCH.date_preferee,
        )
    )
    def recommander_film_utilisateur(
        self,
        genre_preferee,
        note_souhaitee,
        language_preferee,
        date_preferee,
    ):
        films_recommandes = []
        for film in self.film_data:
            if (
                film.release_date >= 2024 - date_preferee
                and genre_preferee.lower() in film.genre.lower()
                and film.note >= note_souhaitee
                and film.language[1:] == language_preferee
            ):
                films_recommandes.append(film)

        if films_recommandes:
            sixth_page(films_recommandes, 0)


# Open the CSV file and load the data
def load_movie_data(file_path):
    film_data = []
    with open(file_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            film = Film(
                titre=row["names"],
                genre=row["genre"],
                note=float(row["score"]),
                overview=row["overview"],
                language=row["orig_lang"],
                release_date=int(row["date_x"][-5:]),
            )
            film_data.append(film)
    return film_data


def recommand():
    # Load movie data from CSV
    film_data = load_movie_data("assets/csv/movies.csv")

    # Initialize the expert system
    engine = RecommandationFilm()
    engine.film_data = film_data

    # Reset the engine and declare user preferences
    engine.reset()
    engine.declare(
        PreferenceUtilisateur(
            genre_preferee=genre_preferee,
            note_souhaitee=float(note_souhaitee),
            language_preferee=language_preferee,
            date_preferee=date_preferee,
        )
    )

    # Run the engine to make recommendations
    engine.run()


def open_google_link(titre):
    # URL to open
    url = f"https://www.google.com/search?q={titre}+movie"

    # Open the URL in the default web browser
    webbrowser.open(url)


def sixth_page(films, index):
    canvas.delete("all")

    canvas.create_image(0, 0, image=bg, anchor="nw")

    canvas.create_rectangle(600, 100, 1350, 750, fill="#141314", outline="white")

    canvas.create_text(
        650,
        130,
        text="Recommended for you:",
        fill="white",
        font=("Helvetica", 24, "normal"),
        anchor="nw",
    )

    canvas.create_text(
        850,
        200,
        text=films[index].titre,
        fill="white",
        font=("Helvetica", 18, "normal"),
        anchor="nw",
    )

    canvas.create_text(
        850,
        250,
        text=films[index].overview,
        fill="white",
        font=("Helvetica", 14, "normal"),
        width=400,
        anchor="nw",
    )

    root.title("Open Google Link")

    button = Button(
        root,
        text="SEARCH ON GOOGLE",
        width=62,
        height=3,
        bg="#E74C3C",
        fg="white",
        font=("Helvetica", 12, "bold"),
        command=lambda: open_google_link(films[index].titre),
    )

    button2 = Button(
        root,
        text="GET ANOTHER RECOMMENDATION",
        width=62,
        height=3,
        bg="#E74C3C",
        fg="white",
        font=("Helvetica", 12, "bold"),
        command=lambda: sixth_page(films, index + 1 if index < len(films) - 1 else 0),
    )

    button3 = Button(
        root,
        text="GO BACK",
        width=62,
        height=3,
        bg="#141314",
        fg="white",
        font=("Helvetica", 12, "bold"),
        command=second_page,
        borderwidth=0,
    )

    canvas.create_window(680, 450, anchor="nw", window=button)

    canvas.create_window(680, 550, anchor="nw", window=button2)

    canvas.create_window(680, 650, anchor="nw", window=button3)


def fifth_page():
    canvas.delete("all")

    canvas.create_image(0, 0, image=bg, anchor="nw")

    bg_rect = canvas.create_rectangle(
        680, 100, 1560, 160, fill="#141314", outline="white"
    )

    canvas.create_text(
        1120,
        130,
        text="Do you have a preference for movies in a specific language?",
        fill="white",
        font=("Helvetica", 24, "normal"),
    )

    languages = ["English", "French", "Spanish", "Korean", "Japanese", "Italian"]
    y_pos = 220
    selected_idx = None
    for idx, language in enumerate(languages):
        bg_rect = canvas.create_rectangle(
            680, y_pos - 30, 1300, y_pos + 30, fill="#141314", outline="white"
        )

        # Create text label with slightly smaller width
        text_width = 1280 - 700  # Calculate width based on rectangle coordinates
        text_label = canvas.create_text(
            700,
            y_pos,
            text=language,
            fill="white",
            font=("Helvetica", 16, "normal"),
            anchor="w",
            width=text_width,  # Set width for hitbox
        )

        # Create a larger hitbox rectangle encompassing both text and background
        hitbox_rect = canvas.create_rectangle(
            680,
            y_pos - 30,
            1300,
            y_pos + 30,
            fill="",
            outline="",
            width=0,  # Invisible rectangle
        )

        # Add tags for identification
        canvas.itemconfig(text_label, tags=f"text_{idx}")
        canvas.itemconfig(bg_rect, tags=f"bg_rect_{idx}")
        canvas.itemconfig(hitbox_rect, tags=f"hitbox_{idx}")

        # Define function to handle click event
        def on_genre_click(_, idx=idx):
            nonlocal selected_idx  # Modify the nonlocal variable

            # Deselect previously selected item (if any)
            if selected_idx is not None:
                prev_bg_rect = canvas.find_withtag(f"bg_rect_{selected_idx}")
                canvas.itemconfig(prev_bg_rect, fill="#141314")

            # Update selected item and change color
            selected_idx = idx
            clicked_bg_rect = canvas.find_withtag(f"bg_rect_{idx}")
            canvas.itemconfig(clicked_bg_rect, fill="#E74C3C")
            global language_preferee
            language_preferee = languages[idx]

        # Bind click event to the hitbox rectangle
        canvas.tag_bind(hitbox_rect, "<Button-1>", on_genre_click)

        y_pos += 70

    button1 = Button(
        root,
        text="Next",
        width=62,
        height=3,
        bg="#E74C3C",
        fg="white",
        font=("Helvetica", 12, "bold"),
        command=recommand,
    )

    canvas.create_window(680, 650, anchor="nw", window=button1)


def forth_page():
    canvas.delete("all")

    canvas.create_image(0, 0, image=bg, anchor="nw")

    bg_rect = canvas.create_rectangle(
        680, 100, 1400, 160, fill="#141314", outline="white"
    )

    canvas.create_text(
        910,
        130,
        text="Select the desired movie rating:",
        fill="white",
        font=("Helvetica", 24, "normal"),
    )

    ratings = [4, 5, 6, 7, 8, 9]
    y_pos = 220
    selected_idx = None
    for idx, rating in enumerate(ratings):
        bg_rect = canvas.create_rectangle(
            680, y_pos - 30, 1300, y_pos + 30, fill="#141314", outline="white"
        )

        # Create text label with slightly smaller width
        text_width = 1280 - 700  # Calculate width based on rectangle coordinates
        text_label = canvas.create_text(
            700,
            y_pos,
            text=rating,
            fill="white",
            font=("Helvetica", 16, "normal"),
            anchor="w",
            width=text_width,  # Set width for hitbox
        )

        # Create a larger hitbox rectangle encompassing both text and background
        hitbox_rect = canvas.create_rectangle(
            680,
            y_pos - 30,
            1300,
            y_pos + 30,
            fill="",
            outline="",
            width=0,  # Invisible rectangle
        )

        # Add tags for identification
        canvas.itemconfig(text_label, tags=f"text_{idx}")
        canvas.itemconfig(bg_rect, tags=f"bg_rect_{idx}")
        canvas.itemconfig(hitbox_rect, tags=f"hitbox_{idx}")

        # Define function to handle click event
        def on_genre_click(_, idx=idx):
            nonlocal selected_idx  # Modify the nonlocal variable

            # Deselect previously selected item (if any)
            if selected_idx is not None:
                prev_bg_rect = canvas.find_withtag(f"bg_rect_{selected_idx}")
                canvas.itemconfig(prev_bg_rect, fill="#141314")

            # Update selected item and change color
            selected_idx = idx
            clicked_bg_rect = canvas.find_withtag(f"bg_rect_{idx}")
            canvas.itemconfig(clicked_bg_rect, fill="#E74C3C")
            global note_souhaitee
            note_souhaitee = ratings[idx]

        # Bind click event to the hitbox rectangle
        canvas.tag_bind(hitbox_rect, "<Button-1>", on_genre_click)

        y_pos += 70

    # Create Buttons
    button1 = Button(
        root,
        text="Next",
        width=62,
        height=3,
        bg="#E74C3C",
        fg="white",
        font=("Helvetica", 12, "bold"),
        command=fifth_page,
    )

    canvas.create_window(680, 650, anchor="nw", window=button1)


def third_page():

    canvas.delete("all")

    canvas.create_image(0, 0, image=bg, anchor="nw")

    bg_rect = canvas.create_rectangle(
        680, 100, 1400, 160, fill="#141314", outline="white"
    )

    canvas.create_text(
        970,
        130,
        text="How old would you like the movie to be?",
        fill="white",
        font=("Helvetica", 24, "normal"),
    )

    years = [3, 5, 10, 20, 30, 50]
    y_pos = 220
    selected_idx = None  # Variable to track currently selected item

    for idx, year in enumerate(years):
        # Create background rectangle
        bg_rect = canvas.create_rectangle(
            680, y_pos - 30, 1300, y_pos + 30, fill="#141314", outline="white"
        )

        # Create text label with slightly smaller width
        text_width = 1280 - 700  # Calculate width based on rectangle coordinates
        text_label = canvas.create_text(
            700,
            y_pos,
            text=f"Published in the last {year} years.",
            fill="white",
            font=("Helvetica", 16, "normal"),
            anchor="w",
            width=text_width,  # Set width for hitbox
        )

        # Create a larger hitbox rectangle encompassing both text and background
        hitbox_rect = canvas.create_rectangle(
            680,
            y_pos - 30,
            1300,
            y_pos + 30,
            fill="",
            outline="",
            width=0,  # Invisible rectangle
        )

        # Add tags for identification
        canvas.itemconfig(text_label, tags=f"text_{idx}")
        canvas.itemconfig(bg_rect, tags=f"bg_rect_{idx}")
        canvas.itemconfig(hitbox_rect, tags=f"hitbox_{idx}")

        # Define function to handle click event
        def on_genre_click(_, idx=idx):
            nonlocal selected_idx  # Modify the nonlocal variable

            # Deselect previously selected item (if any)
            if selected_idx is not None:
                prev_bg_rect = canvas.find_withtag(f"bg_rect_{selected_idx}")
                canvas.itemconfig(prev_bg_rect, fill="#141314")

            # Update selected item and change color
            selected_idx = idx
            clicked_bg_rect = canvas.find_withtag(f"bg_rect_{idx}")
            canvas.itemconfig(clicked_bg_rect, fill="#E74C3C")
            global date_preferee
            date_preferee = years[idx]

        # Bind click event to the hitbox rectangle
        canvas.tag_bind(hitbox_rect, "<Button-1>", on_genre_click)

        y_pos += 70

    button1 = Button(
        root,
        text="Next",
        width=62,
        height=3,
        bg="#E74C3C",
        fg="white",
        font=("Helvetica", 12, "bold"),
        command=forth_page,
    )

    canvas.create_window(680, 650, anchor="nw", window=button1)


def second_page():
    canvas.delete("all")

    canvas.create_image(0, 0, image=bg, anchor="nw")

    bg_rect = canvas.create_rectangle(
        680, 100, 1400, 160, fill="#141314", outline="white"
    )

    canvas.create_text(
        1010,
        130,
        text="Please choose any genre you’re interested in.",
        fill="white",
        font=("Helvetica", 24, "normal"),
    )

    genres = ["Drama", "Action", "Comedy", "Adventure", "Science Fiction", "Horror"]
    y_pos = 220
    selected_idx = None  # Variable to track currently selected item

    for idx, genre in enumerate(genres):
        # Create background rectangle
        bg_rect = canvas.create_rectangle(
            680, y_pos - 30, 1300, y_pos + 30, fill="#141314", outline="white"
        )

        # Create text label with slightly smaller width
        text_width = 1280 - 700  # Calculate width based on rectangle coordinates
        text_label = canvas.create_text(
            700,
            y_pos,
            text=genre,
            fill="white",
            font=("Helvetica", 16, "normal"),
            anchor="w",
            width=text_width,  # Set width for hitbox
        )

        # Create a larger hitbox rectangle encompassing both text and background
        hitbox_rect = canvas.create_rectangle(
            680,
            y_pos - 30,
            1300,
            y_pos + 30,
            fill="",
            outline="",
            width=0,  # Invisible rectangle
        )

        # Add tags for identification
        canvas.itemconfig(text_label, tags=f"text_{idx}")
        canvas.itemconfig(bg_rect, tags=f"bg_rect_{idx}")
        canvas.itemconfig(hitbox_rect, tags=f"hitbox_{idx}")

        # Define function to handle click event
        def on_genre_click(_, idx=idx):
            nonlocal selected_idx  # Modify the nonlocal variable

            # Deselect previously selected item (if any)
            if selected_idx is not None:
                prev_bg_rect = canvas.find_withtag(f"bg_rect_{selected_idx}")
                canvas.itemconfig(prev_bg_rect, fill="#141314")

            # Update selected item and change color
            selected_idx = idx
            clicked_bg_rect = canvas.find_withtag(f"bg_rect_{idx}")
            canvas.itemconfig(clicked_bg_rect, fill="#E74C3C")
            global genre_preferee
            genre_preferee = genres[idx]

        # Bind click event to the hitbox rectangle
        canvas.tag_bind(hitbox_rect, "<Button-1>", on_genre_click)

        y_pos += 70

    button1 = Button(
        root,
        text="Next",
        width=62,
        height=3,
        bg="#E74C3C",
        fg="white",
        font=("Helvetica", 12, "bold"),
        command=third_page,
    )

    canvas.create_window(680, 650, anchor="nw", window=button1)


def first_page():
    canvas.create_image(0, 0, image=bg, anchor="nw")

    canvas.create_text(
        1000,
        150,
        text="MOVIE RECOMMENDATION ENGINE",
        fill="white",
        font=("Helvetica", 32, "bold"),
    )

    canvas.create_text(
        1000,
        230,
        text="You can’t decide between thousands of movies available for streaming?",
        fill="white",
        font=("Helvetica", 24, "normal"),
    )

    canvas.create_text(
        1000,
        280,
        text="Answer 4 questions and let us do the work!",
        fill="white",
        font=("Helvetica", 24, "normal"),
    )

    labels_text = [
        "✓ time-saving & easy to use\n\n",
        "✓ free & no registration\n\n",
        "✓ watch trailers directly\n\n",
        "✓ only high-quality movies\n\n",
        "✓ special recommendations\n   for movie nights\n\n",
        "✓ special categories\n   (e.g. movies based on true\n    stories, action movies …)",
    ]

    # Calculate the coordinates for the gray background rectangle
    x0, y0 = 50, 300
    x1, y1 = 340, 300 + len(labels_text) * 60

    # Add gray background rectangle
    canvas.create_rectangle(x0, y0, x1, y1, fill="#141314", outline="white")

    for idx, text in enumerate(labels_text):
        canvas.create_text(
            70,
            350 + idx * 50,
            text=text,
            fill="white",
            anchor="w",
            font=("Helvetica", 14, "normal"),
        )

    button1 = Button(
        root,
        text="Start Now",
        width=30,
        height=4,
        bg="#E74C3C",
        fg="white",
        font=("Helvetica", 12, "bold"),
        command=second_page,
    )

    canvas.create_window(850, 500, anchor="nw", window=button1)


if __name__ == "__main__":

    # Create object
    root = Tk()

    # Adjust size
    root.geometry("1920x1000")

    # Add image file
    bg = PhotoImage(file="assets/images/background.png")

    # Create Canvas
    canvas = Canvas(root, width=400, height=400)

    canvas.pack(fill="both", expand=True)

    first_page()

    # Execute tkinter
    root.mainloop()
