import os


coinweights = {
    "£2": 12.00,
    "£1": 8.75,
    "50p": 8.00,
    "20p": 5.00,
    "10p": 6.50,
    "5p": 2.35,
    "2p": 7.12,
    "1p": 3.56
}

coinvalues = {
    "£2": 2.00,
    "£1": 1.00,
    "50p": 0.50,
    "20p": 0.20,
    "10p": 0.10,
    "5p": 0.05,
    "2p": 0.02,
    "1p": 0.01
}

bagvalues = {
    "£2": 20,
    "£1": 20,
    "50p": 10,
    "20p": 10,
    "10p": 5,
    "5p": 5,
    "2p": 1,
    "1p": 1
}
total_bags_checked = 0
total_value_of_coins = 0.0
coin_data = []

def display_sorted_volunteers(volunteers):
    sorted_volunteers = sorted(volunteers.items(), key=lambda x: x[1][2], reverse=True)  # Sort by accuracy in descending order

    print("\n\033[91mVolunteer List Sorted by Accuracy:\033[0m")
    for volname, data in sorted_volunteers:
        correct_bags = data[0]
        total_bags = data[1]
        accuracy = data[2]
        print(f"\033[92mVolunteer Name: {volname}")
        print(f"Total Bags Counted: {total_bags}")
        print(f"Correct Bags Percentage: {accuracy:.2f}%")
        print("-" * 30)


# Load data from a file
loaded_volunteers = {}
data_file = "CoinCount.txt"

if os.path.exists(data_file):
    try:
        with open(data_file, "r") as file:
            lines = file.readlines()

            i = 0
            while i < len(lines):
                if lines[i].strip().startswith("Volunteer:") and \
                   lines[i + 1].strip().startswith("Correct Bags:") and \
                   lines[i + 2].strip().startswith("Total Bags:") and \
                   lines[i + 3].strip().startswith("Accuracy:"):
                    volname = lines[i].strip().split(": ")[1]
                    correct_bags = int(lines[i + 1].strip().split(": ")[1])
                    total_bags = int(lines[i + 2].strip().split(": ")[1])
                    accuracy = float(lines[i + 3].strip().split(": ")[1].strip('%'))

                    loaded_volunteers[volname] = [correct_bags, total_bags, accuracy]

                    i += 4
                elif lines[i].strip().startswith("Total Number of Bags Checked:"):
                    total_bags_checked = int(lines[i].strip().split(": ")[1])
                    i += 1
                elif lines[i].strip().startswith("Total Value of Coins:"):
                    total_value_of_coins = float(lines[i].strip().split("£")[1])
                    i += 1
                else:
                    i += 1

        print("Data loaded from CoinCount.txt.")
    except FileNotFoundError:
        print("No data file found. Please save data first.")

volunteers = {}
totalbags = 0

numofvol = (input("\033[91mEnter the number of volunteers: \033[0m"))  # asks number of volunteers
while not numofvol.isdigit():  # validates correct input
    print("\033[91mInvalid Input! Please enter a valid number of volunteers")
    numofvol = (input("\033[91mEnter the number of volunteers: "))

numofvol = int(numofvol)


