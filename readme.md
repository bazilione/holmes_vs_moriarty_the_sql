# Description:  
"holmes_moriarty_sql" project aimed to help learn the basics of the core data science skills:  
pandas, pyspark, SQL/Hive as well as Python in a form of a dynamically generated quest/puzzle  
inspired by the adventures of Conan Doyle's Mr. Holmes and Dr. Watson who are after the crime 
world master mind Professor Moriarty.  
  
The project can also be used to create test data sets to evaluate one's data science skills.  
  
# Usage:  
Setup the environment (see below).
  
Solve the puzzle using the prepared notebook templates:  
'my_solution_pandas.ipynb'  
'my_solution_pyspark.ipynb'  
'my_solution_pyspark_sql.ipynb'.  
(Solving in this order is recommended.)  
  
  
The user can generate the data (saved to the 'data' folder as .csv and .txt files).  
Changing the seed (in 'helpers.py') will change the data (and the correct answer).
  
Alternatively, the user can use the supplied data (generated with '1234' seed).  
The data can be recreated using the same seed. To generate new puzzle data change the seed 
in helpers.py and run the script 'generate_data_files.py'.  
  
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

git clone https://github.com/bazilione/holmes_vs_moriarty_the_sql.git  
cd holmes_moriarty_sql    
python3 -m venv env  
source env/bin/activate  
pip install -- requirements.txt  
cd src  
  
# Testing (in src folder):  
pytest  
  
# to launch jupyter notebook
jupyter notebook  
  
#  License  
Users and developers are encouraged to modify the code and add new puzzles.
Referencing the original creator (Vasily Kerov) is appreciated.

#  Acknowledgements  
I thank Joan Phar for her help in reviewing and testing.  
  

