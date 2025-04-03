# FitnessTracker

Django installation/overview


General Documentation:

https://docs.djangoproject.com/en/5.1/ 

Recommended: Take a look at First Steps > (“from Scratch” and “tutorial”)



Installation

https://docs.djangoproject.com/en/5.1/intro/install/ 


Steps to get it running:
1. Clone the repo: git clone https://github.com/Group9FitnessTracker/FitnessTracker.git
2. navigate to the project directory: cd fitnessTracker
3. Install django and other dependecies: pip install -r requirements.txt
4. Create a virtual environment: python -m venv venv
5. Activate the virtual environment:
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

Note if step 5 has a security error try running this command before rerunning the command above: Set-ExecutionPolicy Unrestricted -Scope Process

Run the server: python manage.py runserver
Step 6 should take you to http://127.0.0.1:8000/ which has the text "Hello, world. You're at the default page."
