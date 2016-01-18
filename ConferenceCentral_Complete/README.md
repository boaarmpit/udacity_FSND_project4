# Udacity Full Stack Web Developer Nanodegree project 4
This project is *a cloud-based API server to support a provided conference organization [application](https://github.com/udacity/ud858) that exists on the web. The API supports the following functionality found within the app: user authentication, user profiles, conference information and various manners in which to query the data.*


## Usage
### Requirements
[Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)

## Setup Instructions
1. Update the value of `application` in `app.yaml` from `udacity-project-4-bryn` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
1. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][1].  At a minimum, a `WEB_CLIENT_ID` is required.
1. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
1. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
1. Run the app with the [devserver][2] using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][3].)
1. (Optional) Generate your client library(ies) with [the endpoints tool][4].
1. Deploy your application.


[1]: https://console.developers.google.com/
[2]: https://cloud.google.com/appengine/docs/python/tools/devserver
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[3]: https://localhost:8080/
[4]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool
