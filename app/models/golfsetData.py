from app import db
from models.users import User
import math

class ClubHead(db.Document):
    meta = {'abstract' : True, 'allow_inheritance': True}
    loft = db.FloatField() 
    weight = db.IntField()

    def getLoft(self):
        return self.loft

    def getMaterialClass(self):
        return type(self).__name__


class WoodHead(ClubHead):
    meta = {'collection' : 'woodheadClub'}
    size = db.IntField()
    
    @staticmethod
    def createWoodHead(loft, weight, size):
        woodHead = WoodHead.objects(loft=loft, weight=weight).first()
        if not woodHead:
             woodHead = WoodHead(loft=loft, weight=weight, size=size).save()
        return woodHead

    def getSize(self):
        return self.size

class IronHead(ClubHead):
    meta = {'collection' : 'ironheadClub'}
    material = db.StringField()
    
    @staticmethod
    def createIronHead(loft, weight, material):
        ironHead = IronHead.objects(loft=loft, weight=weight).first()
        if not ironHead:
             ironHead = IronHead(loft=loft, weight=weight, material=material).save()
        return ironHead

class PutterHead(ClubHead):
    meta = {'collection' : 'putterheadClub'}
    style = db.StringField()
    
    @staticmethod
    def createPutterHead(loft, weight, style):
        putterHead = PutterHead.objects(loft=loft, weight=weight).first()
        if not putterHead:
             putterHead = PutterHead(loft=loft, weight=weight, style=style).save()
        return putterHead

    def getStyle(self):
        return self.style
    
class Shaft(db.Document):
    meta = {'collection': 'shafts'}
    length = db.FloatField()
    weight = db.IntField()
    material = db.StringField()
    flex = db.StringField()

    @staticmethod
    def createShaft(length, weight, material, flex):
        shaft = Shaft.objects(length=length, weight=weight, material=material, flex=flex).first()
        if not shaft:
            shaft = Shaft(length=length, weight=weight, material=material, flex=flex).save()
        return shaft

    def getLength(self):
        return self.length

class Grip(db.Document):
    meta = {'collection': 'grip'}
    diameter = db.FloatField()
    weight = db.IntField()
    material = db.StringField()

    @staticmethod
    def createGrip(diameter, weight, material):
        grip = Grip.objects(diameter=diameter, weight=weight, material=material).first()
        if not grip:
            grip = Grip(diameter=diameter, weight=weight, material=material).save()
        return grip

class Club(db.Document):
    meta = {'collection': 'clubs'}
    label = db.StringField()
    head = db.ReferenceField(ClubHead)
    shaft = db.ReferenceField(Shaft)
    grip = db.ReferenceField(Grip)

    @staticmethod
    def createClub(dataList):
        club = Club.objects(label=dataList[0]).first()

        if not club:
            if dataList[1].strip() == "Wood":
                head = WoodHead.createWoodHead(float(dataList[2]), int(dataList[3]), int(dataList[4]))
            elif dataList[1].strip() == "Iron":
                head = IronHead.createIronHead(float(dataList[2]), int(dataList[3]), str(dataList[4]))
            elif dataList[1].strip() == "Putter":
                head = PutterHead.createPutterHead(float(dataList[2]), int(dataList[3]), str(dataList[4]))

            shaft = Shaft.createShaft(float(dataList[5]), int(dataList[6]), str(dataList[7]), str(dataList[8]))
            grip = Grip.createGrip(float(dataList[9]), int(dataList[10]), str(dataList[11]))
            club = Club(label=dataList[0], head=head, shaft=shaft, grip=grip).save()
   
        return club

    def getClubsize(self):
        return self.head.getSize()

    def getClubstyle(self):
        return self.head.getStyle()

    def getShaftlength(self):
        return self.shaft.getLength()

    def getClubHeadloft(self):
        return self.head.getLoft()

    def getClubMaterial(self):
        return self.head.getMaterialClass()

class GolfSet(db.Document):
    meta = {'collection': 'golfSets'}
    golfer = db.ReferenceField(User)
    clubs = db.DictField()
    
    @staticmethod 
    def createGolfSet(email):
        golfer = User.objects(email=email).first()
        if golfer:
            golfSet = GolfSet.objects(golfer=golfer).first()
            if not golfSet:
                golfSet = GolfSet(golfer=golfer, clubs={}).save()
            return golfSet

    def addClub(self,club):
        if club.label in self.clubs: #if club is found in the clubs dictionary
            return False
        self.clubs[club.label] = club
        self.save()
        return True

    def getClub(self,label):
        return self.clubs.get(label)

    def getAllClubs(self):
        return self.clubs

    @staticmethod
    def getGolfSetByEmail(email):
        golfer = User.getUser(email)
        if golfer:
            return GolfSet.objects(golfer=golfer).first()
        else:
            return None

class Swing(db.Document):
    meta = {'collection': 'swings'}
    golfer = db.ReferenceField(User)
    swing_datetime = db.DateTimeField(['%Y-%m-%d %h:%M'])
    club = db.ReferenceField(Club)
    swingSpeed = db.FloatField()
    distance = db.FloatField()
    
    @staticmethod 
    def createSwing(golfer, swing_datetime, club, swingSpeed, distance):
        swing = Swing.objects(golfer=golfer, swing_datetime=swing_datetime, club=club, swingSpeed=swingSpeed, distance=distance).first()
        if not swing:
            swing = Swing(golfer=golfer, swing_datetime=swing_datetime, club=club, swingSpeed=swingSpeed, distance=distance).save()
            print("added") 
        return swing
    
    @staticmethod
    def getClubLength(club):
        #print(club.getClubMaterial())
        #compute club_head_height
        if club.getClubMaterial() == "WoodHead":
            club_head_height = club.getClubsize() / 400
        elif club.getClubMaterial() == "IronHead":
            club_head_height = 1
        elif club.getClubMaterial() == "PutterHead":
            if club.getClubstyle() == "Blade":
                club_head_height = 1
            else:
                club_head_height = 0.5
        else:
            return False

        #compute club_length
        club_length = club_head_height + club.getShaftlength()

        return club_length

    @staticmethod
    def computeDistance(club,swingSpeed):
        
        club_length = Swing.getClubLength(club)
        #compute estimated_distance
        club_head_loft = club.getClubHeadloft()
        estimated_distance = (280 - abs(48- int(club_length))*10 - abs(int(club_head_loft) - 10)*1.25) * int(swingSpeed)/96

        return estimated_distance

    
        


        