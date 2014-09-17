import web

from web import form

from datetime import date



#Each of the following dictionaries is organized by category now, each of these replace screen_dict

infection_dict = {

'chlamydia':False,

'HIV':'HIV0', 

'syphilis':False,

'gonorrhea':False,

'HepC':False, 

}



other_dict = { # combined behavior and other together to reduce size of output 1/18/14

'osteo':False,

'folic':False,

'dom_violence':False, 

'elder':False,

'falls':False, #This will include both PT and Vit D recommendations, (-done- 12/4/13)

'STI_counsel':False, 

'sun_exposure':False,

'etoh':'etoh',

'depression':'depression'

}



cancer_dict = {

'cervix':False,

'CRC':False,

'mammo':False,

'BRCA':False,

'breastmed':False,

'lung':False

}



CV_dict = {

'ASA':False,

'lipids':False,

'AAA':False,

'obesity':'obesity',

'DM':'DM',

'diet':'diet',

'tobacco':False

}



vaccine_dict = {

'flu':'flu',

'zoster':False,

'pneumo':False,

'Tdap':'Tdap',

'HepB':'HepB',

'HepA':'HepA',

'HPV':False

}



#screen_list = [infection_dict, cancer_dict, CV_dict, other_dict, vaccine_dict]



#=======================================OUTPUT TEXTS============================

text_dict = {

'ASA':

'-Aspirin: Recommend if benefit outweighs GI risk\n',

'ASA0':

'-Aspirin: Above the recommended age for primary prophylaxis\n',

'ASA1':

'-Aspirin: Consider when 45 years old\n',

'ASA2':

'-Aspirin: Consider when 55 years old\n',



'cervix0':

'',

'cervix':

'-Cervical Cancer Screening: Recommend\n',

'cervix1':

'-Cervical Cancer Screening: Recommend when 21\n',

'cervix2':

'-Cervical Cancer Screening: Past recommended age\n',



'chlamydia0':

'',

'chlamydia':

'-Chlamydia screening: Recommend\n',



'CRC':

'-Colon Cancer: Recommend FOBT or colonoscopy\n',

'CRC1':

'-Colon Cancer: Recommend at age 50\n',

'CRC2':

'-Colon Cancer: Past recommended age\n',



'folic0':

'',

'folic':

'-Folic Acid Supplementation: Recommend if capable of having children\n',



'HIV0':

'-HIV Screening: Not indicated at this time\n',

'HIV':

'-HIV Screening: Recommend\n',



'lipids':

'-Lipid Screening: Recommend\n',

'lipids1':

'-Lipid Screening: Recommend if CAD risk factors\n',

'lipids2':

'-Lipid Screening: Consider at age 20 if CAD risk factors\n',



'syphilis0':

'',

'syphilis':

'-Syphilis Screening: Recommend\n',



'tobacco0':

'',

'tobacco':

'-Tobacco Cessation Counseling: Recommend\n',



'AAA0':

'',

'AAA':

'-AAA Screening: Recommend\n',

'AAA1':

'-AAA Screening: Recommend at age 65\n',

'AAA2':

'-AAA Screening: Past recommended screening age\n',



'etoh':

'-Alcohol Abuse Screening: Recommend\n',



'mammo0':

'',

'mammo':

'-Mammogram: Recommend\n',

'mammo1':

'-Mammogram: Recommend at age 50\n',

'mammo2':

'-Mammogram: Past recommended age\n',



'BRCA0':

'',

'BRCA':

'-BRCA: Obtain family history and calculate risk of BRCA mutation\n',

'BRCA1':

'-BRCA: Probably not indicated due to age\n',



'breastmed0':

'',

'breastmed':

'-Breast Cancer Modifying Drugs: Calculate patient risk and consider\n',

'breastmed1':

'-Breast Cancer Modifying Drugs: Probably not indicated due to age\n',



'depression':

'-Depression Screening: Recommend\n',



'falls0':

'',

'falls':

'-Fall Risk: Assess risk. If high prescribe vitamin D and Physical Therapy\n',



'gonorrhea0':

'',

'gonorrhea':

'-Gonorrhea Screening: Recommend\n',



'diet':

'-Nutrition Referral: Recommend if dyslipidemia or CVD\n',



'HepC0':

'', 

'HepC':

'-HepC Screening: Recommend\n', 



'dom_violence0':

'',

'dom_violence':

'-Interpersonal Violence Screening: Recommend\n',



'elder0':

'',

'elder':

'-Elder Abuse Screening: Recommend\n',



'obesity':

'-Obesity Screening: Recommend\n', # Add EPIC smarttext for BMI



'osteo0': 

'',

'osteo': 

'-Osteoporosis: Recommend DEXA\n', 

'osteo1': 

'-Osteoporosis: Assess risk with FRAX, consider screening\n', 

'osteo2': 

'-Osteoporosis: Not recommended until age 65, or 50 if risk factors\n',  



'STI_counsel0':

'',

'STI_counsel':

'-STI Counseling: Discuss safe sex practices\n',



'sun_exposure0':

'',

'sun_exposure':

'-Skin Cancer Precautions: Discuss if patient has fair skin\n',



'DM':

'-Diabetes: Screen patients with BP > 135/80 or treated HTN\n',



'flu':

'-Flu: Recommend yearly\n', #smarttext?



'Tdap':

'-Tdap: Recommend Tdap once, then Td booster every 10 years.\n',



'zoster0':

'-Zoster: Recommend at age 60\n',

'zoster':

'-Zoster: Recommend\n',



'pneumo0':

'-Pneumonia Vaccination: Recommend at age 65\n',

'pneumo':

'-Pneumonia Vaccination: Recommend\n',

'pneumo1':

'-Pneumonia Vaccination: Recommend now and then repeat at age 65\n',



'HPV0':

'',

'HPV':

'-HPV: Recommend \n',

'HPV1':

'-HPV: Recommend for HIV + males younger than 26 \n',



'HepB':

'-Hepatitis B: May require, see CDC recommendations\n', #smart?



'HepA':

'-Hepatitis A: May require, see CDC recommendations\n', #smart?



'lung0':

'',

'lung':

'-Lung Cancer: Consider CT (see recs)\n',

'lung1':

'-Lung Cancer: Consider CT at age 55 (see recs)\n',

'lung2':

'-Lung Cancer: Past recommended screening age\n',

}



#The string that will be displayed in the final text box

basic_text = "USPSTF Grade A/B screening and CDC adult vaccination recommendations:\n"



#Need to make debug mode off if using sessions

web.config.debug = False



urls = (

	'/', 'index',

	'/results', 'results',

	'/formpage', 'formpage'

)



app = web.application(urls, locals())



#Code to create and store sessions (allows POSTed input to be stored and used to make rec lists)

store = web.session.DiskStore('sessions')

session = web.session.Session(app, store, initializer={'count':0})



#Makes sure the template engine looks under the folder 'templates/' for my html files.  Also makes globals do something(?) so that I can save variables as a session.

render = web.template.render('templates/', globals={'context': session})



# The Forms used for input

age_form = form.Form(

	form.Textbox('number',

		form.notnull,

		form.regexp('^-?\d+$', 'Not a number.'),

		form.Validator("Too young, don't use this tool.", lambda x: int(x)>17),

		size="1",

		maxlength="2",

		description='Age:'

		))

#At some point I would like to figure out how to validate age_form to prevent age < 18.



gender_form = form.Form(

	form.Radio('Gender:', ['Female','Male'], 

	form.notnull))



smoke_form = form.Form(

	form.Radio('Smoking:', ['Never Smoker', 'Past Smoker', 'Current Smoker'], 

	form.notnull))



sex_form = form.Form(

	form.Radio('Sexually Active?:', ['Yes', 'No',], 

	form.notnull))



highrisk_form = form.Form(

	form.Checkbox('High Risk Sexual Activity?:', 

	value=True, 

	post="<em>  High risk history includes having a history of STI, new or multiple sex partners, inconsistent condom use, exchanging sex for money or drugs.</em>"))



drug_form = form.Form(

	form.Checkbox('Past or current IV or intranasal drug use?:', 

	value=True))



pneumo_form = form.Form(

	form.Checkbox('Chronic Disease?:', 

	value = True, 

	post = "<em>  Any lung, CVD, DM, CKD, nephrotic syndrome, liver, alcoholism, cochlear implants, CSF leaks, immunocompromise, spleen issues, and nursing home residents.</em>"))



#A function that takes the input from the forms and gives a sentence

def resulter(results):

	age = results['number']

	gender = results['Gender:']

	smoking = results['Smoking:']

	sexActive = results['Sexually Active?:']

	drug = ""

	if 'Past or current IV or intranasal drug use?:' in results:

		drug = ", has IV or intranasal drug use,"

	if 'High Risk Sexual Activity?:' in results:

		hr = " and has a high risk sexual history."

	else:

		hr = "."	

	

	if sexActive == 'Yes':

		activity = ""

	else:

		activity = "not"

	finaltext = " %s year old %s who is a %s%s and is %s sexually active%s" % (age, gender, smoking, drug, activity, hr)

	return finaltext	



#==============================================================================

#A really ugly function that assigns correct recommendations in dictionary, anything that defaults to True in the dictionaries is omitted here

def assigner(somevariable):

	age = int(somevariable['number'])

	gender = somevariable['Gender:']

	smoking = somevariable['Smoking:']

	sexActive = somevariable['Sexually Active?:']

	if 'High Risk Sexual Activity?:' in somevariable:

		hr = True

		sexActive = 'Yes'

	else:

		hr = False

	if 'Past or current IV or intranasal drug use?:' in somevariable:

		drug = True

	else:

		drug = False

	# Next line toggles chronic true for indications for pneumovax (smoking and disease)

	if 'Chronic Disease?:' in somevariable or smoking == 'Current Smoker':

		chronic = True

	else:

		chronic = False

	DOB = (date.today().year - age)

#screen_list = [infection_dict, cancer_dict, CV_dict, other_dict, vaccine_dict]



	inf = infection_dict.copy()

	can = cancer_dict.copy()

	cv = CV_dict.copy()

	oth = other_dict.copy()

	vac = vaccine_dict.copy()



	

#ASA

	if gender == 'Male':

		if age >= 45 and age <= 79:

			cv['ASA'] = 'ASA'

		if age > 79:

			cv['ASA'] = 'ASA0'

		if age < 45:

			cv['ASA'] = 'ASA1'			

	if gender == 'Female':

		if age >= 55 and age <= 79:

			cv['ASA'] = 'ASA'

		if age > 79:

			cv['ASA'] = 'ASA0'

		if age < 55:

			cv['ASA'] = 'ASA2'

	

	

#cervix

	if gender == 'Female':

		if age >= 21 and age <= 65:

			can['cervix'] = 'cervix'

		if age < 21:

			can['cervix'] = 'cervix1'

		if age > 65:

			can['cervix'] = 'cervix2'

	if gender == 'Male':

		can['cervix'] = 'cervix0'



#chlamydia

	if gender == 'Female':

		if sexActive == 'Yes':

			if age <= 24:

				inf['chlamydia'] = 'chlamydia'

			elif hr == True:

				inf['chlamydia'] = 'chlamydia'

			else:

				inf['chlamydia'] = 'chlamydia0'

		else:

			inf['chlamydia'] = 'chlamydia0'

	else:

		inf['chlamydia'] = 'chlamydia0'



#CRC

	if age >=50 and age <= 75:

		can['CRC'] = 'CRC'

	if age < 50:

		can['CRC'] = 'CRC1'

	if age > 75:

		can['CRC'] = 'CRC2'

#folic

	if gender == 'Female':

		if age >= 18 and age <= 50:

			oth['folic'] = 'folic'

		else:

			oth['folic'] = 'folic0'

	else:

		oth['folic'] = 'folic0'

#HIV

	if age >= 15 and age <= 65 or hr == True or drug == True:

		inf['HIV'] = 'HIV'	

#lipids 

	if gender == 'Male':

		if age >= 35:

			cv['lipids'] = 'lipids'

		if age >= 20 and age < 35:

			cv['lipids'] = 'lipids1'

		if age < 20:

			cv['lipids'] = 'lipids2'

	if gender == 'Female':

		if age >= 45:

			cv['lipids'] = 'lipids'

		if age >= 20 and age <= 45:

			cv['lipids'] = 'lipids1'

		if age < 20:

			cv['lipids'] = 'lipids2'



