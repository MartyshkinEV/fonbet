CLOBAL="GLOBAL"

class Requets_Id:
    requestId=''

    def __init__(self):
        from betconfig import headers, fsing, clientId, deviceId, betRequestId, data_betRequestId
        import requests

        response = requests.post(betRequestId, headers=headers, data=data_betRequestId)
        jresponse = response.json()
        print(jresponse)
        #
        self.requestId = jresponse['requestId']


class Bets_Info:
    sums = ''
    sums = ''
    bonusBets = ''
    ifnobet_id = ''
    ifnobet_rootId = ''
    ifnobet_kindName = ''
    ifnobet_kind = ''
    ifnobet_rootKind = ''
    ifnobet_sportId = ''
    ifnobet_competitionId = ''
    ifnobet_competitionName = ''
    ifnobet_startTime = ''
    ifnobet_team1Id = ''
    ifnobet_team2Id = ''
    ifnobet_team1 = ''
    ifnobet_team2 = ''
    ifnobet_rootTeam1Id = ''
    ifnobet_rootTeam2Id = ''
    ifnobet_rootTeam1 = ''
    ifnobet_rootTeam2 = ''
    ifnobet_name = ''
    ifnobet_rootName = ''
    ifnobet_place = ''
    ifnobet_timer = ''
    ifnobet_timerSeconds = ''
    ifnobet_timerDirection = ''
    ifnobet_score = ''
    ifnobet_betIncompatible = ''
    ifnobet_timerTimestamp = ''
    ifnobet_timerTimestampMsec = ''
    infofac_id = ''
    infofac_v = ''
    infofac_blocked = ''
    infofac_couponFactorCaption = ''
    infofac_couponChoiceCaption = ''
    infofac_couponFactorCaptionParametered = ''
    infofac_couponChoiceCaptionParametered = ''
    betis=''

    def __init__(self, e_event, factor_f):
        import requests
        from betconfig import fsing, headers,deviceId

        data = '''{"sysId":1,"clientId":20211191,''' + f'"fsid":"{fsing}",' + '"lang":"ru","bets":[{''' + f'''"place":"live","factorId":{factor_f},"eventId":{e_event}''' + '''}],"CDI":0,"deviceId":'''+f'"{deviceId}'+'''"}'''


        response = requests.post('https://clientsapi04w.bk6bba-resources.com/coupon/betSlipInfo', headers=headers,
                                 data=data)


        try:
            bets=response.json()['bets']
            self.betis=bets
        except:
            pass
        try:
         self.bonusBets=response.json()['bonusBets']
        except:
            pass
        try:
            self.sums=response.json()['sums']
        except:
            pass
        try:
            event = bets[0]['event']
            factor = (bets[0]['factor'])
        except:
            pass
        # for x in factor:
        #
        #
        #     print(f"try:\n   self.infofac_{x}.append(factor['{x}'])\nexcept:\n   self.infofac_{x}.append('None')  ")

        try:
            self.infofac_id = factor['id']
        except:
            self.infofac_id = 'None'
        try:
            self.infofac_v = factor['v']
        except:
            self.infofac_v = 'None'
        try:
            self.infofac_couponFactorCaption = factor['couponFactorCaption']
        except:
            self.infofac_couponFactorCaption = 'None'
        try:
            self.infofac_couponChoiceCaption = factor['couponChoiceCaption']
        except:
            self.infofac_couponChoiceCaption = 'None'
        try:
            self.infofac_couponFactorCaptionParametered = factor['couponFactorCaptionParametered']
        except:
            self.infofac_couponFactorCaptionParametered = 'None'
        try:
            self.infofac_couponChoiceCaptionParametered = factor['couponChoiceCaptionParametered']
        except:
            self.infofac_couponChoiceCaptionParametered = 'None'

        try:
            self.ifnobet_id = event['id']
        except:
            self.ifnobet_id = 'None'
        try:
            self.ifnobet_rootId = event['rootId']
        except:
            self.ifnobet_rootId = 'None'
        try:
            self.ifnobet_kindName = event['kindName']
        except:
            self.ifnobet_kindName = 'None'
        try:
            self.ifnobet_kind = event['kind']
        except:
            self.ifnobet_kind = 'None'
        try:
            self.ifnobet_rootKind = event['rootKind']
        except:
            self.ifnobet_rootKind = 'None'
        try:
            self.ifnobet_sportId = event['sportId']
        except:
            self.ifnobet_sportId = 'None'
        try:
            self.ifnobet_competitionId = event['competitionId']
        except:
            self.ifnobet_competitionId = 'None'
        try:
            self.ifnobet_competitionName = event['competitionName']
        except:
            self.ifnobet_competitionName = 'None'
        try:
            self.ifnobet_startTime = event['startTime']
        except:
            self.ifnobet_startTime = 'None'
        try:
            self.ifnobet_team1Id = event['team1Id']
        except:
            self.ifnobet_team1Id = 'None'
        try:
            self.ifnobet_team2Id = event['team2Id']
        except:
            self.ifnobet_team2Id = 'None'
        try:
            self.ifnobet_team1 = event['team1']
        except:
            self.ifnobet_team1 = 'None'
        try:
            self.ifnobet_team2 = event['team2']
        except:
            self.ifnobet_team2 = 'None'
        try:
            self.ifnobet_rootTeam1Id = event['rootTeam1Id']
        except:
            self.ifnobet_rootTeam1Id = 'None'
        try:
            self.ifnobet_rootTeam2Id = event['rootTeam2Id']
        except:
            self.ifnobet_rootTeam2Id = 'None'
        try:
            self.ifnobet_rootTeam1 = event['rootTeam1']
        except:
            self.ifnobet_rootTeam1 = 'None'
        try:
            self.ifnobet_rootTeam2 = event['rootTeam2']
        except:
            self.ifnobet_rootTeam2 = 'None'
        try:
            self.ifnobet_name = event['name']
        except:
            self.ifnobet_name = 'None'
        try:
            self.ifnobet_rootName = event['rootName']
        except:
            self.ifnobet_rootName = 'None'
        try:
            self.ifnobet_place = event['place']
        except:
            self.ifnobet_place = 'None'
        try:
            self.ifnobet_timer = event['timer']
        except:
            self.ifnobet_timer = 'None'
        try:
            self.ifnobet_timerSeconds = event['timerSeconds']
        except:
            self.ifnobet_timerSeconds = 'None'
        try:
            self.ifnobet_timerDirection = event['timerDirection']
        except:
            self.ifnobet_timerDirection = 'None'
        try:
            self.ifnobet_timerTimestamp = event['timerTimestamp']
        except:
            self.ifnobet_timerTimestamp = 'None'
        try:
            self.ifnobet_timerTimestampMsec = event['timerTimestampMsec']
        except:
            self.ifnobet_timerTimestampMsec = 'None'
        try:
            self.ifnobet_score = event['score']
        except:
            self.ifnobet_score = 'None'
        try:
            self.ifnobet_betIncompatible = event['betIncompatible']
        except:
            self.ifnobet_betIncompatible = 'None'