for _ in range(numofvol):
    valid_coin_types = {"£2", "£1", "50p", "20p", "10p", "5p", "2p", "1p"}

    volname = input("\033[91mEnter Volunteer's name: ").capitalize()  # asks volunteers name and capitalizes it
    numofbags = input(f"\033[91mHow many bags does \033[92m{volname} \033[91mhave?")  # asks how many bags volunteer has
    while not numofbags.isdigit():  # validates correct input
        print("\033[91mInvalid input! Please enter a valid number of bags.")
        numofbags = input(f"\033[91mHow many bags does \033[92m{volname} \033[91mhave?")

    numofbags = int(numofbags)

    totalvolbags = 0
    correctvolbags = 0

    for i in range(numofbags):
        bagnum = i + 1

        ctype = input(f"\033[91mEnter Coin type for bag \033[94m{bagnum}\033[91m: ")
        while ctype not in valid_coin_types:  # validates correct input
            print("\033[91mInvalid Coin type! Please enter a valid Coin type.")
            ctype = input("\033[91mEnter Coin type: ")

        while True:
            bagw8_input = input(f"\033[91mEnter Bag weight for bag \033[94m{bagnum}\033[91m: ")
            try:
                bagw8 = float(bagw8_input)
                if bagw8 % coinweights[ctype] == 0:
                    break
                else:
                    print("\033[91mInvalid Bag weight! Please enter a valid multiple.")
            except ValueError:  # validates correct input
                print("\033[91mInvalid Bag weight! Please enter a valid number.")

        coin_data.append((ctype, bagw8))

        bagvalue = (float(bagw8) / coinweights[ctype]) * coinvalues[ctype]  # calculates if bagvalue is correct
        coinscorrected = (bagvalues[ctype] - bagvalue) / coinvalues[ctype]

        totalbags += 1  # adds to total amount of bags checked

        if coinscorrected == 0:  # If coinscorrected = 0 then it means bag is correct, so it will
            correctvolbags += 1  # +1 to volunteers correct bags
            totalvolbags += 1
        else:
            totalvolbags += 1

        accuracy = (correctvolbags / totalvolbags) * 100
        volunteers[volname] = [correctvolbags, totalvolbags, accuracy]

        if coinscorrected > 0:  # If value is under 0 it means you must add coins to bag
            print(f"\033[91mYou must add \033[94m{coinscorrected} \033[91mcoins to this bag.")
        elif coinscorrected < 0:  # If value is above 0 it means you must remove coins from bag
            print(f"\033[91mYou must take \033[94m{-coinscorrected} \033[91mcoins from this bag.")

    print(f"\033[91mData for \033[92m{volname} \033[91mrecorded.")

# Calculate the total value of coins for the loaded data
total_value_for_loaded_data = sum(
    [(float(bagw8) / coinweights[ctype]) * coinvalues[ctype] for vol_data in loaded_volunteers.values() for ctype, bagw8 in coin_data]
)

# Calculate the total value of coins for the new data
total_value_for_new_data = sum(
    [(float(bagw8) / coinweights[ctype]) * coinvalues[ctype] for ctype, bagw8 in coin_data]
)
# Update the total bags checked
total_bags_checked += sum([data[1] for data in loaded_volunteers.values()])
total_bags_checked += len(coin_data)

# Update the total value of coins
total_value_of_coins = total_value_of_coins + total_value_for_new_data


# Merge the new data with the existing data
for volname, data in loaded_volunteers.items():
    if volname in volunteers:
        # Update existing data with new data
        volunteers[volname][0] += data[0]
        volunteers[volname][1] += data[1]
        # Recalculate accuracy based on the updated data
        volunteers[volname][2] = (volunteers[volname][0] / volunteers[volname][1]) * 100
    else:
        # Add new data if volunteer is not in the existing data
        volunteers[volname] = data

# Save the updated data back to the file
with open(data_file, "w") as file:
    for volname, data in volunteers.items():
        file.write(f"Volunteer: {volname}\n")
        file.write(f"Correct Bags: {data[0]}\n")
        file.write(f"Total Bags: {data[1]}\n")
        file.write(f"Accuracy: {data[2]:.2f}%\n\n")
    file.write(f"Total Number of Bags Checked: {total_bags_checked}\n")
    file.write(f"Total Value of Coins: £{total_value_of_coins:.2f}\n")

desc1 = input("\033[91mDo you wish to see the totals? (Y/N): ").lower()

if desc1 == "y":
    print(f"\033[91mTotal Number of Bags Checked: \033[94m{total_bags_checked}")
    print(f"\033[91mTotal Value of Coins: £\033[94m{total_value_of_coins:.2f}")


desc2 = input("\033[91mDo you wish to display the list of volunteers sorted by accuracy? (Y/N): ").lower()

if desc2 == "y":
    display_sorted_volunteers(volunteers)
elif desc2 == "n":
    exit()

print("\033[91mData saved to CoinCount.txt.")
exit()