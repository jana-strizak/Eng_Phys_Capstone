#tinydb file to take in a food item and store it 
import datetime
import tinydb 
from math import floor
import operator
import datetime
from threading import Timer
exec(open('foodItem_class.py').read())

#making a fake food item which will be recieved from UI
fooditem1 = foodItem()
fooditem1.name = 'Apple'
fooditem1.foodGrp = 'fruit'
fooditem1.setExpiry(2022,2,4)
fooditem1.templateNum = 3
fooditem1.image = 'picture 1'

#creating the templates class which serves as a guide to storing items so they don't need to be created multiple times
class template:
	def __init__(self,foodobject):
		self.number = foodobject.templateNum
		self.name = foodobject.name
		self.foodGrp = foodobject.foodGrp
		self.image = foodobject.image



# import os

# if os.path.exists('location_data.json'):
#     os.remove('location_data.json')
# else:
#     print("Can not delete the file as it doesn't exists")


food_db = TinyDB('food_data.json') #making a file which will contain the food info
location_db = TinyDB('location_data.json') #making a file which will contain the location info
#/
#/
#/
#/
#/
#/
#/
#/
#/
#//////////****** Favorite food function ********//////////
#/ this function will store any food items which are frequently used and will tell
#the user when they are running low on this item 

history_db = TinyDB('history_data.json')
favorites_db = TinyDB('favorites_data.json')

#need to make location file to manage objects and locations
def make_location(distance):
	location_db.insert({'distance':distance,'item_stored': None})
	return 

#this function finds the favorite templates from any file (eg.favorites_db)
def get_templates(database_db):
	templates = []
	for i in database_db.all():
		templates.append(i.get('template_num'))
	return templates

#This functions searches to see if a template is already marked as favorite and update the favorites field of the item
def check_if_favorite(item_template,food_db_id, fav_db_id): #NEEDS TO BE CHECKED
	favorites = get_templates(favorites_db) #get list of favorite templates
	if item_template in favorites: #only update the favorites section of favorite templates
		food_db.update({'favorite': 1}, doc_ids=[food_db_id]) #update favorties field in food database
		history_db.update({'favorite': 1}, doc_ids=[fav_db_id]) #update favorites field in favorites database
	else: #the field should still be updated for trouble shooting to make sure it is working 
		food_db.update({'favorite': 0}, doc_ids=[food_db_id])
		history_db.update({'favorite': 0}, doc_ids=[fav_db_id])
	return



#this function will store the template, time, and item_id of an inputted item into the 
#history database
def store_template(item_id):
	template = food_db.get(doc_id = item_id)['template_num']
	in_date = food_db.get(doc_id = item_id)['date_inputted']
	
	new_history_db_id = history_db.insert({'template_num': template,'date_inputted': in_date,'favorite':None})
	check_if_favorite(template, item_id, new_history_db_id) #checking to see if it is favorite and updating favorites field
	return 


#this function counts the number of repeated templates
def total_templates(anything_db):
	aviable_inventory = []
	checked_templates = []

	for item in anything_db: #iterate through all stored items
		if item['template_num'] not in checked_templates: #if there is a template number, then there is repeats of same item
			template = item['template_num']
			checked_templates.append(item['template_num'])

			food = Query()
			repeats = anything_db.search(food.template_num == template) #search through all the repeats 
			
			aviable_inventory.append([template, len(repeats)]) #adding the item id of closest expiry date and it's quantity

	return aviable_inventory



#This function will make this template a new favortie 
def update_db_for_fav(template):

	for item in history_db: #need to check each item in history db
		if item['template_num'] == template: #if the templates match
			history_db.update({'favorite': 1}, doc_ids=[item.doc_id]) #change the item to a favorite
	for item in food_db: #need to check each item in food db
		if item['template_num'] == template: #if the templates match
			food_db.update({'favorite': 1}, doc_ids=[item.doc_id]) #change the item to a favorite
	return 
#a separation to the function above that makes a bran new item in fav database
def new_favorite(template):
	new_favorites_db_id = favorites_db.insert({'template_num': template}) #input template into favorites_db
	update_db_for_fav(template) #update all fields 
	return 


