heroku create emoti-ds
git remote add heroku https://git.heroku.com/emoti-ds.git

# Call example
 curl -X POST -H "Content-Type: application/json" -d '{"text": "The experiemce was very bad, do not recommend"}' http://emoti-ds.herokuapp.com/scores
