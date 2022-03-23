import requests, json, time, progressbar


def scanSummoner(api_key,summoner_name):

    urlName = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name + "?api_key=" + api_key
    # On créer l'url avec le nom du joueur et la clée de l'API

    response1 = requests.get(urlName)
    summoner_name = response1.json()['name']
    idSummoner = response1.json()['id']
    puuidSummoner = response1.json()['puuid']
    levelSummoner = response1.json()['summonerLevel']
    # On interroge l'API et on donne les valeurs à des variables

    sF = 0
    startFrom = str(sF)
    urlHistoriqueMatchs = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuidSummoner + "/ids?queue=420&start=" + startFrom + "&count=100"+ "&api_key=" + api_key
    # On créer l'url qui cherche les 100 derniers matchs de solo q à partir de countFrom

    sF = 0
    startFrom = str(sF)
    urlHistoriqueMatchs = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuidSummoner + "/ids?queue=420&start=" + startFrom + "&count=100"+ "&api_key=" + api_key
    # On créer l'url qui cherche les 100 derniers matchs de solo q à partir de countFrom

    gamesIds = []
    # Une liste pour accueuillir les ID de toutes les games et une pour accueuillir celles que renvoie l'API

    i = 0
    while i < 1:
        response2 = requests.get(urlHistoriqueMatchs)
        gamesIdsResponses = response2.json()
    # On interroge l'url précédente
        
        if not (gamesIdsResponses):
            i = 1    
    # Si la liste de la requête que renvoie l'API est vide la fonction s'arrete 

        else:
            gamesIds = gamesIds + gamesIdsResponses
            sF = sF + 100
            startFrom = str(sF)
            urlHistoriqueMatchs = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuidSummoner + "/ids?queue=420&start=" + startFrom + "&count=100"+ "&api_key=" + api_key
    # On explore la liste de l'API 100 par 100 

    # On obtient la liste complète des IDs de toutes les dernières games en soloq disponibles via l'API dans gamesIds
    totalGames = len(gamesIds)
    # On obtient le nombre total de games

    championsDict = {}
    positionsDict = {}
    totalGamesDict = {}
    last10Games = {}
    # On créer les dictionnaires qui vont accueillir les stats du joueur par champion / position / games totales / 10 dernières

    addIt = 0
    for i in progressbar.progressbar(range(totalGames)):
        time.sleep(1.3)
    # On delay la boucle pour pas être limité par l'API
        
        urlGameId = "https://europe.api.riotgames.com/lol/match/v5/matches/" + gamesIds[i] + "?api_key=" + api_key
        response3 = requests.get(urlGameId)
    # On créer l'URL qui interroge l'API avec l'ID de la game
        
        participantId = response3.json()['metadata']['participants'].index(puuidSummoner)
    # On trouve le numero de participant du joueur
        gameDuration = response3.json()['info']['participants'][participantId]['timePlayed']
        gameDurationMin = response3.json()['info']['participants'][participantId]['timePlayed'] // 60
        gameDurationResteSec = response3.json()['info']['gameDuration'] % 60
       
    # variable qui ajoute une game au dict 10lastgames si un remake est présent
        if gameDuration < 270:
            addIt = addIt + 1
            pass
    # On demande si la game a durée plus de 270secondes pour savoir si c'est un remake
        else:
            championName = response3.json()['info']['participants'][participantId]['championName']
            kills = response3.json()['info']['participants'][participantId]['kills']
            deaths = response3.json()['info']['participants'][participantId]['deaths']
            assists = response3.json()['info']['participants'][participantId]['assists']
            farm = response3.json()['info']['participants'][participantId]['totalMinionsKilled'] + response3.json()['info']['participants'][participantId]['neutralMinionsKilled']
        
            csMin = farm / gameDurationMin
            teamPosition = response3.json()['info']['participants'][participantId]['teamPosition']
            teamId = response3.json()['info']['participants'][participantId]['teamId']
            if teamId == 100:
                teamId2 = 0
            else:
                teamId2 = 1
            totalTeamKills = response3.json()['info']['teams'][teamId2]['objectives']['champion']['kills']
            try:
                killParticipation = ((kills + assists) / totalTeamKills) * 100
            except:
                killParticipation = 0
            visionScore = response3.json()['info']['participants'][participantId]['visionScore']
            win = response3.json()['info']['participants'][participantId]['win']
            if win == True:
                win1 = 1
            else:
                win1 = 0
    # On request toutes les données qui nous interesse

            if championName in championsDict:
                championsDict[championName][0] = championsDict[championName][0] + kills
                championsDict[championName][1] = championsDict[championName][1] + deaths
                championsDict[championName][2] = championsDict[championName][2] + assists
                championsDict[championName][3] = championsDict[championName][3] + farm
                championsDict[championName][4] = championsDict[championName][4] + csMin
                championsDict[championName][5] = championsDict[championName][5] + killParticipation
                championsDict[championName][6] = championsDict[championName][6] + visionScore
                championsDict[championName][7] = championsDict[championName][7] + win1
                championsDict[championName][8] = championsDict[championName][8] + 1
            else:
                championsDict[championName] = [kills, deaths, assists, farm, csMin, killParticipation, visionScore, win1, 1]
    # On les classe en les regroupant par champion

            if teamPosition in positionsDict:
                positionsDict[teamPosition][0] = positionsDict[teamPosition][0] + kills
                positionsDict[teamPosition][1] = positionsDict[teamPosition][1] + deaths
                positionsDict[teamPosition][2] = positionsDict[teamPosition][2] + assists
                positionsDict[teamPosition][3] = positionsDict[teamPosition][3] + farm
                positionsDict[teamPosition][4] = positionsDict[teamPosition][4] + csMin
                positionsDict[teamPosition][5] = positionsDict[teamPosition][5] + killParticipation
                positionsDict[teamPosition][6] = positionsDict[teamPosition][6] + visionScore
                positionsDict[teamPosition][7] = positionsDict[teamPosition][7] + win1
                positionsDict[teamPosition][8] = positionsDict[teamPosition][8] + 1
            else:
                positionsDict[teamPosition] = [kills, deaths, assists, farm, csMin, killParticipation, visionScore, win1, 1]
    # On les classe en les regroupant par role

            if 'allGames' in totalGamesDict:
                totalGamesDict['allGames'][0] = totalGamesDict['allGames'][0] + kills
                totalGamesDict['allGames'][1] = totalGamesDict['allGames'][1] + deaths
                totalGamesDict['allGames'][2] = totalGamesDict['allGames'][2] + assists
                totalGamesDict['allGames'][3] = totalGamesDict['allGames'][3] + farm
                totalGamesDict['allGames'][4] = totalGamesDict['allGames'][4] + csMin
                totalGamesDict['allGames'][5] = totalGamesDict['allGames'][5] + killParticipation
                totalGamesDict['allGames'][6] = totalGamesDict['allGames'][6] + visionScore
                totalGamesDict['allGames'][7] = totalGamesDict['allGames'][7] + win1
                totalGamesDict['allGames'][8] = totalGamesDict['allGames'][8] + 1
            else:
                totalGamesDict['allGames'] = [kills, deaths, assists, farm, csMin, killParticipation, visionScore, win1, 1]
    # Et on les classe avec le total sur toutes les games
            
            if i < 10 + addIt:
                last10Games[i] = [championName, kills, deaths, assists, farm, csMin, killParticipation, visionScore, win]

    mostPlayedChampions = sorted(championsDict.items(), key=lambda t: t[1][8], reverse=True)
    mostPlayedChampionsDict = {}
    totalChampPlayed = len(mostPlayedChampions)
    # On tri le premier dictionnaire par champions les plus joués
    mostPlayedChampionsIndex = {}
    # Et un qui accueille l'index des champions les plus joués
    for i in range(totalChampPlayed):
        try:
            kda = round((mostPlayedChampions[i][1][0] + mostPlayedChampions[i][1][2]) / mostPlayedChampions[i][1][1],2)
        except:
            kda = 'Perfect '
        mostPlayedChampionsDict[i] = [round(mostPlayedChampions[i][1][0] / mostPlayedChampions[i][1][8],1), round(mostPlayedChampions[i][1][1] / mostPlayedChampions[i][1][8],1), round(mostPlayedChampions[i][1][2] / mostPlayedChampions[i][1][8],1), kda, round(mostPlayedChampions[i][1][3] / mostPlayedChampions[i][1][8],1), round(mostPlayedChampions[i][1][4] / mostPlayedChampions[i][1][8],1), round(mostPlayedChampions[i][1][5] / mostPlayedChampions[i][1][8]), round(mostPlayedChampions[i][1][6] / mostPlayedChampions[i][1][8]), mostPlayedChampions[i][1][7], mostPlayedChampions[i][1][8] - mostPlayedChampions[i][1][7], mostPlayedChampions[i][1][8], round((mostPlayedChampions[i][1][7] / mostPlayedChampions[i][1][8])*100)]
    # On transfère les données dans un nouveau dict en créeant les nouvelles données
    # Format : 'Champion' : [kills, deaths, assists, KDA, farm, cs/min, kill participation, score de vision, wins, loses , jouées, winrate]    
        mostPlayedChampionsIndex[i] = mostPlayedChampions[i][0]
    #  Format : {0:'champion1', 1: 'champion2', 2:'champion3' etc..}
    

    mostPlayedPosition = sorted(positionsDict.items(), key=lambda t: t[1][8], reverse=True)
    mostPlayedPositionDict = {}
    totalPositionPlayed = len(mostPlayedPosition)
    # On tri le deuxieme dictionnaire par roles les plus joués
    mostPlayedPositionIndex = {}
    # Et un qui accueille l'index des positions les plus jouées
    for i in range(totalPositionPlayed):
        try:
            kda = round((mostPlayedPosition[i][1][0] + mostPlayedPosition[i][1][2]) / mostPlayedPosition[i][1][1],2)
        except:
            kda = 'Perfect '
        mostPlayedPositionDict[i] = [round(mostPlayedPosition[i][1][0] / mostPlayedPosition[i][1][8],1), round(mostPlayedPosition[i][1][1] / mostPlayedPosition[i][1][8],1), round(mostPlayedPosition[i][1][2] / mostPlayedPosition[i][1][8],1), kda, round(mostPlayedPosition[i][1][3] / mostPlayedPosition[i][1][8],1), round(mostPlayedPosition[i][1][4] / mostPlayedPosition[i][1][8],1), round(mostPlayedPosition[i][1][5] / mostPlayedPosition[i][1][8]), round(mostPlayedPosition[i][1][6] / mostPlayedPosition[i][1][8]), mostPlayedPosition[i][1][7], mostPlayedPosition[i][1][8] - mostPlayedPosition[i][1][7], mostPlayedPosition[i][1][8], round((mostPlayedPosition[i][1][7] / mostPlayedPosition[i][1][8])*100)]
    # Format : 'ROLE' : [kills, deaths, assists, KDA, farm, cs/min, kill participation, score de vision, wins, loses , jouées, winrate]
        mostPlayedPositionIndex[i] = mostPlayedPosition[i][0]
    #  Format : {0:'position1', 1: 'position2', 2:'position3' etc..}

    totalPlayedGames = sorted(totalGamesDict.items(), key=lambda t: t[1][8], reverse=True)
    totalPlayedGamesDict = {}
    totalPlayedGamesDict[totalPlayedGames[0][0]] = [round(totalPlayedGames[0][1][0] / totalPlayedGames[0][1][8],1), round(totalPlayedGames[0][1][1] / totalPlayedGames[0][1][8],1), round(totalPlayedGames[0][1][2] / totalPlayedGames[0][1][8],1), round((totalPlayedGames[0][1][0] + totalPlayedGames[0][1][2]) / totalPlayedGames[0][1][1],2), round(totalPlayedGames[0][1][3] / totalPlayedGames[0][1][8],1), round(totalPlayedGames[0][1][4] / totalPlayedGames[0][1][8],1), round(totalPlayedGames[0][1][5] / totalPlayedGames[0][1][8]), round(totalPlayedGames[0][1][6] / totalPlayedGames[0][1][8]), totalPlayedGames[0][1][7], totalPlayedGames[0][1][8] - totalPlayedGames[0][1][7], totalPlayedGames[0][1][8], round((totalPlayedGames[0][1][7] / totalPlayedGames[0][1][8])*100)]
    # Format : 'allGames' : [kills, deaths, assists, KDA, farm, cs/min, kill participation, score de vision, wins, loses , jouées, winrate]

    last10GamesDict = {}
    # Dictionnaire qui accueille les 10 dernières parties

    y = 0
    for i in range(10):
        if i+y in last10Games:
            try:
                kda = round((last10Games[i+y][1] + last10Games[i+y][3]) / last10Games[i+y][2],2)
            except:
                kda = 'Perfect '
            last10GamesDict[i] = [last10Games[i+y][0], last10Games[i+y][1], last10Games[i+y][2], last10Games[i+y][3], kda, last10Games[i+y][4], round(last10Games[i+y][5],1), round(last10Games[i+y][6]), last10Games[i+y][7], last10Games[i+y][8]]
        else:
            y = y + 1
            try:
                kda = round((last10Games[i+y][1] + last10Games[i+y][3]) / last10Games[i+y][2],2)
            except:
                kda = 'Perfect '
            last10GamesDict[i] = [last10Games[i+y][0], last10Games[i+y][1], last10Games[i+y][2], last10Games[i+y][3], kda, last10Games[i+y][4], round(last10Games[i+y][5],1), round(last10Games[i+y][6]), last10Games[i+y][7], last10Games[i+y][8]]
            
    # Format : Numero de game : ['Champion', kills, deaths, assists, KDA, farm, cs/min, kill participation, score de vision, win/lose]

    urlSummonerRank = "https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + idSummoner + "?api_key=" + api_key
    response4 = requests.get(urlSummonerRank)
    # On créer l'url et on interroge son rank dans les files classées

    try :
        try:
            response4.json()[0]['queueType'].index('RANKED_SOLO_5x5')
            tierSummoner = response4.json()[0]['tier']
            rankSummoner = response4.json()[0]['rank']
            leaguePointsSummoner = response4.json()[0]['leaguePoints']
            winsSummoner = response4.json()[0]['wins']
            lossesSummoner = response4.json()[0]['losses']
            totalGamesSummoner = response4.json()[0]['wins'] + response4.json()[0]['losses']
            winrateSummoner = round((response4.json()[0]['wins'] / (response4.json()[0]['wins'] + response4.json()[0]['losses'])) * 100)
        
        except:
            response4.json()[1]['queueType'].index('RANKED_SOLO_5x5')
            tierSummoner = response4.json()[1]['tier']
            rankSummoner = response4.json()[1]['rank']
            leaguePointsSummoner = response4.json()[1]['leaguePoints']
            winsSummoner = response4.json()[1]['wins']
            lossesSummoner = response4.json()[1]['losses']
            totalGamesSummoner = response4.json()[1]['wins'] + response4.json()[1]['losses']
            winrateSummoner = round((response4.json()[1]['wins'] / (response4.json()[1]['wins'] + response4.json()[1]['losses'])) * 100)
    except:
        tierSummoner = 'UNRANKED'
        rankSummoner = ''
        leaguePointsSummoner = 0
        winsSummoner = ''
        lossesSummoner = ''
        totalGamesSummoner = ''
        winrateSummoner = ''
      
    # On créer une fonction qui cherche ses stats en soloq et qui récupère ses stats
    return summoner_name, levelSummoner, tierSummoner, rankSummoner, leaguePointsSummoner, winsSummoner, lossesSummoner, totalGamesSummoner, winrateSummoner, mostPlayedChampionsIndex, mostPlayedChampionsDict, mostPlayedPositionIndex, mostPlayedPositionDict, last10GamesDict, totalPlayedGamesDict,
    
def scanGroup(api_key, summonerList):
    results = {}
    for i in range(len(summonerList)):
        results[i] = scanSummoner(api_key, summonerList[i])
    return results

