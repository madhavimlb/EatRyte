
class actualNutrition:
    physicalActivityFactor_dict = {'average amount of activity': 1.2, 'high amount of activity': 1.5,'low amount of activity': 1}

    def __init__(self,sex,height,weight,age,physicalActivity):
        self.s=sex
        self.h=height
        self.w=weight
        self.a=age

    def calulateCalorieNeeds(self):
        if self.s=='Male':
            male_BEE = 66.5 + 13.8*self.w + 5.0*self.h - 6.8*self.a
            physicalActivityFactor=actualNutrition.physicalActivityDict[self.physicalActivity]
            male_BEE= male_BEE*physicalActivityFactor
            return male_BEE

        elif self.s=='Female':
            Women_BEE = 655.1 + 9.6*self.w + 1.9*self.h - 4.7*self.a
            physicalActivityFactor = actualNutrition.physicalActivityDict[self.physicalActivity]
            Women_BEE = Women_BEE * physicalActivityFactor
            return Women_BEE

    def calulateProteinNeeds(self):
        protien_lowerLimit=self.w/2.2 * .8
        protien_upperLimit = self.w / 2.2 * 1.0
        protienNeeds = [protien_lowerLimit,protien_upperLimit]
        return protienNeeds

    def calculateCarbsNeeds(self):
        cal = self.calulateCalorieNeeds()
        carbs_upperLimit = 45/100*cal
        carbs_upperLimit=60/100*cal
        carbsNeeds = [carbs_upperLimit, carbs_upperLimit]

    def calculateFasNeeds(self):
        cal = self.calulateCalorieNeeds()
        fat_Required = cal*0.30/9
        return fat_Required








