# Udacity Full Stack Nanodegree Project 4: "Design a Game" 
*"The backend for a platform-agnostic app using Google App Engine backed by Google Datastore."*  
This application is the backend for an implementation of the *iterated prisoner's dilemma* game.

####About the prisoner's dilemma
The prisoner's dilemma is a common example in game theory, illustrating a situation in which by optimizing only their own outcomes, two parties cause a non-optimal outcome for both parties.

The situation is as follows:  
*Two prisoners, or suspects in a crime, are interrogated independently and cannot communicate with each other.  They both have the following options; to stay silent, or to admit guilt by defecting and incriminating both themselves and the other party.*  
Their sentences are determined in the following manner:  

||Prisoner B stays silent (<i>cooperates</i>)|Prisoner B betrays (<i>defects</i>)
|---|---|---|
|<b>Prisoner A stays silent (<i>cooperates</i>)</b>|Each serves 1 year|Prisoner A: 3 years<br>Prisoner B: goes free
|<b>Prisoner A betrays (<i>defects</i>)</b>|Prisoner A: goes free<br>Prisoner B: 3 years|Each serves 2 years

(From [wikipedia](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma))

One can see from the table above that a party trying to optimize their own outcome (reduce their own sentence) will always choose to defect, as regardless of what the other party chooses, defecting will always reduce the defector's sentence.  However, if both parties act in this way they will both receive a two year sentence, which is worse than the one year sentence that they both would have received if they had both stayed silent!

This is interesting in itself, however the *iterated* prisoner's dilemma is a more interesting game in which the above situation is repeated.  In each round, the players (prisoners) decide whether to stay silent or to defect, and are then given the result (their sentence).  This process is repeated a number of times until the game is terminated.  The number of rounds is not known to the players beforehand.  The final scores are determined by the total number of years to be served by each player, where less is better.

###Features  

This backend for an online two player iterated prisoner's dilemma game has the following functionality.

- Create Users (players).  Users' email addresses are sourced from their google login and are used for game notifications.
- Create Matches with multiple Games between Users.
- Play Games with recorded history, and scores saved to User profiles
- Get User rankings
- Notify Users of unfinished Matches (automatically every hour)

## Usage
### Requirements
*[Python 2.7](https://www.python.org/downloads/)* (tested with version 2.7.6)  
*[Google App Engine SDK](https://cloud.google.com/appengine/downloads)* (tested with version 1.9.28)  

### Setup
0. Clone this repository.
1. Create a new project in your *[Google Cloud Platform Console](https://console.cloud.google.com/)* and copy your application ID to *app.yaml* in place of `udacity-project-4-bryn`.
2. Deploy your project. (See the [docs](https://cloud.google.com/appengine/docs/python/) for details).

### Endpoints
 - **create_user**
    - Path: 'create_user'
    - Method: POST
    - Parameters: user_name
    - Returns: Message confirming creation of the User.
    - Description: *Create a User. Requires a unique username. Gets email from oauth account*

 - **create_match**
    - Path: 'create_match'
    - Method: POST
    - Parameters: player_1_name, player_2_name
    - Returns: Message confirming creation of the Match.
    - Description: *Create a Match between two Users*

 - **create_game**
    - Path: 'create_game'
    - Method: POST
    - Parameters: match_key
    - Returns: Message confirming creation of the Game.
    - Description: *Create a Game in a Match (between participating Users)*

 - **get_game**
    - Path: 'get_game'
    - Method: GET
    - Parameters: game_key
    - Returns: Confirmation message listing players if Game is found.
    - Description: *Get a Game from its websafe key*
    
 - **play_game**
    - Path: 'play_game'
    - Method: POST
    - Parameters: game_key, player_name, move
    - Returns: Confirmation message listing move and result.
    - Description: *Play move in a Game.* A move of 'True' corresponds to defecting and 'False' corresponds to staying silent. This function registers a single player's move. If both player's have played it scores the game and returns the result.  It also automatically updates the Match and player User objects.
    
 - **get_user_matches**
    - Path: 'get_user_matches'
    - Method: GET
    - Parameters: player_name
    - Returns: List of active matches for the user
    - Description: *Play move in a Game.*

 - **cancel_match**
    - Path: 'cancel_match'
    - Method: POST
    - Parameters: match_key
    - Returns: Confirmation message
    - Description: *Cancel an active match*
 
 - **get_user_rankings**
    - Path: 'get_user_rankings'
    - Method: GET
    - Parameters: match_key
    - Returns: List of Users in descending order of score
    - Description: *Return list of Users in descending order of score*
    
  - **get_match_history**
    - Path: 'get_match_history'
    - Method: GET
    - Parameters: match_key
    - Returns: List of Game plays in Match
    - Description: *Return list of Game plays in Match*
    
   - **get_active_users**
    - Path: 'get_active_users'
    - Method: GET
    - Parameters: 
    - Returns: List of users with active matches
    - Description: *Return list of users with active matches*