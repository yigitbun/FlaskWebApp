from flask import Flask, render_template, request
import pandas as pd
import TeamITea

app = Flask(__name__)

df=pd.read_csv("kbClean.csv")
kb_stars = df[['NameKlinik', 'Gesamt', 'Zufriedenheit']]
kb_means = kb_stars.groupby(['NameKlinik'], as_index=False)['Gesamt'].mean()
kb_means = kb_means.sort_values('Gesamt',ascending=False, ignore_index=True)
vergleich_list = kb_means['Gesamt'].to_list()
nameKlinik = kb_means['NameKlinik'].to_list()

# Sterne Dict
df2 = df.groupby(['NameKlinik', 'Gesamt']).size().unstack().reset_index()
sterneDict = df2.set_index('NameKlinik').T.to_dict('list')


@app.route("/")
def index():
    return render_template("index.html",serie=vergleich_list)

@app.route('/vorhersage')
def my_form():
    return render_template('vorhersage.html')

@app.route('/vorhersage', methods=['POST'])
def my_form_post():
    text = request.form['text']
    result = TeamITea.vorhersage(text) 
    return render_template('vorhersage.html',result=result[0],text1=text)

@app.route("/bewertungen")
def bewertungen():
    dizi = df.groupby(['NameKlinik']).mean().get('Gesamt')
    return render_template("bewertungen.html",dizi=dizi,nameKlinik=nameKlinik,display='none')   

@app.route("/bewertungen", methods=['POST'])
def bewertungen_post():
    kname = request.form['options']

    # KB Bewertungen
    df2 = df.where(df["NameKlinik"]==kname)
    df2.dropna(inplace=True)
    kb_bewertungen = df2['Erfahrungsbericht']

    # KB Sterne
    kb_sterne = df2['Gesamt']
    kb_sterne =[int(i) for i in kb_sterne]

    # KB poz_neg result
    kb_result = df2['Zufriedenheit']

    kb = zip(kb_bewertungen,kb_sterne,kb_result)

    data = sterneDict[kname]
    
  
    return render_template("bewertungen.html",kname=kname,display='block',display2='none',nameKlinik=nameKlinik,kb=kb,data=data)      
  

if __name__ == "__main__":
    app.run(debug=True)