#this function will be executed daily to check for items with repeated
#templates and make them as favorite items
def check_for_favorites():
	templates_in_history_db = total_templates(history_db)
	templates_in_favorites_db = get_templates(favorites_db)
	for i in templates_in_history_db:
		template = i[0] 
		repeats = i[1]

		if (repeats >= 4) & (template not in templates_in_favorites_db) :
			#this template should be made a favorite
			answer = input('Would you like to make this template a favorite? Type Y/N: ') 
			if (answer == 'Y') or (answer == 'y'):
				print('Item will be made a favorite')
				new_favorite(template)
			else:
				print('ok, item will not be made a favorite')

		if template in templates_in_favorites_db:
			update_db_for_fav(template)
	return 


#this function will delete old item data which did not meet favorites for the week
def history_db_cleanse():
	for item in history_db.all():
		in_date = make_date(item['date_inputted'])
		time_elapsed = in_date - date.today()
		
		if (item['favorite']==0) and (time_elapsed < -datetime.timedelta(days=7)): #only want to delete items what have been stored for more than 7 days
			history_db.remove(doc_ids = [item.doc_id])
		if (item['favorite']==1) and (time_elapsed < -datetime.timedelta(weeks=4)): #only want to delete items what have been stored for more than 1 month
			history_db.remove(doc_ids = [item.doc_id])
	return 


#function to count through food_db favorites and see how many favorites we have left. 
def check_favorites_inventory(): #this will output all the favorite templates and the quantity of them in the food_db
	favorites_list = []
	for item in food_db.all():
		if item['favorite'] ==1:
			template = item['template_num'] 
			food = Query()
			repeats = food_db.search(food.template_num == template)

			favorites_list.append([template,len(repeats)])
	return favorites_list


#this function sends a notification when the favorite item is running low 
def send_low_on_favorites_msg(template):
	food = Query()
	msg = "You have one template " + str(food_db.search(food.template_num == template)[0]['template_num']) + " left"
	return print(msg)

#this function send notification when favorite item is empty
def send_empty_on_favorites_msg(template):
	food = Query()
	msg = "You don't have any template " + str(history_db.search(food.template_num == template)[0]['template_num']) + " left"
	return print(msg)


#this function will determine what message needs to be sent
def Assign_favorites_msg():
	stored_favs = check_favorites_inventory() #fav items stored
	stored_favs_template = []
	all_favs = get_templates(favorites_db)
	different = []
	
	for i in stored_favs: #for loop makes the list of all templates currently in storage
		stored_favs_template.append(i[0])

	for template in all_favs: #seperate templates which aren't in storage but are listed as a fav
		if template not in stored_favs_template:
			different.append(template) 

	for i in stored_favs:
		template = i[0]
		quantity = i[1]
		if quantity == 1:
			send_low_on_favorites_msg(template)
			
	for template in different:
		send_empty_on_favorites_msg(template)
	return 



#this function will remove an item which has been marked as a favorite but has not been used for a long time 
#this will be exicuted daily 
def favorites_db_cleanse():
	favorite_templates = get_templates(favorites_db)
	history_templates = get_templates(history_db)

	for template in favorite_templates:
		if template not in history_templates:
			#fav template is not in history so needs to be removed as a favorite bc hasn't been used for a month
			item = Query()
			favorites_db.remove(item.template_num == template) #removed from favorites_db
			food_db.update({'favorite': 0}, doc_ids=[item.doc_id]) #also needs to not be marked as a favorite

	return 

def check_old_items():
	for item in food_db.all():
		exp_date = make_date(item['expiry_date'])
		#print(exp_date)
		time_elapsed = date.today() - exp_date
		#print(time_elapsed)

		if (time_elapsed > datetime.timedelta(days=0)): #if time elapsed is positive, it is already expired
			msg = item['name']+' is '+ str(time_elapsed.days) + ' days old'
			print(msg)
		elif time_elapsed == datetime.timedelta(days=0): #today it expires
			msg = item['name']+' expires today'
			print(msg)
		elif (time_elapsed > datetime.timedelta(days=-7)) and (time_elapsed < datetime.timedelta(days=0)): #if time elapsed is neg, it still has time
			msg = item['name']+' will expire in '+ str(abs(time_elapsed.days))+' days'
			print(msg)

	

		
#this function will be run daily and it refreshed the history_db, refreshes the favorites_db,
# checks the favorite items inventory, and sends a message to the UI if we are low, checks for old items and sends a notification
def daily_check():
	history_db_cleanse() #refreshes history_db
	favorites_db_cleanse() #refresh the favorites_db
	check_for_favorites() #checks to see if an item can be made a favorite
	Assign_favorites_msg()#send UI message if we are running low on favorite items
	check_old_items() #sends message if an item is getting old
	return print('history and favorites have been updated, messages have been sent')