# Bets_Info('35214573','921')

class Stav_bet:
    coupon_resultCode = ""
    coupon_regTime = ""
    coupon_bets_event = ""
    coupon_bets = ""
    coupon_clientSaldo = ""
    coupon_amountMax = ""
    coupon_checkCode = ""
    coupon_bets_value = ""
    coupon_amountMin = ""
    coupon_bonusAccountClientSaldo = ""
    coupon_amount = ""
    coupon_bets_factor = ""
    coupon_regId = ""
    result = ""
    coupon_bets_score = ""
    coupon_bonusAccountAmount = ""


    def __init__(self, event_id, fac_id,amount):
        from betconfig import fsing, headers,deviceId
        import requests
        import traceback
        from sqlmyskr import Inser_into_one
        import time
        from bet import Requets_Id

        requestId=Requets_Id().requestId
        print(requestId)
        a=Bets_Info(event_id,fac_id)



        print('-------',requestId)


        data = '{"sysId":1,"clientId":20211191,' + \
                f'"fsid":"{fsing}","requestId":{requestId}' + \
                ',"coupon":{"'+f'amount":{amount}'+',"flexParam":false,"flexBet":"any","bets":[{' \
                + f'"num":1,"event":{a.ifnobet_id},"factor":{a.infofac_id},"value":{a.infofac_v}, "score":"{a.ifnobet_score}"'\
                + '}],"mirror":"https://www.fon.bet"},"lang":"ru","CDI":0,"deviceId":'+f'"{deviceId}"'+'}'

        print(data)

        try:
            insert_in = (requestId, amount, a.ifnobet_id, a.infofac_id, a.infofac_v)
            Inser_into_one('betResult', 'requestId ,amount , ifnobet_id, infofac_id , infofac_v ', '?,?,?,?,?',
                           insert_in)
            response = requests.post('https://clientsapi52w.bk6bba-resources.com/coupon/bet', headers=headers,
                                     data=data)
            print(response.json())
            result = response.json()['result']
            print('ставка сделана')
        except:
            print(f'Ошибка ставки:\n', traceback.format_exc())












        time.sleep(10)
        try:
            coupon = response.json()['coupon']

            self.coupon_resultCode = coupon["resultCode"]
            self.coupon_regId = coupon["regId"]
            self.coupon_checkCode = coupon["checkCode"]
            self.coupon_regTime = coupon["regTime"]
            self.coupon_clientSaldo = coupon["clientSaldo"]
            self.coupon_bonusAccountClientSaldo = coupon["bonusAccountClientSaldo"]
            self.coupon_bonusAccountAmount = coupon["bonusAccountAmount"]
            self.coupon_amountMin = coupon["amountMin"]
            self.coupon_amountMax = coupon["amountMax"]
            self.coupon_amount = coupon["amount"]
            self.coupon_bets_event = coupon["bets"][0]["event"]
            self.coupon_bets_factor = coupon["bets"][0]["factor"]
            self.coupon_bets_value = coupon["bets"][0]["value"]
            self.coupon_bets_score = coupon["bets"][0]["score"]
        except:
            print('Ошибка:\n', traceback.format_exc())




#
# Stav_bet('35211786','921','70')

class betResult:


    def __init__(self, requestId):
        from betconfig import headers,deviceId


        import requests

        data = '{"sysId":1,"clientId":20211191,"fsid":"ogWFF9sq4yhzCLqKyCoDebpr",'+f'"requestId":{requestId}'+',"lang":"ru","CDI":0,"deviceId":'+f'"{deviceId}"'+'}'

        response = requests.post('https://clientsapi31w.bk6bba-resources.com/coupon/betResult', headers=headers,
                                                             data=data)

        j_resp=response.json()
        print('betResult',j_resp)


def Proverka_bet(event_id, factor_id):
    from connt import conn, cursor

    cursor.execute('''SELECT * FROM  betResult WHERE ifnobet_id=? and infofac_id=? ''',(event_id,factor_id,))
    cur=cursor.fetchall()
    if (len(cur))==0:
        return 0
    else:
        return 1



