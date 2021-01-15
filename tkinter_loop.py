# USAGE
# tkinter_test.py

# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog as tkFileDialog
import cv2
from google.cloud import vision

def invert_image(image, name):
	image = (255-image)
	cv2.imwrite(name, image)
	return image

def print_image_text(image):
	import pytesseract
	print(pytesseract.image_to_string(image, lang='eng'))

def annotate_google(image):
	client = vision.ImageAnnotatorClient()
	response = client.face_detection

def select_image():
	# grab a reference to the image panels
	global panelA, panelB

	# open a file chooser dialog and allow the user to select an input
	# image
	path = tkFileDialog.askopenfilename()

	# ensure a file path was selected
	if len(path) > 0:
		# load the image from disk, convert it to grayscale, and detect
		# edges in it
		image = cv2.imread(path)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		cv2.imwrite("gray.tif", gray)
		high_thresh, thresh_im = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		low_thresh = 0.5 * high_thresh
		edged = cv2.Canny(gray, 100, 350)
		print_image_text(edged)
		edged = invert_image(edged, "edged.tif")
		print_image_text(edged)
		print_image_text(gray)

		# OpenCV represents images in BGR order; however PIL represents
		# images in RGB order, so we need to swap the channels
		color = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# convert the images to PIL format...
		color = Image.fromarray(color)
		edged = Image.fromarray(edged)

		# ...and then to ImageTk format
		color = ImageTk.PhotoImage(color)
		edged = ImageTk.PhotoImage(edged)

		# if the panels are None, initialize them
		if panelA is None or panelB is None:
			# the first panel will store our original image
			panelA = Label(image=color)
			panelA.image = color
			panelA.pack(side="left", padx=10, pady=10)

			# while the second panel will store the edge map
			panelB = Label(image=edged)
			panelB.image = edged
			panelB.pack(side="right", padx=10, pady=10)

		# otherwise, update the image panels
		else:
			# update the pannels
			panelA.configure(image=image)
			panelB.configure(image=edged)
			panelA.image = color
			panelB.image = edged

# initialize the window toolkit along with the two image panels
root = Tk()
panelA = None
panelB = None

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

# kick off the GUI
root.mainloop()
