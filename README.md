## simple poll 

The Full-Stack Polling System is a web application that allows users to create, share, and participate in polls in a secure and interactive way. It integrates a frontend, backend, and database to deliver a complete solution. Users can create polls with multiple options, cast votes, and view results in real time. The system ensures that each user votes only once per poll, stores poll data efficiently, and displays results using charts or graphical statistics.


## features

Poll Management: Users can create, edit, or delete polls.

Voting System: Secure voting ensures one vote per user per poll.

Real-Time Results: Display results dynamically using charts or percentages.

Responsive Design: Works on desktops and mobile devices.

Data Storage: Poll questions, options, votes, and user info stored in the database.

## project structure

SIMPLE POLL
|
|---src                 #core application logic
|   |---logic.py        #business logic and task
operations
|   |__db.py            #database operations
|
|----api/               #backend api
|   |__main.py          #FASTAPI end points
|
|----front end/         #front end applications
|   |--app.py           #streamlit web interfaces
|
|___requirements.txt    #python dependencies
|
|___README.md           #project documentation
|
|__.env                 #python Variables

## quick start
### prerequisuties

 - python 3.8 or higher
 - a supabase account
 - Git(Push,Cloning)

### 1.clone or download the project
# option 1:clone with Git
git clone:<repository-url>

# option 2: Download and extract the zip files

# install all required python packages
pip install -r requirements.txt

### 3.setup supa base database

1.create a supabase project:

2.create the task table:

- goto sql editor in your supabase dashboard
- run this sql command

3. get your credentials

### 4.configure environment variables

1. create a `.env` file in the project root

2. add your supabase credentitals to `.env` :
SUPABASE_URL=
SUPABASE_KEY=

**example** 
SUPABASE_URL=
SUPABASE_KEY=

## streamlit frontend
streamlit run frontend/app.py

the app will open in your browser at `http://localhost:8501`

## fastapi backend

cd api
python main.py

The API will be available at `http://localhost:8000`

## How to use

## Technical Details

## Technologies used

- **frontend**: streamlit (python web framework)
- **backed**: FastAPI (python REST API framework)
- **Database**: supabase (postgreSQL-based backen-A--service)
- **Laguage**: pyhton 3.8+

### key components

1. **`src/db.py`**: Database operation handles all CRUD operations with Supabase

2. **`src/logic.py`**: Business logic task validation and processing

## Trouble shooting

## common issues

## future Enhancements

Idea for extenfing this project :

**user Authentication** :Add user accounts and login

**Task categories**: Email or push notifications for due dates

**File attchments**: Attach file to tasks

**collaboration**: share tasks with classmates



## support

If you encounter any issues or have questions:
