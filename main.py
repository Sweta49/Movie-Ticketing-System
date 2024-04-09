import json

# Global variables 
USERS_FILE = "users.json"
MOVIES_FILE = "movies.json"

def load_data(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        data = {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file '{filename}'.")
        data = {}
    return data

def save_data(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def load_movies_data():
    movies = load_data(MOVIES_FILE)
    return movies.get("movies", [])

def save_movies_data(movies):
    updated_movies = {'movies': movies}
    save_data(updated_movies, MOVIES_FILE)

def sign_up():
    users = load_data(USERS_FILE)

    while True:
        username = input("Enter a unique Username: ")

        if username in users:
            print("Username already exists. Please choose a different one.")
        else:
            # Add the new user to the dictionary with an empty history list
            users[username] = {'history': []}
            save_data(users, USERS_FILE)
            print("Sign up successful!")
            break

def log_in():
    users = load_data(USERS_FILE)
    username = input("Enter your Username: ")

    if username not in users:
        print("Username does not exist.")
        return None
    else:
        print("Login successful!")
        return username

def show_available_movies():
    movies = load_movies_data()
    print("Available Movies:")
    for movie in movies:
        print(f"{movie['id']}. {movie['name']}")

def book_ticket(username):
    movies = load_movies_data()
    show_available_movies()

    movie_id = input("Enter the movie ID you want to book: ")
    movie = next((m for m in movies if str(m["id"]) == movie_id), None)
    
    if not movie:
        print("Movie not found.")
        return

    # Check for seats
    seats_available = movie['seats']
    if seats_available == 0:
        print("Sorry, no seats available for this movie.")
        return

    # Ticket Booking
    seat_number = input("Enter the seat number you want to book: ")

    # movie data
    movie['seats'] -= 1
    save_movies_data(movies)

    # user's history
    users = load_data(USERS_FILE)
    users[username]['history'].append({
        'movie': movie['name'],
        'seat': seat_number
    })
    save_data(users, USERS_FILE)

    print("Ticket booked successfully!")

def main():
    while True:
        print("\nWelcome to Movie Ticketing System")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Show Available Movies")
        print("4. Book a Ticket")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            sign_up()
        elif choice == '2':
            username = log_in()
            if username:
                current_user = username
        elif choice == '3':
            show_available_movies()
        elif choice == '4':
            if 'current_user' in locals():
                book_ticket(current_user)
            else:
                print("Please log in first.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
