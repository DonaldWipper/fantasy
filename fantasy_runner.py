import FlaskApp.sport_fantasy as sport_fantasy
import FlaskApp.parse as parse


#sport_fantasy.create_new_team(_tournament_id=57)
parse.run()
sport_fantasy.make_transfers(check=False)
