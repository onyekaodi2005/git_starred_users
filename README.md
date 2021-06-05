# git_starred_users
Get Githubs starred users and display them

Architecture: 
  1. retrieve data from github endpoint 100 pages per call using multiprocessing
  2. Retrieve key values from api response and store data using FLASK SQLALCHEMY 
  3. Incase of reruns validate that no duplicated data exist within database, else insert
  4. load retrieved datas to the webpage, add pagination, and sort to streamline data filteration
