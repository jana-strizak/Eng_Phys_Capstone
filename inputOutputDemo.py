exec(open('HandyPantry_allfunctions.py').read())

#first delete everything currently in all the json files
for loc in location_db.all():
	location_db.remove(doc_ids = [loc.doc_id])

for item in food_db.all():
	food_db.remove(doc_ids = [item.doc_id])

for record in history_db.all():
	history_db.remove(doc_ids = [record.doc_id])

for item in favorites_db.all():
	favorites_db.remove(doc_ids = [item.doc_id])
	
#making the location spots to store items
make_location(10)
make_location(20)
make_location(5)
make_location(25)


#intro
print('Welcome to the Handy Pantry autonomous storage unit. This tutorial will show you how this python code works to keep track of the food items stored, locations and their availabiliy, the history of items inputed, and your favorite items ')
input('\n Press enter to continue...')

#see everything in the files

print('\n First let\'s see what info is stored in all the json files:')

def print_all_file_content(): #this function shows all the info in the 4 json files in the command window
	input('\n Press enter to see all the location spots. Notice how the closer locations fill up first...')
	print('\n The location spots are:')
	print(location_db.all()) #see everything in location file

	input('\n Press enter to see all the food items...')
	print('\n The food items currently stored are:')
	print(food_db.all())

	input('\n Press enter to see the history...')
	print('\n The items used in the past month are:')
	print(history_db.all())

	input('\n Press enter to continue see the favorite items...')
	print('\n The favorite items are:')
	print(favorites_db.all())

print_all_file_content() #executing function to show what's the state of the json files

#Showing item input
input('\n Lets input an apple into the Handy Pantry\n Press enter to input the item...')
complete_input_item(fooditem1) #function to completely input an item into all the files

input('\n Let\'s check that all our files have updated with the new item\'s information\n Press enter to see all the files...')
print_all_file_content()

#showing how expiry date works by inputing item that is almost expired
input('\n Lets input another item that expires tomorrow. We will put in black beans.\n Press enter to input the item...')

#set new item parameters
fooditem1.name = 'black beans'
fooditem1.foodGrp = 'beans'
fooditem1.templateNum = 1
newDate = date.today() + datetime.timedelta(days=1)
fooditem1.setExpiry(newDate.year,newDate.month,newDate.day)

complete_input_item(fooditem1) #function to completely input an item into all the files

#input('\n Let\'s check that all our files have updated with the new item\'s information\n Press enter to see all the files...')
#print_all_file_content()

input('\n Let\'s run the daily check function and see if it reminds us of the upcoming expiry date\n Press enter to continue...')
daily_check()

#showing message that is sent if item is already old
input('\n Now let\'s put in an item that expired yesterday. We will put in old Chickpeas. \n Press enter to input the item...')

#set new item parameters
fooditem1.name = 'Chickpeas'
fooditem1.foodGrp = 'beans'
fooditem1.templateNum = 1
newDate = date.today() - datetime.timedelta(days=1)
fooditem1.setExpiry(newDate.year,newDate.month,newDate.day)

complete_input_item(fooditem1) #function to completely input an item into all the files

#input('\n Let\'s check that all our files have updated with the new item\'s information\n Press enter to see all the files...')
#print_all_file_content()

input('\n Let\'s run the daily check function and see if it reminds us of the upcoming expiry date\n Press enter to continue...')
daily_check()


#showing output of multiple items 
input('\n Let\'s take out all the items to see how Handy Pantry saves time by taking out the closest items first so the user can start cooking. \n Press enter to continue...')

complete_output_item([1,2,3])


#showing favorite item 
input('\n Let\'s input the same item multiple times to see if Handy Pantry will mark it as a favorite item. \n Press enter to continue...')
complete_input_item(fooditem1)
input('\n press enter to input it again...')
complete_input_item(fooditem1)
# input('\n press enter to input it again...')
# complete_input_item(fooditem1)
# input('\n press enter to input it again...')
# complete_input_item(fooditem1)

input('\n Look at that, it\'s a favorite! Press enter see if the favorite file was updated...')
print(favorites_db.all())


#removing the item
input('\n Now that it is a favorite, we will remove it and see what happens. Press enter to remove the apple...')
complete_output_item(4)

input('\n Now let\'s take the last one out. Press enter to remove the apple...')
complete_output_item(5)


#filling up all the spaces
input('\n Now let\'s keep putting stuff in until the pantry is full. Press enter to input the apple...')
complete_input_item(fooditem1)

input('\n press enter to input it again...')
complete_input_item(fooditem1)

input('\n press enter to input it again...')
complete_input_item(fooditem1)

input('\n press enter to input it again...')
complete_input_item(fooditem1)

input('\n press enter to input it again...')
complete_input_item(fooditem1)

print('That\'s all for now!')