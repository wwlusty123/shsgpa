from flask import Flask, render_template, request
import pickle
import codecs

application=app = Flask(__name__)

h_dictionary={"A":5.0, "A-":4.7, "B+":4.3, "B":4.0, "B-":3.7, "C+":3.3, "C":3.0, "C-":2.7, "D": 1.3, "F":0.0}
reg_dictionary={"A":4.3, "A-":4.0, "B+":3.7, "B": 3.3, "B-":3.0, "C+":2.7, "C":2.3, "C-":2.0, "D":1.3,"F":0.0}
count = 24628
responses = [4.52, 3.3, 3.3, 4.3, 4.35, 4.4, 4.475, 3.3, 4.428571428571429, 4.428571428571429]

@app.route('/donate')
def donate():
	return render_template('donate.html')

@app.route('/distribution')
def distribution():
	pickled = codecs.encode(pickle.dumps(responses), "base64").decode()
	return render_template("distribution.html", text=pickled)

@app.route('/', methods=["GET", "POST"])
def home():
	global count
	count += 1
	return render_template('summitgpa.html')
@app.route("/about")
def about():
	return render_template('about.html')
@app.route('/display', methods=["GET", "POST"])
def display():
	if request.method=="POST":
		entries=[]
		for num in range(1, 11):
			g = "grade_" + str(num)
			h = "honors_" + str(num)
			hal = "halfyear_" + str(num)
			grade=request.form.get(g)
			honors=request.form.get(h)
			halfyear=request.form.get(hal)
			if grade != "":
				e = Entry()
				e.grade=grade
				e.honors=(honors=="yes")
				e.halfyear=(halfyear=="yes")
				entries.append(e)
	return render_template("display.html", gpa=calculate(entries))
def calculate(entries):
	toRet=0.0
	total=0.0
	for entry in entries:
		if entry.honors:
			if entry.halfyear:
				toRet+=(h_dictionary[entry.grade]*2.5)
				total += 2.5
			else:
				toRet+= h_dictionary[entry.grade]*5
				total+=5
		else:
			if entry.halfyear:
				toRet+=(reg_dictionary[entry.grade]*2.5)
				total += 2.5
			else:
				toRet += reg_dictionary[entry.grade]*5
				total += 5
	toRet /= total
	entries.clear()
	responses.append(toRet)
	return toRet
@app.route("/usercount")
def user_count():
	return render_template("count.html", count=count)
class Entry(object):
	def __init__(self):
		grade=""
		honors=False
		halfyear=False
	def __str__(self):
		return "{} {}".format(self.grade, self.honors)
if __name__ == "__main__":
	app.run(debug=True)
