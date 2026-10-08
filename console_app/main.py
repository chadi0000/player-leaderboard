from player import Player


def add_player(players):
    """Vraagt een username en voegt een nieuwe Player toe aan de lijst."""
    username = input("Voer een username in: ")
    new_id = len(players) + 1
    new_player = Player(new_id, username)
    players.append(new_player)
    print(f"Speler '{username}' toegevoegd met id {new_id}.")


def view_all_players(players):
    """Print alle spelers in de lijst."""
    if not players:
        print("Er zijn nog geen spelers.")
        return

    for p in players:
        print(p)


def search_player(players, query):
    """Zoekt een speler op id of username. Print het resultaat."""
    for p in players:
        if str(p.id) == str(query) or p.username.lower() == str(query).lower():
            print("Gevonden:", p)
            return p

    print(f"Geen speler gevonden met id/username '{query}'.")
    return None


def update_score(players, query, new_score):
    """Zoekt een speler op en past diens score aan."""
    player = search_player(players, query)

    if player is None:
        return

    player.score = new_score
    print(f"Score van '{player.username}' aangepast naar {player.score}.")


def show_leaderboard(players):
    """Print alle spelers gesorteerd op score, hoogste eerst."""
    if not players:
        print("Er zijn nog geen spelers.")
        return

    sorted_players = sorted(players, key=lambda p: p.score, reverse=True)

    for rank, p in enumerate(sorted_players, start=1):
        print(f"{rank}. {p.username} - score: {p.score}")


# Lijst die alle spelers bijhoudt
players = []


def show_menu():
    """Print het menu met keuzes."""
    print("\n--- MENU ---")
    print("1. Speler toevoegen")
    print("2. Alle spelers bekijken")
    print("3. Speler zoeken")
    print("4. Score wijzigen")
    print("5. Leaderboard tonen")
    print("6. Afsluiten")


def main():
    while True:
        show_menu()
        keuze = input("Maak een keuze (1-6): ")

        if keuze == "1":
            add_player(players)
        elif keuze == "2":
            view_all_players(players)
        elif keuze == "3":
            query = input("Zoek op id of username: ")
            search_player(players, query)
        elif keuze == "4":
            query = input("Voor welke speler wil je de score wijzigen (id of username)? ")
            try:
                new_score = int(input("Nieuwe score: "))
                update_score(players, query, new_score)
            except ValueError:
                print("Ongeldige invoer: voer een geheel getal in voor de score.")
        elif keuze == "5":
            show_leaderboard(players)
        elif keuze == "6":
            print("Tot ziens!")
            break
        else:
            print("Ongeldige keuze, probeer opnieuw.")


main()