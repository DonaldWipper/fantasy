import requests
from robobrowser import RoboBrowser
import pandas as pd
try:
    import  FlaskApp.parse_class as pc
except:
    import  parse_class as pc
#import  parse_class as pc

class sportsApiMethods():
    def __init__(self, _settings = None, _url_login = None, _login = None, _password = None):
        self.settings = _settings["sport_api"]
        self.headers = _settings['headers']   
        self.url_login = _url_login
        self.login = _login
        self.parser = pc.MyHTMLParser(False)
        self.password =  _password 
        self.setConnection()
        
    def setConnection(self):
        self.session = requests.Session()
        self.session.headers = self.headers 
        '''
        browser = RoboBrowser(history=True)
        browser.open(self.url_login)
        form = browser.get_forms()[1]
        form['login'].value = self.login 
        form['password'].value = self.password
        browser.submit_form(form)
        '''
        
      
    def getFantasyInfo(self, tournament = None):
        session = requests.Session() 
        resp = session.get(self.settings['url_fantasy_menu'], headers = self.headers)  
        df = pd.DataFrame(data =  resp.json()['data']['items'])
        return df
    
    def getMainFantasyPage(self):
        session = requests.Session() 
        print(self.settings['url_fantasy'])
        resp = session.get(self.settings["url_fantasy"], headers = self.headers) 
        return resp
    
    def getAllTournament(self, category_id = None, key_name = None):
        if category_id != None:
            prefix = '?category_id=%d' % category_id
        else:
            prefix = ''   
        resp = requests.get(self.settings['url_tournament_all'] + prefix)  
        df = pd.DataFrame(data =  resp.json())
        if (key_name != None):
            df = df[df["name"].str.contains(key_name)]
        return df
    
 
    def getStatSeasonsById(self, tournament, season = None):
        resp = requests.get(self.settings['url_seasons'] + '?tournament=%d' % tournament)  
        df = pd.DataFrame(data =  resp.json())
        if (season != None):
            df = df[df["name"].str.contains(season)]
        return df
   
    def geSeasonsIdByKeyNameAndSeason(self, key_name, season):
        tournament = self.getAllTournament(key_name = key_name).head(1)["id"]
        season = self.getStatSeasonsById(tournament, season).any['id']
        return season

    def getPlayerInfo(self, tag):
        resp = requests.get(url_player_info + '?tag=%d' % (tag)) 
        print(self.settings['url_player_info'] + '?tag=%d' % (tag))
        return resp.json() 

    def getTourInfoById(self, tournament_id):
        resp = requests.get(self.settings['url_tournament_info'] + '?&tournament=%d' % tournament_id) 
        return resp.json()
      
    def getPlayerStat(self, tag, season_id = None, tournament_id = None):
        if (season_id == None) and (tournament_id == None):
            url = self.settings['url_player_stat'] + '?tag=%d' % tag
        else:    
            url =   self.settings['url_player_stat'] + '?tag=%d&season_id=%d&tournament_id=%d' % (tag, season_id, tournament_id)
        resp = requests.get(url) 
        #df = pd.DataFrame(data =  resp.json())
        return resp.json()

    def getPlayerStatSeason(self, tag, season_id = None, tournament_id = None):
        resp = self.getPlayerStat(tag, season_id, tournament_id)
        data = resp['all_stat']
        data['tag_id'] = tag
        return data

    def getMyTeamInfo(self, team_id):
        session = self.session
        url = self.settings['url_get']  % team_id
        print(url)
        resp = session.get(self.settings['url_get']  % team_id)
        if 'players' in resp.json():
            res = resp.json()['players']
        elif resp.status_code != 200:
            res = [{'error':'cockie was expired'}]
        else:
            res = [resp.json()]
            
        return res

    def getAllTeamInfo(self, tournament_id):
        session = self.session
        url = self.settings['url_tournaments']  % tournament_id
        print('get tournament players from url %s' % url)
        resp = session.get(url, headers = self.headers)
        res = resp.json()['players']
        df = pd.DataFrame(data =  res)
        df.set_index('id')
        return df
    
    def getMyTeamInfoAllTours(self, team_id):
        session = self.session
        url = self.settings['url_team_info']  % team_id
        #print(url)
        txt = requests.get(url).text 
                         #  "https://www.sports.ru/fantasy/football/team/%d.html",  
        #parser.tours
        #https://www.sports.ru/fantasy/football/team/2104286.html
        parser = pc.MyHTMLParser(False)
        parser.feed(txt)
        team_history = []
        #print(parser.tours)
        for tour in parser.tours:
            url = self.settings['url_points_tour']  % (team_id, parser.tours[tour])
            #print(url)
            resp = session.get(url, headers = self.headers)
            if 'players' in resp.json():
                res = resp.json()['players']
                for r in res:
                    r["tour"] = tour    
                #res = [resp.json()]    
                team_history = team_history + res
            elif resp.status_code != 200 and 'team' not in resp.json():
                res = [{'error':'cockie was expired'}]
            
                
        return pd.DataFrame(data = team_history)
    
    def getTeamsTournament(self, season_id, tournament_id, month = None):
        params = {"tournament":tournament_id,
                  "season_id":season_id,
                  "month":month 
                 }
        url = self.settings['url_tournament_calendar']
        #print(url + '?tornament=%s&season_id=%s '% (str(tournament_id), str(season_id) )
        resp = requests.get(url, params = params) 
        tag_ids = []
        for stage in resp.json():
            res = stage["matches"]
            for match in res:
                tag_ids.append(match["command1"]["tag_id"])                        
                tag_ids.append(match["command2"]["tag_id"])                 
        return list(set(tag_ids))                     

    def getTeamPlayers(self, tag):
        url = self.settings['url_team_stat_players'] + '?tag=%d' % (tag)
        print(url)
        resp = requests.get(url)
        return resp.json()["players"]
 
    def getPlayersDict(self,season_id, tournament_id, month, list_ids):
        players = {}
        teams = self.getTeamsTournament(season_id, tournament_id)
        print(teams)
        pls = []
        for team in teams:
            pl =  self.getTeamPlayers(team)
            for p in pl:
                if p['id'] in list_ids:
                    players[p['id']] = p['tag_id']     
        return players 
    
    def sendTransfers(self, transfers, team_id):
        session = requests.Session() 
        resp = session.post(self.settings['url_save']  % team_id, data = transfers, headers = self.headers)
        
        if resp.status_code != 200:
            try:
                print('team %d send %s' % (team_id, str(resp.json())) )   
                return resp.json()
            except:
                print('team %d send %s' % (team_id, resp.text))
                return resp.text
        else:
            print('team %d send %s' % (team_id, resp.text))
            return {'status':'OK'} 
         