#syphilis

	if hr == True:

		inf['syphilis'] = 'syphilis'

	else:

		inf['syphilis'] = 'syphilis0'

#tobacco

	if smoking == 'Current Smoker':

		cv['tobacco'] = 'tobacco'

	else:

		cv['tobacco'] = 'tobacco0'

#AAA

	if gender == 'Male':

		if smoking == 'Current Smoker' or smoking == 'Past Smoker':

			if age >= 65 and age <= 75:

				cv['AAA'] = 'AAA'

			if age < 65:

				cv['AAA'] = 'AAA1'

			if age > 75:

				cv['AAA'] = 'AAA2'

		else:

			cv['AAA'] = 'AAA0'

	else:

		cv['AAA'] = 'AAA0'		

#BRCA

	if gender == 'Female':

		if age < 70:

			can['BRCA'] = 'BRCA'

		else:

			can['BRCA'] = 'BRCA1'	

	else:

		can['BRCA'] = 'BRCA0'

#breastmed

	if gender == 'Female':

		if age < 70:

			can['breastmed'] = 'breastmed'

		else:

			can['breastmed'] = 'breastmed1'

	else:

		can['breastmed'] = 'breastmed0'

#mammo

	if gender == 'Female':

		if age >= 50 and age <= 74:

			can['mammo'] = 'mammo'

		if age < 50:

			can['mammo'] = 'mammo1'

		if age > 74:

			can['mammo'] = 'mammo2'

	else:

		can['mammo'] = 'mammo0'

#falls(including PT and vitamin D)

	if age >= 65:

		oth['falls'] = 'falls'

	else:

		oth['falls'] = 'falls0'

#gonorrhea 

	if gender == 'Female':

		if hr == True:

			inf['gonorrhea'] = 'gonorrhea'

		elif hr == False:

			if sexActive == 'Yes':

				if age <= 25:

					inf['gonorrhea'] = 'gonorrhea'

				else:

					inf['gonorrhea'] = 'gonorrhea0'

			else:

				inf['gonorrhea'] = 'gonorrhea0'

	else:

		inf['gonorrhea'] = 'gonorrhea0'

				

#HepC

	if DOB >= 1944 and DOB <= 1966:

		inf['HepC'] = 'HepC'

	elif drug == True:

		inf['HepC'] = 'HepC'

	else:

		inf['HepC'] = 'HepC0'

#dom_violence

	if gender == 'Female':

		if age >= 18 and age <= 50:

			oth['dom_violence'] = 'dom_violence'

		else:

			oth['dom_violence'] = 'dom_violence0'

	else:

		oth['dom_violence'] = 'dom_violence0'

		

#elder abuse

	if age >= 60:

		oth['elder'] = 'elder'

	else:

		oth['elder'] = 'elder0'

		

#osteo

	if gender == 'Female':

		if age >= 65:

			oth['osteo'] = 'osteo'

		if age < 65 and age >= 50:

			oth['osteo'] = 'osteo1'

		if age < 50:

			oth['osteo'] = 'osteo2'

	else:

		oth['osteo'] = 'osteo0'

			

#STI_counsel

	if hr == True:

		oth['STI_counsel'] = 'STI_counsel'

	else:

		oth['STI_counsel'] = 'STI_counsel0'



#sun_exposure (only if fair skin)

	if age >= 18 and age <= 24:

		oth['sun_exposure'] = 'sun_exposure'

	else:

		oth['sun_exposure'] = 'sun_exposure0'	



#zoster

	if age >= 60:

		vac['zoster'] = 'zoster'

	else:

		vac['zoster'] = 'zoster0'





#pneumo

	if age >= 65:

		vac['pneumo'] = 'pneumo'

	if age < 65 and chronic == True:

		vac['pneumo'] = 'pneumo1'

	if age < 65 and chronic == False:

		vac['pneumo'] = 'pneumo0'



#HPV (issue is that HIV+ males should have it until age 26, non HIV only until age 21)

	if gender == 'Female':

		if age <= 26:

			vac['HPV'] = 'HPV'

		else:

			vac['HPV'] = 'HPV0'

		

	if gender == 'Male':

		if age <= 26:

			vac['HPV'] = 'HPV1'

		else:

			vac['HPV'] = 'HPV0'

