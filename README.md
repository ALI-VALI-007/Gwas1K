# Gwas1K
The plan is to: \n
-Add the 1KG project to the database \n
  -If the 1KG isn't able to be added we can instead call the ensemble API and treat the database like a cache and store the called data there \n
  -As we keep using it more data is stored and we will eventually get all (or most) of the data and remove the ensemble API \n
-Create a frontend for the tables \n
  -Should have a search bar which executes a func the search bar input will be the WHERE clause (for the specific disease) \n
  -Maybe a "adv search" feature where we let the user put in the specific populationss themselves \n
-Fix up the backend \n
  -Either remove nonused funcs and code or redo the backend \n
