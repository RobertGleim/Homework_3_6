
import requests
import json
import os

from colorama import Fore


def show_menu():
    """Display the main menu"""
    print(Fore.GREEN+"\nBored Activity Finder")
    print(Fore.MAGENTA+"=" * 50 + Fore.RESET)
    print(Fore.BLUE+"1. Get a random activity")
    print("2. Get activity by type")
    print("3. Get activity by participants")
    print("4. Save my own activity")
    print("5. View my saved activities")
    print("6. Remove a saved activity")
    print(Fore.YELLOW+"9. Exit" + Fore.RESET)
    print(Fore.MAGENTA + "=" * 50 + Fore.RESET)


def get_random_activity():
    os.system('cls' if os.name == 'nt' else 'clear')
    response = requests.get(
        url="https://bored-api.appbrewery.com/random", timeout=10)
    if response.status_code == 200:
        data = response.json()
        activity = data.get('activity', 'No activity found.').title()
        activity_type = data.get('type', 'unknown').title()
        participants = data.get('participants', 'N/A')
        print(Fore.MAGENTA+"=" * 50 + Fore.RESET)
        print(Fore.GREEN+"Get Random Activity" + Fore.RESET)
        print(Fore.BLUE+f"Random Activity: \n--{activity}, \n--{activity_type},\n--{participants} Participant(s)")
        print(Fore.MAGENTA+"=" * 50 + Fore.RESET)
        prompt_to_save(activity)
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print(Fore.RED+"Failed to fetch activity. Please try again.")


def get_activity_by_type():
    os.system('cls' if os.name == 'nt' else 'clear')
    activity_map = {

        "1": "education",
        "2": "recreational",
        "3": "social",
        "4": "charity",
        "5": "cooking",
        "6": "relaxation",
        "7": "busywork",
    }
    print(Fore.GREEN+"Get Activity by Type" + Fore.RESET)
    print(Fore.MAGENTA+"=" * 50 + Fore.RESET)
    user_input = input(Fore.BLUE+"""
                       
    Enter activity type: 
    1.Education 
    2.Recreational 
    3.Social
    4.Charity 
    5.Cooking 
    6.Relaxation 
    7.Busywork"""
                       + Fore.CYAN+"Please choose 1-7: "+Fore.RESET).strip()
    activity_type = activity_map.get(user_input)
    if activity_type:
        response = requests.get(
            f"https://bored-api.appbrewery.com/filter?type={activity_type}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                activity = data[0]['activity']
                print(Fore.BLUE+f"\nActivity: {data[0]['activity']}")
                print(f"Type: {data[0]['type'].capitalize()}")
                print(f"Participants: {data[0]['participants']}")
                prompt_to_save(activity)
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                print("No activity found for this type.")
        else:
            print("Failed to fetch activity. Please try again.")
    else:
        print("Invalid type selection. Please choose a number between 1 and 7.")


def get_activity_by_participants():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.MAGENTA+"=" * 50 + Fore.RESET)
    print(Fore.BLUE+"Get Activity by Participants (Number of People 1, 2, 3, 4, 5, 8)")
    num = int(input("Enter number of participants: "+Fore.RESET))
    response = requests.get(
        f"https://bored-api.appbrewery.com/filter?participants={num}", timeout=10)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and data:
            activity = data[0]['activity']
            print(Fore.BLUE+f"\nActivity: \n{data[0]['activity'].title()}")
            print(f"Type: {data[0]['type'].capitalize()}")
            print(f"Participants: {data[0]['participants']}")
            prompt_to_save(activity)
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("No activity found for that number of participants.")
    else:
        print(Fore.YELLOW+"Failed to fetch activity. Please try again.")


def save_favorite_activity(activity=None):
    if activity is None:
        print(Fore.MAGENTA+"=" * 50 + Fore.RESET)
        activity = input(Fore.CYAN+"\nSave your own Activity:"+Fore.RESET).strip()
    if activity:
        try:
            with open("favorite_activities.txt", "a", encoding="utf-8") as file:
                file.write(activity + "\n")
            print(Fore.YELLOW+"Activity saved successfully!"+Fore.RESET)
        except IOError as e:
            print(Fore.RED+f"Error saving activity: {e}")
    else:
        print(Fore.YELLOW+"No activity entered to save.")


def prompt_to_save(activity_text):
    save = input(
        Fore.CYAN+f"Do you want to save this activity: '{activity_text}'? (yes/no): "+Fore.RESET).strip().lower()
    if save in ['yes', 'y']:
        save_favorite_activity(activity_text)
    else:
        print(Fore.YELLOW+"Activity not saved.")


def view_saved_activities():
    os.system('cls' if os.name == 'nt' else 'clear')
    with open("favorite_activities.txt", "r", encoding="utf-8") as file:
        activities = file.readlines()
        if activities:
            print(Fore.GREEN+"\nYour Saved Activities:"+Fore.RESET)
            for activity in activities:
                print(Fore.BLUE+f"- {activity.strip()}"+Fore.RESET)

        else:
            print(Fore.YELLOW+"No saved activities found.")


def remove_saved_activity():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        try:
            with open("favorite_activities.txt", "r", encoding="utf-8") as file:
                activities = file.readlines()
        except FileNotFoundError:
            print(Fore.YELLOW+"No saved activities found.")

            return

        if not activities:
            print(Fore.YELLOW+"No saved activities to Remove.")

            return

        print(Fore.GREEN+"\nYour Saved Activities:"+Fore.RESET)
        for index, activity in enumerate(activities, start=1):
            print(Fore.BLUE + f"{index}. {activity.strip()}")
        print("\nEnter the number of the activity you want to remove.")
        print("Enter 0 to return to the main menu.")

        choice = input(Fore.CYAN+"Your choice: "+Fore.RESET).strip()

        if choice.strip() == '0':
            print("Returning to main menu...")

            return

        if not choice.isdigit():
            print("Invalid input. Please enter a valid number.")

            continue

        choice = int(choice)
        if 1 <= choice <= len(activities):
            removed_activity = activities.pop(choice - 1).strip()
            with open("favorite_activities.txt", "w", encoding="utf-8") as file:
                file.writelines([activity if activity.endswith(
                    '\n') else activity + '\n' for activity in activities])
            print(f"Removed activity: {removed_activity}")

            return
        else:
            print("Invalid choice. Please try again.")


def main():
    """Main function with menu loop"""
    print("Welcome to the Bored Activity Finder!")

    while True:
        show_menu()

        try:
            choice = input(
                Fore.CYAN+"\nChoose an option (1-6) or 9 TO EXIT: "+Fore.RESET).strip()

            if choice == '1':
                get_random_activity()
            elif choice == '2':
                get_activity_by_type()
            elif choice == '3':
                get_activity_by_participants()
            elif choice == '4':
                save_favorite_activity()
            elif choice == '5':
                view_saved_activities()
            elif choice == '6':
                remove_saved_activity()
            elif choice == '9':
                print(Fore.GREEN+"Thanks for using Bored Activity Finder, Come bcck soon!!!!"+Fore.RESET)
                break
            else:
                print(Fore.YELLOW+"Invalid choice! Please choose 1-5 or 9 to exit."+Fore.RESET)

        except KeyboardInterrupt:
            print(Fore.GREEN+"\n\nGoodbye!"+Fore.RESET)
            break


if __name__ == "__main__":
    main()