#lung

	if smoking == 'Current Smoker' or smoking == 'Past Smoker':

		if age >= 55 and age <= 80:

			can['lung'] = 'lung'	

		if age > 80:

			can['lung'] = 'lung2'

		if age < 55:

			can['lung'] = 'lung1'

	else:

		can['lung'] = 'lung0'

	

	

	return inf, can, cv, oth, vac

#=============================================end of assigner function==================



#screen_list = [infection_dict, cancer_dict, CV_dict, other_dict, vaccine_dict]



#Function that appends the text from text_dict to final_text

def infection_texter(text, infection_dict, true_string_dict):

	text += "\n*INFECTION*\n"

	for i in infection_dict:

		text += true_string_dict[infection_dict[i]]

	return text



def cancer_texter(text, cancer_dict, true_string_dict):

	text += "\n*CANCER*\n"

	for i in cancer_dict:

		text += true_string_dict[cancer_dict[i]]

	return text



def CV_texter(text, CV_dict, true_string_dict):

	text += "\n*CARDIOVASCULAR*\n"

	for i in CV_dict:

		text += true_string_dict[CV_dict[i]]

	return text



def other_texter(text, other_dict, true_string_dict):

	text += "\n*OTHER*\n"

	for i in other_dict:

		text += true_string_dict[other_dict[i]]

	return text



def vaccine_texter(text, vaccine_dict, true_string_dict):

	text += "\n*VACCINATIONS*\n"

	for i in vaccine_dict:

		text += true_string_dict[vaccine_dict[i]]

	return text

	

class formpage:

	

	def GET(self):

		# create copies of forms so that changes do not act globally

		my_form = age_form()

		my_form2 = gender_form()

		my_form3 = smoke_form()

		my_form4 = sex_form()

		my_form5 = highrisk_form()

		my_form6 = drug_form()

		my_form7 = pneumo_form()

		

		return render.screenHTML1(my_form, my_form2, my_form3, my_form4, my_form5, my_form6, my_form7)



	def POST(self):

		my_form = age_form(web.input())

		my_form2 = gender_form(web.input())

		my_form3 = smoke_form(web.input())

		my_form4 = sex_form(web.input())

		my_form5 = highrisk_form(web.input())

		my_form6 = drug_form(web.input())

		my_form7 = pneumo_form(web.input())

		

		if not my_form.validates():

			return render.screenHTML1(my_form, my_form2, my_form3, my_form4, my_form5, my_form6, my_form7)

		if not my_form2.validates(): 

			return render.screenHTML1(my_form, my_form2, my_form3, my_form4, my_form5, my_form6, my_form7)

		if not my_form3.validates():

			return render.screenHTML1(my_form, my_form2, my_form3, my_form4, my_form5, my_form6, my_form7)

		if not my_form4.validates():

			return render.screenHTML1(my_form, my_form2, my_form3, my_form4, my_form5, my_form6, my_form7)

		if not my_form5.validates():

			return render.screenHTML1(my_form, my_form2, my_form3, my_form4, my_form5, my_form6, my_form7)

		result_data = web.input()

		#Create a session, web.input() will be stored as session.count (probably not ideal)

		session.count = result_data

		#print session.count

		return web.seeother('/results')



#screen_list = [infection_dict, cancer_dict, CV_dict, other_dict, vaccine_dict] (for reference of order)						

class results:

	def GET(self):

		bob = resulter(session.count)

		raw_results = session.count #Make a copy of the global before I end the session

		final_infection, final_cancer, final_CV, final_other, final_vaccine = assigner(raw_results) # Runs assigner, which toggles True for indicated screenings/vaccinations

		print final_CV, final_cancer, final_infection, final_other, final_vaccine

		text1 = infection_texter(basic_text, final_infection, text_dict) # Split up text assigners into multiple functions

		text2 = cancer_texter(text1, final_cancer, text_dict)

		text3 = CV_texter(text2, final_CV, text_dict)

		text4 = other_texter(text3, final_other, text_dict)

		text5 = vaccine_texter(text4, final_vaccine, text_dict)

		

		session.kill()

		return render.screenHTML2(bob, text5)

					

#This runs the website

if __name__ == "__main__":

	#app = web.application(urls, globals(), True)

	app.run()



