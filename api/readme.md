# Test API My Emotion
The my emotion API is a FLASK based test app deployed in Heroku on top of the Logistic regression we have trained before. Now the api is world wide open and there is no authentication applied. Currently there is only one end endpoint with post request is possible.

__The first few calls to the api will take long time as the server need to 
initiate. That's a Heroku issue when using free service.__

## Endpoints
The api is serving on : `http://emoti-ds.herokuapp.com/` with the only applied endpoint `scores`

## Post /scores
- General:
  - The endpoint receive a json string like object and capable of providing prediction on the text.

- sample call:
  - `curl -X POST -H "Content-Type: application/json" -d '{"text": "The experiemce was very bad, do not recommend"}' http://emoti-ds.herokuapp.com/scores`

The call back should be a json like object:

```json
{
  "confidence": 96.63,
  "label": "not satisfied",
  "score": 0,
  "success": true
}
```

In case of any wrong data provided it should handle the error with error code 400, 422 and 404 and success indicator will be false.

A failed request:

sample: `curl -X POST -H "Content-Type: application/json" -d '{"abc": "asdfdsf sdasdf asdfadsf"}' http://emoti-ds.herokuapp.com/scores`

```json
{
  "error": 400,
  "message": "bad request",
  "success": false
}
```
