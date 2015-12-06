from flask import Flask, url_for, redirect
import praw
app = Flask(__name__)

subs = ['Formula1', 'WEC', 'MechanicalKeyboards', 'BTCC', 'FountainPens', 'Programming', 'ProgrammerHumor', 'Civ', 'TruckSim', 'FlightSim', 'Flying', 'AskReddit', 'WorldNews', 'All']
r = praw.Reddit(user_agent="Readit: Reddit as a newsstream viewer")

@app.route('/r/<sub>')
def readSub(sub):
    if sub == "":
        sub = "All"
    starthtml = """<html><head>
    <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Ubuntu">
    </head><body><div style=\"font-family:Ubuntu\">"""
    subreddit = r.get_subreddit(sub)
    starthtml += "<div style=\"background-color: PowderBlue;padding-top:10px;height:50px\">"
    starthtml += "<span style=\"font-weight:bold; width:200px;float:left;padding-left:10px\">" + sub + "</span>"
    starthtml += "<span style=\"width:calc(100% - 300px);text-align:right;float:right;padding-right:10px\">" + ("&nbsp;" * 5).join(["<a href = '/r/" + s + "'>" + s + "</a>" for s in subs]) + "</span>"
    starthtml += "</div>"
    colours = ["floralwhite", "lightgrey"]
    colourpick = False
    for submission in subreddit.get_top_from_day(limit=20):
        tags = ""
        addto = False
        newtitle = list(submission.title)
        for i, c in enumerate(submission.title):
            if addto:
                newtitle[i] = ""
                if c == "]":
                    addto = False
                    tags = tags + ", "
                    continue
                tags = tags + c
            else:
                if c == "[":
                    addto = True
                    newtitle[i] = ""
        taggedas = ""
        if tags:
            tags = tags[:-2]

        is_self = submission.is_self
        taggedas = "<div style=\"text-align:center;width:100px;height:50px;vertical-align:center;line-height:50px\">" + tags + "</div>"

        starthtml += "<div style=\"padding-top:10px;padding-bottom:10px;width:100%;overflow: auto;background-color: " + colours[int(colourpick)] + "\">"
        starthtml += "<div style=\"width:100px; height:50px; float:left; background-image:url('" + url_for("static", filename = ((is_self * "selfpost.png") + (not is_self) * "linkpost.png")) + "')\">" + taggedas + "</div>"
        starthtml += "<div style=\"font-size:18px;float:left;width: calc(100% - 100px)\"><a href=\"" + submission.url + "\" target=\"_blank\">" + "".join(newtitle) + "</a>"
        starthtml += "</br>""<i>Submitted by " + submission.author.name + " with " + str(submission.score) + " points." + " <a href=\"" + submission.short_link + "\" target=\"_blank\">[comments]</a></i></div></div>"
        colourpick = not colourpick
    endhtml = "</div></body></html>"
    return starthtml + endhtml
        
@app.route('/')
def mainPage():
    return redirect(url_for('readSub', sub='All'))


if __name__ == '__main__':
    app.run(host='192.168.1.113', port=80)
    r.login('readit_crawler', 'readit')
    
