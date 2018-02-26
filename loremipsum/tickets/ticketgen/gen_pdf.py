from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import PIL
import datetime
import os 


from tickets import models

def gen_pdf_from_tx(tx):
	_event = tx.event
	_parent = tx.parent
	event_date = _event.event_date.strftime("%Y-%m-%d %H:%M:%S")
	parent_name = _parent.full_name
	purchase_date = tx.date.strftime("%Y-%m-%d %H:%M:%S")
	amount = tx.amount
	cost = tx.total_cost
	location = _event.location
	provider = _event.provider.full_name


	#pdfmetrics.registerFont(TTFont('DroidSerif', '/code/DroidSerif-Regular.ttf'))
	pdfmetrics.registerFont(TTFont('DroidSerif', '/code/loremipsum/tickets/ticketgen/DroidSerif-Regular.ttf'))

	pdfmetrics.registerFont(TTFont('DroidSerifBd', '/code/loremipsum/tickets/ticketgen/DroidSerif-Bold.ttf'))
	#pdfmetrics.registerFont(TTFont('DroidSerifIt', fontPath('DroidSerif-Italic.ttf')))
	#pdfmetrics.registerFont(TTFont('DroidSerifBI', fontPath('DroidSerif-BoldItalic.ttf')))




	 
	c = canvas.Canvas("/code/loremipsum/tickets/ticketgen/receipt.pdf", pagesize=A4)
	c.setFont('DroidSerif',14)
	c.drawImage('/code/loremipsum/tickets/ticketgen/loremipsum_lrg.jpg', 0, 0, 325, 100)
	c.drawString(20,750,"Ευχαριστούμε που επιλέξατε τη LoremIpsum για την επιλογή των εκδηλώσεων σας!")
	c.setFont('DroidSerifBd',14)
	c.drawString(210,720,"Λεπτομέρειες εισιτηρίου")
	c.setFont('DroidSerif',14)
	c.drawString(150,670,"Όνομα εκδήλωσης: " + _event.title)
	c.drawString(150,650,"Τοποθεσία: " + location)
	c.drawString(150,630,"Πάροχος: " + provider)
	c.drawString(150,610,"Όνομα γονέα: " + parent_name)
	c.drawString(150,590,"Αριθμός εισιτηρίων: " + str(int(amount)))
	c.drawString(150,570,"Κόστος σε coins: " + str(cost))
	c.drawString(150,550,"Ημερομηνία αγοράς: " + purchase_date)
	c.save()


