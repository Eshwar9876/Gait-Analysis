import os
import cv2
from tkinter import *
import ctypes,os
from tkinter.tix import *
from PIL import ImageTk, Image
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as filedialog
from time import sleep
import sys
import pickle
import mediapipe as mp
from detect import detect_pose
from tensorflow.keras.models import load_model
from pose_segmentation_mask import make_segmenation_file
from train import *

model = load_model('dataset/gait_model.h5')
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


with open(os.path.join(os.getcwd(), 'dataset', 'classes.pkl'), 'rb') as fl:
	classes_list = pickle.load(fl)
	

def HomePage():
	global cntct,about, imgmode, vdomode, detect
	try:
		cntct.destroy()
	except:
		pass
	try:
		about.destroy()
	except:
		pass
	try:
		detect.destroy()
	except:
		pass


	window = Tk()
	img = Image.open("Images\\HomePage.png")
	img = ImageTk.PhotoImage(img)
	panel = Label(window, image=img)
	panel.pack(side="top", fill="both", expand="yes")

	user32 = ctypes.windll.user32
	user32.SetProcessDPIAware()
	[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
	lt = [w, h]
	a = str(lt[0]//2-446)
	b= str(lt[1]//2-383)

	window.title("HOME - Human Gait Recognition")
	window.geometry("1214x680+"+a+"+"+b)
	window.resizable(0,0)

	def contactus():
		global cntct,about, detect
		try:
			window.destroy()
		except:
			pass
		try:
			about.destroy()
		except:
			pass
		try:
			detect.destroy()
		except:
			pass
		cntct = Tk()
		img = Image.open("Images\\AboutTeam.png")
		img = ImageTk.PhotoImage(img)
		panel = Label(cntct, image=img)
		panel.pack(side="top", fill="both", expand="yes")

		user32 = ctypes.windll.user32
		user32.SetProcessDPIAware()
		[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
		lt = [w, h]
		a = str(lt[0]//2-446)
		b= str(lt[1]//2-383)

		cntct.title("About Team - Human Gait Recognition")
		cntct.geometry("1214x680+"+a+"+"+b)
		cntct.resizable(0,0)

		homebtn = Button(cntct,text = "HomePage",font = ("Agency FB",16,"bold"),width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=HomePage)	
		homebtn.place(x=784, y = 40)
		contactusbtn = Button(cntct,text = "About Project",font = ("Agency FB",16,"bold"), width=12, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=aboutus)
		contactusbtn.place(x=909,y = 40)
		exitbtn = Button(cntct,text = "Exit",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=exit)
		exitbtn.place(x=1050,y = 40)

		cntct.mainloop()

	def aboutus():
		global about,cntct, detect
		try:
			window.destroy()
		except:
			pass
		try:
			cntct.destroy()
		except:
			pass
		try:
			detect.destroy()
		except:
			pass
		about = Tk()
		img = Image.open("Images\\AboutUs.png")
		img = ImageTk.PhotoImage(img)
		panel = Label(about, image=img)
		panel.pack(side="top", fill="both", expand="yes")

		user32 = ctypes.windll.user32
		user32.SetProcessDPIAware()
		[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
		lt = [w, h]
		a = str(lt[0]//2-446)
		b= str(lt[1]//2-383)

		about.title("About Project - Human Gait Recognition")
		about.geometry("1214x680+"+a+"+"+b)
		about.resizable(0,0)

		homebtn = Button(about,text = "HomePage",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=HomePage)	
		homebtn.place(x=800, y = 40)
		contactusbtn = Button(about,text = "About Us",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=contactus)
		contactusbtn.place(x=925,y = 40)
		exitbtn = Button(about,text = "Exit",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=exit)
		exitbtn.place(x=1050,y = 40)

		about.mainloop()

	def addperson():
		global about,cntct, detect
		try:
			window.destroy()
		except:
			pass
		try:
			cntct.destroy()
		except:
			pass
		try:
			detect.destroy()
		except:
			pass
		about = Tk()
		img = Image.open("Images\\HomePage.png")
		img = ImageTk.PhotoImage(img)
		panel = Label(about, image=img)
		panel.pack(side="top", fill="both", expand="yes")

		user32 = ctypes.windll.user32
		user32.SetProcessDPIAware()
		[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
		lt = [w, h]
		a = str(lt[0]//2-446)
		b= str(lt[1]//2-383)

		about.title("Add Person - Human Gait Recognition")
		about.geometry("1214x680+"+a+"+"+b)
		about.resizable(0,0)


		def SelectTrainFile():
			global selected_filename
			selected_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=( ("Video Files",(".mp4",".avi",".mkv")),("All Files", "*.*")))
			select_file_label.config(text = selected_filename)

		def StartTraining():
			select_file.place_forget()
			username_entry.place_forget()
			select_file_label.place_forget()
			start_training.place_forget()
			username_label.config(text="Training Started ....")

			make_segmenation_file(selected_filename, username_entry.get())
			X_train, X_valid, y_train, y_valid, classess = prepare_data()

			model = build_model(X_train.shape[1:], len(classess))
			my_callbacks = [tf.keras.callbacks.EarlyStopping(patience=2)]

			history = model.fit(X_train, y_train, validation_data = (X_valid, y_valid), batch_size = 32, epochs = 100, callbacks=my_callbacks)
			model.save('dataset/gait_model.h5')

			plot_history(history)
			HomePage()

		username_label = Label(about, text="Person Name", font = ("Agency FB",20,"bold"),relief = FLAT, fg="#0F044C", bg="#787A91")
		username_label.place(x = 129,y = 250)
		username_entry = Entry(about, font = ("Agency FB",20,"normal"), highlightthickness=2, bg="#0F044C", fg="#787A91", highlightcolor="#006EFF", selectbackground="black", width=25)
		username_entry.place(x= 250,y = 250)
	
		select_file = Button(about,text = "Select File",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=SelectTrainFile)	
		select_file.place(x=129, y = 310)

		select_file_label = Label(about, text="", font = ("Agency FB",20,"bold"),relief = FLAT, fg="#0F044C", bg="#787A91")
		select_file_label.place(x = 240,y = 310)

		start_training = Button(about,text = "Start Training",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=StartTraining)	
		start_training.place(x=250, y = 370)

		homebtn = Button(about,text = "HomePage",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=HomePage)	
		homebtn.place(x=800, y = 40)
		contactusbtn = Button(about,text = "About Us",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=contactus)
		contactusbtn.place(x=925,y = 40)
		exitbtn = Button(about,text = "Exit",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=exit)
		exitbtn.place(x=1050,y = 40)

		about.mainloop()

	# EXIT . . . 
	def exit():
		global cntct,about
		result = tkMessageBox.askquestion("Human Gait Recognition", "Are you sure you want to exit?", icon= "warning")
		if result == 'yes':
			sys.exit()

	def start_detection(filename):
		global about,cntct, detect
		try:
			window.destroy()
		except:
			pass
		try:
			cntct.destroy()
		except:
			pass

		detect = Tk()
		img = Image.open("Images\\HomePage.png")
		img = ImageTk.PhotoImage(img)
		panel = Label(detect, image=img)
		panel.pack(side="top", fill="both", expand="yes")

		user32 = ctypes.windll.user32
		user32.SetProcessDPIAware()
		[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
		lt = [w, h]
		a = str(lt[0]//2-446)
		b= str(lt[1]//2-383)

		detect.title("Detection - Human Gait Recognition")
		detect.geometry("1214x680+"+a+"+"+b)
		detect.resizable(0,0)



		imageFrame = Frame(detect, width=640, height=480, borderwidth=4, bg='black')
		imageFrame.place(x=287, y=100)

		cap = cv2.VideoCapture(filename)
		def show_frame():
			try:
				_, frame = cap.read()
				frame, detected_points = detect_pose(frame, mp_drawing, mp_drawing_styles, mp_pose, pose, model, classes_list, True)
				cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
				img = Image.fromarray(cv2image)
				imgtk = ImageTk.PhotoImage(image=img)
				display1.imgtk = imgtk
				display1.configure(image=imgtk)
				window.after(10, show_frame)
			except Exception as e:
				print(e)
		display1 = Label(imageFrame)
		display1.grid(row=1, column=0)
		

		show_frame()


		homebtn = Button(detect,text = "HomePage",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=HomePage)	
		homebtn.place(x=800, y = 40)
		contactusbtn = Button(detect,text = "About Us",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=contactus)
		contactusbtn.place(x=925,y = 40)
		exitbtn = Button(detect,text = "Exit",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=exit)
		exitbtn.place(x=1050,y = 40)

		detect.mainloop()

	def StreamMode():
		start_detection(0)

	def VideoMode():
		filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=( ("Video Files",(".mp4",".avi",".mkv")),("All Files", "*.*")))
		start_detection(filename)



	''' MENU BAR '''             
	
	addpersonbtn = Button(window,text = "Add Person",font = ("Agency FB",16,"bold"), width=12, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=addperson)	
	addpersonbtn.place(x=643, y = 40)
	
	aboutusbtn = Button(window,text = "About Project",font = ("Agency FB",16,"bold"), width=12, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=aboutus)	
	aboutusbtn.place(x=784, y = 40)
	contactusbtn = Button(window,text = "About Us",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=contactus)
	contactusbtn.place(x=925,y = 40)
	exitbtn = Button(window,text = "Exit",font = ("Agency FB",16,"bold"), width=10, relief = FLAT, bd = 0, borderwidth='0',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=exit)
	exitbtn.place(x=1050,y = 40)

	videobtn = Button(window,text = "FROM VIDEO",font = ("Arial Narrow",18,"bold"),width = 20,relief = FLAT, bd = 1, borderwidth='1',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=VideoMode)
	videobtn.place(x=225,y = 250)
	livestream = Button(window,text = "LIVE STREAM",font = ("Arial Narrow",18,"bold"),width = 20,relief = FLAT, bd = 1, borderwidth='1',bg="#787A91",fg="#0F044C",activebackground = "#EEEEEE",activeforeground = "#141E61",command=StreamMode)
	livestream.place(x=225,y = 450)

	window.mainloop()

#HomePage()
def LoadingScreen():
	root = Tk()
	root.config(bg="white")
	root.title("Loading - Human Gait Recognition")

	img = Image.open(r"Images\\Loading.png")
	img = ImageTk.PhotoImage(img)
	panel = Label(root, image=img)
	panel.pack(side="top", fill="both", expand="yes")

	user32 = ctypes.windll.user32
	user32.SetProcessDPIAware()
	[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
	lt = [w, h]
	a = str(lt[0]//2-446)
	b= str(lt[1]//2-383)

	root.geometry("1214x680+"+a+"+"+b)
	root.resizable(0,0)

	for i in range(40):
		Label(root, bg="#EEEEEE",width=2,height=1).place(x=(i+4)*25,y=600) 

	def play_animation(): 
		for j in range(40):
			Label(root, bg= "#141E61",width=2,height=1).place(x=(j+4)*25,y=600) 
			sleep(0.07)
			root.update_idletasks()
		else:
			root.destroy()
			HomePage()

	root.update()
	play_animation()
	root.mainloop()
	
# LoadingScreen()

HomePage()