#/
#/
#/
#/
#/
#/
#/
#/
#/
#/
#/
#/
#/
#/
#/
#///////////************ INPUTTING ITEM ***********//////////////

#function to store the info from the foodItem object to a database made above 
def store_in_db(fooditem):
	#converting indate and expiry date to a list of numbers 
	date_inputted = [int(fooditem.inDate.strftime("%Y")),int(fooditem.inDate.strftime("%m")),int(fooditem.inDate.strftime("%d"))]
	date_expiry = [int(fooditem.expDate.strftime("%Y")),int(fooditem.expDate.strftime("%m")),int(fooditem.expDate.strftime("%d"))]

	template = fooditem.templateNum
	#store in food_db:
	new_food_id = food_db.insert({'name': fooditem.name,'food_group':fooditem.foodGrp,'image': fooditem.img,'date_inputted':date_inputted,'expiry_date': date_expiry,'template_num':template,'location': None, 'favorite':None})
	
	store_template(new_food_id) #stores the template in the favorites database and updates food_db if it is a favorite

	return new_food_id
 

#function to reassemble the date from the db to an actual datetime object
def make_date(date_list_from_db):
	#assemble the individual year month and day
	inDate_year = date_list_from_db[0]
	inDate_month = date_list_from_db[1]
	inDate_day = date_list_from_db[2]

	date1 = date(inDate_year,inDate_month,inDate_day) #make into actual date
	return date1


#item_from_db1 = food_db.all()[2] #some item from db to test the next function


#function to reassemble the foodItem object when outputting info to the UI
def make_object_foodItem(item_id_from_db):
	fooditem_object= foodItem() #making it into the foodItem class for the UI
	
	fooditem_object.name = food_db.get(doc_id = item_id_from_db)['name']
	fooditem_object.foodGrp = food_db.get(doc_id = item_id_from_db)['food_group']
	fooditem_object.img = food_db.get(doc_id = item_id_from_db)['image']
	#input date must be resembled
	fooditem_object.inDate = make_date(food_db.get(doc_id = item_id_from_db)['date_inputted'])
	fooditem_object.expDate = make_date(food_db.get(doc_id = item_id_from_db)['expiry_date'])
	fooditem_object.templateNum = food_db.get(doc_id = item_id_from_db)['template_num']

	return fooditem_object #returns reassembled object from db entry 




#function to find closest available location
def closest_location():
	#first get all locations that are empty
	empty_location = Query()
	empty_loc_list = location_db.search(empty_location.item_stored == None)

	distance_list = [] 
	for location in empty_loc_list:
		distance_list.append([location['distance'],location.doc_id]) #make list of distances for empty locations [distance,id]
	
	min_distance = min(distance_list)

	#search location_db for the closest location 
	closest_loc = min_distance[1]
	return  closest_loc



#function to move to certain location
def move_to_location(location_id):
	return print('input item to location '+str(location_id))

#questions for mechanical bois:
# how will we differentiate storing item from taking out item from location

#function to sort item to location 
def store_in_location(item_id_from_db):
	#assign closest location to it 
	location_assigned = closest_location()
	
	food_db.update({'location': location_assigned}, doc_ids=[item_id_from_db])
	location_db.update({'item_stored': item_id_from_db}, doc_ids=[location_assigned])
	move_to_location(location_assigned)
	return location_assigned

#//////***** Grand input function *****//////
#the follow function is the complete inputting an item function that combines
#all the above functions to store the object in the location and db
def complete_input_item(foodItem_object_from_UI):
	try:
		test = closest_location()
	except ValueError:
		return print('There are no more storage spots left')

	new_items_id = store_in_db(foodItem_object_from_UI)
	store_in_location(new_items_id)
	check_for_favorites()
	return

#/
#/
#/
#/
#/
#/
#////** OUTPUTTING THE ITEM FROM STORAGE **//////
#give UI a list of avaible items to remove (ignoring repeats)
#tell motors to move to location to output object 
#update food and location database to not contain the item

#function which takes in a list of items from food_db and fines the min value of one catagory 
def find_closest_expiry(list_of_same_template): #catagory_of_item must be an actual catagroy in the item's dictionary ex:'name'
	date_list = []
	for item in list_of_same_template: #extracting date from the items
		date_list.append([make_date(item['expiry_date']),item.doc_id])

	date_list.sort(key=operator.itemgetter(0)) #sorting by date

	return date_list[0][1] #returns the id of the item with closest date 

	

