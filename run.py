from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/trial', methods=['GET', 'POST'])
def trials():
    words = [['table', 'mesa'], ['chair', 'silla'], ['bathroom', 'baño']]
    displayText = ''

    if request.method == 'POST':
        answer = request.form.get('answer')

        if answer.lower() == words[0][1].lower():
            displayText = 'RIGHT!'
        else:
            displayText = 'WRONG!'
        return render_template('trials/trial.html', success=displayText)
    return render_template('trials/trial.html')




@app.route('/settings')
def settings():
    return render_template('settings/settings.html')

@app.route('/open')
def open_file():
    return render_template('open/open.html')

if __name__ =='__main__':
    app.run()
