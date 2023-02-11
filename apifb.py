print('hi men')
class Sports:
    sports_ids=''
    sports_parentId=''
    sports_kinds=''
    sports_sortOrder=''
    sports_name=''
    sports_parentIds=''
    sports_name_tip=''


    def __init__(self):
        from classy import Jsn_txt

        categ = 'sports'

        asti = Jsn_txt(categ=categ)


        sp_id=[]
        parentId=[]
        kind=[]
        sortOrder=[]
        name=[]
        parentIds=[]
        name_tip=[]
        for astd in asti.cate:

            sport_ids=astd['id']
            sp_id.append(sport_ids)
            try:
              parentId.append(astd['parentId'])

            except:
                parentId.append('None')
            try:
                kind.append(astd['kind'])
            except:
                kind.append('None')
            try:
                sortOrder.append(astd['sortOrder'])
            except:
                sortOrder.append('None')

            try:
                name.append(astd['name'])
            except:
                name.append('None')
            try:
                parentIds.append(astd['parentIds'])
            except:
                parentIds.append('None')
            try:
                name_tip.append((str(astd['name']).split('.'))[0])
            except:
                name_tip.append('None')



        self.sports_ids=sp_id
        self.sports_parentId=parentId
        self.sports_kinds=kind
        self.sports_sortOrder=sortOrder
        self.sports_name=name
        self.sports_parentIds=parentIds
        self.sports_name_tip=name_tip




class Event:
    event_name = ""
    event_team1 = ""
    event_team1Id = ""
    event_statisticsType = ""
    event_team2 = ""
    event_specialTableId = ""
    event_team2Id = ""
    event_startTime = ""
    event_kind = ""
    event_state = ""
    event_parentId = ""
    event_priority = ""
    event_sportId = ""
    event_id = ""
    event_tv = ""
    event_info = ""
    event_notMatch = ""
    event_place = ""
    event_level = ""
    event_rootKind = ""
    event_sortOrder = ""
    event_num = ""



    def __init__(self):
        from classy import Jsn_txt
        categ = 'events'

        eva = Jsn_txt(categ=categ)


        xkkeys=[]
        place = []
        id = []
        statisticsType = []
        team1 = []
        name = []
        specialTableId = []
        team2 = []
        team1Id = []
        parentId = []
        num = []
        startTime = []
        level = []
        priority = []
        state = []
        team2Id = []
        rootKind = []
        sportId = []
        sortOrder = []
        kind = []
        notMatch = []
        info = []
        tv = []

        for evasa in eva.cate:
            try:
                sportId.append(evasa["sportId"])
            except:
                sportId.append("None")
            try:
                id.append(evasa["id"])
            except:
                id.append("None")
            try:
                state.append(evasa["state"])
            except:
                state.append("None")
            try:
                parentId.append(evasa["parentId"])
            except:
                parentId.append("None")
            try:
                tv.append(evasa["tv"])
            except:
                tv.append("None")
            try:
                team1Id.append(evasa["team1Id"])
            except:
                team1Id.append("None")
            try:
                sortOrder.append(evasa["sortOrder"])
            except:
                sortOrder.append("None")
            try:
                info.append(evasa["info"])
            except:
                info.append("None")
            try:
                notMatch.append(evasa["notMatch"])
            except:
                notMatch.append("None")
            try:
                statisticsType.append(evasa["statisticsType"])
            except:
                statisticsType.append("None")
            try:
                priority.append(evasa["priority"])
            except:
                priority.append("None")
            try:
                team2.append(evasa["team2"])
            except:
                team2.append("None")
            try:
                startTime.append(evasa["startTime"])
            except:
                startTime.append("None")
            try:
                num.append(evasa["num"])
            except:
                num.append("None")
            try:
                level.append(evasa["level"])
            except:
                level.append("None")
            try:
                kind.append(evasa["kind"])
            except:
                kind.append("None")
            try:
                rootKind.append(evasa["rootKind"])
            except:
                rootKind.append("None")
            try:
                team1.append(evasa["team1"])
            except:
                team1.append("None")
            try:
                specialTableId.append(evasa["specialTableId"])
            except:
                specialTableId.append("None")
            try:
                team2Id.append(evasa["team2Id"])
            except:
                team2Id.append("None")
            try:
                name.append(evasa["name"])
            except:
                name.append("None")
            try:
                place.append(evasa["place"])
            except:
                place.append("None")

            for xkeys in (list(evasa.keys())):
                xkkeys.append(xkeys)




        self.event_id = id
        self.event_name = name
        self.event_num = num
        self.event_notMatch = notMatch
        self.event_parentId = parentId
        self.event_team1 = team1
        self.event_statisticsType = statisticsType
        self.event_kind = kind
        self.event_rootKind = rootKind
        self.event_place = place
        self.event_priority = priority
        self.event_specialTableId = specialTableId
        self.event_sportId = sportId
        self.event_team2 = team2
        self.event_team1Id = team1Id
        self.event_startTime = startTime
        self.event_level = level
        self.event_tv = tv
        self.event_team2Id = team2Id
        self.event_sortOrder = sortOrder
        self.event_info = info
        self.event_state = state




class Sel_play:
    from apifb import Sports, Event


    evD=Event()

    index_tip =[]
    str_ids=''
    event_idos=''


    def sport_name(self,spr_name):
        from apifb import Sports, Event


        ind=[]
        id_spr=[]
        spr= Sports()

        n=0
        for spr_nam in spr.sports_name_tip:
            n+=1
            if spr_nam==spr_name:

                india=n-1
                ind.append(india)
                id_spr.append(spr.sports_ids[india])
        self.index_tip=set(ind)
        self.str_ids=id_spr




    def __init__(self, spr_name):
        from classy import Tims
        from apifb import Sports, Event
        from datetime import datetime
        t_nw=Tims().ts_nw
        self.sport_name(spr_name)




        strTime=self.evD.event_startTime
        n=0
        id_ev=[]
        for strTims in strTime:

            n+=1

            if strTims<t_nw:

                ev_id=(self.evD.event_sportId[n-1])
                id_ev.append(ev_id)
        self.event_idos=id_ev



class CustomFac:
    custom_e=''
    custom_all=''




    def __init__(self):
        from classy import Jsn_txt
        categ = 'customFactors'

        custF = Jsn_txt(categ=categ)
        cust_e=[]
        cust_all=[]
        for custom in custF.cate:
            cust_e.append(custom['e'])
            cust_all.append(custom)


        self.custom_e=cust_e
        self.custom_all=cust_all







class Sob_live:
    live_sb = []
    custom_all=[]
    index_event=[]
    sport_id=[]

    def __init__(self):
        from apifb import Event,CustomFac
        a=Event()
        cs=CustomFac()


        n=-1
        for lv in a.event_place:
            n+=1
            if lv=='live':

                self.live_sb.append(a.event_id[n])
                self.index_event.append(n)
                self.sport_id.append(a.event_sportId[n])


        for fac in self.live_sb:
            try:
              index_fac=(cs.custom_e.index(fac))
              self.custom_all.append(cs.custom_all[index_fac])
            except:
                pass




class Name_sl:
    sport_id=[]


    def __init__(self,name_sob):

        from apifb import Sob_live, Sports

        sl=Sob_live()
        sp = Sports()
        n=-1
        for xname in sp.sports_name:
            n+=1
            name = (str(xname).split('.'))[0]

            if name == name_sob:
                self.sport_id.append(sp.sports_ids[n])

        for sport in self.sport_id:
            try:
                print(sl.sport_id.index(sport))
            except:
                print('ошибка')