#this function outputs a list of all food items stored in db for the UI
#to let the user decide which they want to select
#Output is in the format [foodItem object , quantity, item id]
def make_UI_inventory():
	aviable_inventory = []
	checked_templates = []

	for item in food_db: #iterate through all stored items
		if item['template_num']!=None and item['template_num'] not in checked_templates: #if there is a template number, then there is repeats of same item
			template = item['template_num']
			checked_templates.append(item['template_num'])

			food = Query()
			repeats = food_db.search(food.template_num == template) #search through all the repeats 
			itemid_w_closest_expiry = find_closest_expiry(repeats) #use function to get only the min expiry date of all the repeats 
			
			aviable_inventory.append([make_object_foodItem(itemid_w_closest_expiry),len(repeats),itemid_w_closest_expiry]) #adding the item id of closest expiry date and it's quantity

		elif item['template_num']==None: #if there is no other item like this, we simply add this item to the inventory
			aviable_inventory.append([make_object_foodItem(item.doc_id),1,item.doc_id])

	return aviable_inventory



#this function outputs a number which represents the total number of items stored in the food_db at the moment
#The purpose of this is to make it easier for the UI to number of items stored in the HP 
def make_UI_quantity():
	quantity_stored = []
	checked_templates = []

	for item in food_db: #iterate through all stored items
		if item['template_num']!=None and item['template_num'] not in checked_templates: #if there is a template number, then there is repeats of same item
			template = item['template_num']
			checked_templates.append(item['template_num'])

			food = Query()
			repeats = food_db.search(food.template_num == template) #search through all the repeats 
			
			quantity_stored.append(len(repeats)) #adding the item id of closest expiry date and it's quantity

		elif item['template_num']==None: #if there is no other item like this, we simply add this item to the inventory
			quantity_stored.append(1)

	return sum(quantity_stored)


#this function tells motors to remove item from certain location
def remove_from_location(location_id):
	#send signal to motors to get object from certain location 
	print('remove item from location '+str(location_id))
	print([location_id, 0])
	return 

#this function takes in a food item given by UI and removes it from 
#location and food db, as well as telling the motors to remove it
def output_item(item_id_from_UI):
	location_id = food_db.get(doc_id = item_id_from_UI)['location']
	remove_from_location(location_id) #tell motors to remove item 
	location_db.update({'item_stored': None}, doc_ids=[location_id]) #delete item from location
	return

#function to delete item profile after item has been sucessfully removed
def delete_item(location_id):
	item = Query()
	food_db.remove(item.location==location_id)
	return 'item has been deleted'

#///* Grand Removal Function *///
def single_output_item(item_id_from_UI):
	try: 
		output_item(item_id_from_UI)
		#wait for confirmation from motors 
		location_id = food_db.get(doc_id = item_id_from_UI)['location']
		delete_item(location_id)
		Assign_favorites_msg()#send UI message if we are running low on favorite items
	except TypeError:
		print('This item is not in the Handy Pantry')
	return 

#/
#/
#/
#///////////**** Multiple item retrival ******////////

#this function will sort the location of items into accending order
def find_closest_location(list_of_item_ids_from_UI): #catagory_of_item must be an actual catagroy in the item's dictionary ex:'name'
	location_list = []
	for item_id in list_of_item_ids_from_UI: #extracting date from the items
		location = food_db.get(doc_id = item_id)['location'] #getting location of stored object 
		location_distance = location_db.get(doc_id = location)['distance']#getting distance of the location of stored object 
		location_list.append([location, location_distance, item_id])

	location_list.sort(key=operator.itemgetter(1)) #sorting by distance

	return location_list #returns the id of the item with closest date 


#this function will take in a list of multple items to be outputted and it will 
#output them in order of shortest distance location to largest
def output_multiple(list_of_item_ids_from_UI):
	location_list = find_closest_location(list_of_item_ids_from_UI)
	for item in location_list:
		#print(item[2]) #printing item id in food_db 
		complete_output_item(item[2])

	return 

def complete_output_item(id_from_UI):
	if type(id_from_UI) == int:
		single_output_item(id_from_UI)
	elif isinstance(id_from_UI,list):
		print('multiple items selected')
		output_multiple(id_from_UI)
	return 


