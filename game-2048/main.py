from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
import numpy as np
from functions import move_labels

colors = {"2": (1,1,1,1), "4": (.9,.9,.1,1), "8": (.9,.6,.1,1), "16": (.9,.3,.1,1),
          "32": (.9,.0,.1,1), "64": (.6,.9,.1,1), "128": (.3,.9,.1,1), "256": (.0,.9,.1,1),
          "512": (.1,.6,.9,1), "1024": (.1,.3,.9,1), "2048": (.1,.0,.9,1)}

class MyLayout(FloatLayout):

	def text_appeared(self, widget):
		anim = Animation(color=[.9,.6,.3,.1], duration=0.025)
		anim += Animation(color=[.9,.6,.3,.05], duration=0.025) 
		anim += Animation(color=[1,1,1,1], duration=0.025) 
		anim.start(widget)

	def text_changed(self, widget):
		anim = Animation(font_size=44, duration=.025)
		anim += Animation(font_size=58, duration=.025) 
		anim += Animation(font_size=44, duration=.025)
		anim.start(widget)

	def freeze_buttons(self):
		self.ids.up.disabled = True
		self.ids.down.disabled = True  
		self.ids.left.disabled = True  
		self.ids.right.disabled = True

	def is_movable(self):
		for i in range(4):
			for j in range(3):
				btn1 = self.ids.get('button'+str(i)+str(j))
				btn2 = self.ids.get('button'+str(i)+str(j+1))
				if btn1.text == btn2.text:
					return True
		for i in range(3):
			for j in range(4):
				btn1 = self.ids.get('button'+str(i)+str(j))
				btn2 = self.ids.get('button'+str(i+1)+str(j))
				if btn1.text == btn2.text:
					return True 
		return False

	def start_button_pressed(self):
		self.ids.endgame.text = ""
		self.ids.score.text = "0"
		self.ids.up.disabled = False
		self.ids.down.disabled = False  
		self.ids.left.disabled = False  
		self.ids.right.disabled = False
		for i in range(4):
			for j in range(4):
				self.ids.get('button'+str(i)+str(j)).text = ""
		i_, j_ = np.random.randint(4,size=(2))
		btn = self.ids.get('button'+str(i_)+str(j_))
		btn.text = "2"
		btn.color = colors["2"]
		self.text_appeared(btn)


	def left_button_pressed(self):
		total_mask = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
		total_list = []
		for i in range(4):
			list_ = []
			for j in range(4):
				btn = self.ids.get('button'+str(i)+str(j))
				if btn.text != "":
					list_.append(btn.text)
			new_list = move_labels(list_, True)
			for j in range(4):
				self.ids.get('button'+str(i)+str(j)).text = new_list[j]
			total_list.append(new_list)

		for i in range(4):
			for j in range(3):
				if total_list[i][j] == total_list[i][j+1] and total_list[i][j] != "" and total_list[i][j+1] != "":
					total_list[i][j] = str(2*int(total_list[i][j]))
					total_mask[i][j] = 1
					self.ids.score.text = str(int(total_list[i][j]) + int(self.ids.score.text)) 
					for k in range(j+1,3):
						total_list[i][k] = total_list[i][k+1]
					total_list[i][3] = ""

		for i in range(4):
			for j in range(4):
				btn = self.ids.get('button'+str(i)+str(j))
				btn.text = total_list[i][j]
				if total_list[i][j] != "":
					btn.color = colors[total_list[i][j]]
				if total_mask[i][j] == 1:
					self.text_changed(btn)


		is_empty = np.argwhere(np.array(total_list) == "")
		shape = is_empty.shape[0]
		if shape != 0:
			i_, j_ = is_empty[np.random.randint(shape)]
			btn = self.ids.get('button'+str(i_)+str(j_))
			btn.color = colors["2"]
			btn.text = "2"
			self.text_appeared(btn)
			shape -= 1
		if shape == 0 and self.is_movable() == False:
			self.ids.endgame.text = "Game Over!"
			self.freeze_buttons()

		if "2048" in sum(total_list, []):
			self.ids.endgame.text = "You Won!"
			self.freeze_buttons()
	
	def right_button_pressed(self):	
		total_mask = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
		total_list = []
		for i in range(4):
			list_ = []
			for j in range(4):
				btn = self.ids.get('button'+str(i)+str(j))
				if btn.text != "":
					list_.append(btn.text)
			new_list = move_labels(list_, False)
			for j in range(4):
				self.ids.get('button'+str(i)+str(j)).text = new_list[j]
			total_list.append(new_list)

		for i in range(4):
			for j in range(3,0,-1):
				if total_list[i][j-1] == total_list[i][j] and total_list[i][j-1] != "" and total_list[i][j] != "":
					total_list[i][j] = str(2*int(total_list[i][j]))
					total_mask[i][j] = 1
					self.ids.score.text = str(int(total_list[i][j]) + int(self.ids.score.text)) 
					for k in range(j-1,0,-1):
						total_list[i][k] = total_list[i][k-1]
					total_list[i][0] = ""

		for i in range(4):
			for j in range(4):
				btn = self.ids.get('button'+str(i)+str(j))
				btn.text = total_list[i][j]
				if total_list[i][j] != "":
					btn.color = colors[total_list[i][j]]
				if total_mask[i][j] == 1:
					self.text_changed(btn)

		is_empty = np.argwhere(np.array(total_list) == "")
		shape = is_empty.shape[0]
		if shape != 0:
			i_, j_ = is_empty[np.random.randint(shape)]
			btn = self.ids.get('button'+str(i_)+str(j_))
			btn.color = colors["2"]
			btn.text = "2"
			self.text_appeared(btn)
			shape -= 1
		if shape == 0 and self.is_movable() == False:
			self.ids.endgame.text = "Game Over!"
			self.freeze_buttons()

		if "2048" in sum(total_list, []):
			self.ids.endgame.text = "You Won!"
			self.freeze_buttons()


	def up_button_pressed(self):
		total_mask = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
		total_list = []
		for j in range(4):
			list_ = []
			for i in range(4):
				btn = self.ids.get('button'+str(i)+str(j))
				if btn.text != "":
					list_.append(btn.text)
			new_list = move_labels(list_, True)
			for i in range(4):
				self.ids.get('button'+str(i)+str(j)).text = new_list[i]
			total_list.append(new_list)

		for j in range(4):
			for i in range(3):
				if total_list[j][i] == total_list[j][i+1] and total_list[j][i] != "" and total_list[j][i+1] != "":
					total_list[j][i] = str(2*int(total_list[j][i]))
					total_mask[j][i] = 1
					self.ids.score.text = str(int(total_list[j][i]) + int(self.ids.score.text)) 
					for k in range(i+1,3):
						total_list[j][k] = total_list[j][k+1]
					total_list[j][3] = ""

		for j in range(4):
			for i in range(4):
				btn = self.ids.get('button'+str(i)+str(j))
				btn.text = total_list[j][i]
				if total_list[j][i] != "":
					btn.color = colors[total_list[j][i]]
				if total_mask[j][i] == 1:
					self.text_changed(btn)


		is_empty = np.argwhere(np.array(total_list) == "")
		shape = is_empty.shape[0]
		if shape != 0:
			j_, i_ = is_empty[np.random.randint(shape)]
			btn = self.ids.get('button'+str(i_)+str(j_))
			btn.color = colors["2"]
			btn.text = "2"
			self.text_appeared(btn)
			shape -= 1
		if shape == 0 and self.is_movable() == False:
			self.ids.endgame.text = "Game Over!"
			self.freeze_buttons()

		if "2048" in sum(total_list, []):
			self.ids.endgame.text = "You Won!"
			self.freeze_buttons()

	def down_button_pressed(self):	
		total_mask = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
		total_list = []
		for j in range(4):
			list_ = []
			for i in range(4):
				btn = self.ids.get('button'+str(i)+str(j))
				if btn.text != "":
					list_.append(btn.text)
			new_list = move_labels(list_, False)
			for i in range(4):
				self.ids.get('button'+str(i)+str(j)).text = new_list[i]
			total_list.append(new_list)

		for j in range(4):
			for i in range(3,0,-1):
				if total_list[j][i-1] == total_list[j][i] and total_list[j][i-1] != "" and total_list[j][i] != "":
					total_list[j][i] = str(2*int(total_list[j][i]))
					total_mask[j][i] = 1
					self.ids.score.text = str(int(total_list[j][i]) + int(self.ids.score.text)) 
					for k in range(i-1,0,-1):
						total_list[j][k] = total_list[j][k-1]
					total_list[j][0] = ""

		for j in range(4):
			for i in range(4):
				btn = self.ids.get('button'+str(i)+str(j))
				btn.text = total_list[j][i]
				if total_list[j][i] != "":
					btn.color = colors[total_list[j][i]]
				if total_mask[j][i] == 1:
					self.text_changed(btn)
		
		is_empty = np.argwhere(np.array(total_list) == "")
		shape = is_empty.shape[0]
		if shape != 0:
			j_, i_ = is_empty[np.random.randint(shape)]
			btn = self.ids.get('button'+str(i_)+str(j_))
			btn.color = colors["2"]
			btn.text = "2"
			self.text_appeared(btn)
			shape -= 1
		if shape == 0 and self.is_movable() == False:
			self.ids.endgame.text = "Game Over!"
			self.freeze_buttons()

		if "2048" in sum(total_list, []):
			self.ids.endgame.text = "You Won!"
			self.freeze_buttons()


class MainApp(MDApp):
	def build(self):
		return MyLayout()

app = MainApp()
app.run()