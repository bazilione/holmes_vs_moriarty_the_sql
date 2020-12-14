# Description:  
"Holmes_moriarty_sql" project aimed to help learn the basics of the core data science skills:  
pandas, pyspark, SQL/Hive as well as Python in a form of a dynamically generated quest/puzzle.  

# Usage:  
Setup the environment (see below).
  
Solve the puzzle using the prepared notebook templates:  
'my_pandas_solution.ipynb'  
'my_pyspark_solution.ipynb'  
'my_pyspark_sql_solution.ipynb'.  
(Solving in this order is recommended.)  
  
  
The user can generate the data (saved to the 'data' folder as .csv and .txt files).  
Changing the seed (in 'helpers.py') will change the data (and the correct answer).
  
Alternatively, the user can use the precreated data (generated with '1234' seed).  
The data can be recreated using the same seed.  
  
To generate puzzle data, after the setup run the script 'generate_data_files.py' or  
open and run 'generate_data_files.ipynb' jupyter notebook.  
  
The correct answer is generated during data generation process and is saved  
in 'solution/moriarty_name.txt' file. Along with the answer, if needed for comparison or  
for help, the user can run and follow the notebooks with the solution:  
'pandas_solution.ipynb'  
'pyspark_solution.ipynb'  
'pyspark_sql_solution.ipynb'. 


# Setup:  
The project requires Python 3.6 or higher.  
  
Installation on a Linux-like terminal (includes MacOS).  
  
In a folder with your projects:  
git clone https://gitlab.com/vkerov/holmes_moriarty_sql.git  
cd holmes_moriarty_sql    
python3 -m venv env  
source env/bin/activate  
pip install -- requirements.txt  
cd src 
# to launch jupyter notebook
jupyter notebook  


#  Licence
Users and developers are encouraged to modify the code and add new puzzles.
Referencing the original creator (Vasily Kerov) is appreciated.
