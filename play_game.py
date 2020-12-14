import json
import random

def main():
    # TODO: allow them to choose from multiple JSON files?
    with open('spooky_mansion.json') as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)


def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    items_in_the_room = {}
    # The things the player has collected.
    stuff = ['Cellphone with no battery...']
    
    
    while True:
        print("")
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"], here['itemsinroom'])
        
        
        
        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.
        if current_place not in items_in_the_room:
            items_in_the_room[current_place] = here['itemsinroom']
        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_visable_exits(here)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))
        
        kitty = random.randint (1, 5)
        if kitty == 3:
            print("you see a black cat")

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        if action == "help":
            print_instructions()
            continue
        if action == "stuff":
            print(stuff)
            continue
        if action == "take":
            stuff.append(here['itemsinroom'])
            here['itemsinroom'].clear()
            continue       
        if action == "drop":
            print(stuff)
            s = int(input('What do you want to remove?'))  
            j = stuff.pop(s)
            here['itemsinroom'].append(j)
            if (j == 'rawfish') and (kitty == 3):
                print("Cat purrs and doesn't leave room")
            continue
        if action == "search":
            for exit in here['exits']:
                if ('hidden' in exit) == True:
                    exit['hidden'] = False
            continue
        
            

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if 'required_key' in selected:
                if (selected['required_key'] in stuff) == True:
                     current_place = selected['destination']
                else:
                    print("You need key")
            else:
                current_place = selected['destination']
                print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
       
    print("")
    print("")
    print("=== GAME OVER ===")

def find_visable_exits(room):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'drop' to remove an item.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()