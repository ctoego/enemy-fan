Попытка написать на английском.

##### System management the data in directory 'data'.

###### File:

/data/

|	|—data.py			//management data in the game

|	|—savegame.json		//keep the  player's progress

|	|—config.toml			/ / stores configuration data; causes an error and stops if missing

|	|—setting.json		/ / stores  setting data, if missing causes a reset progress



This management class Data. 



##### UI

/game\_ui/

|	|−level.py	//managment surface this a level button

|	|−menu.py	//my widget(button) for a game

|	|−option.py	//loading image

|	|−set.py		//manages surface for this widget for setting

!! In level.py and set.py, widget dont't draw on the local surface, draw on main surface. Pygame\_gui watches collision based main coordinates but draw local surface x and y.	!!

&nbsp;

