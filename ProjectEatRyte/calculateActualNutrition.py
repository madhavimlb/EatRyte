class actualNutrition:
    physicalActivityFactor_dict = {'average amount of activity': 1.2, 'high amount of activity': 1.5,
                                   'low amount of activity': 1}

    def __init__(self, sex, height, weight, age, physicalActivity):
        self.s = sex
        self.h = height
        self.w = weight
        self.a = age
        self.physicalActivity = physicalActivity

    def calulateCalorieNeeds(self):
        # print(' carbs male')
        if self.s == 'Male':
            print(type(self.a))
            print(type(self.h))
            print(type(self.w))
            print(type(int(self.h)))
            male_BEE = 66.5 + 13.8 * int(self.w) + 5.0 * int(self.h) - 6.8 * int(self.a)
            physicalActivityFactor = actualNutrition.physicalActivityFactor_dict[self.physicalActivity]
            male_BEE = male_BEE * physicalActivityFactor
            return male_BEE

        elif self.s == 'Female':
            # print(' carbs female')
            Women_BEE = 655.1 + 9.6 * int(self.w) + 1.9 * int(self.h) - 4.7 * int(self.a)
            physicalActivityFactor = actualNutrition.physicalActivityFactor_dict[self.physicalActivity]
            Women_BEE = Women_BEE * physicalActivityFactor
            return Women_BEE

    def calulateProteinNeeds(self):
        protien_lowerLimit = (int(self.w) / 2.2) * .8
        protien_upperLimit = (int(self.w) / 2.2) * 1.0
        protienNeeds = [protien_lowerLimit, protien_upperLimit]
        return protienNeeds

    def calculateCarbsNeeds(self):
        print('cabs')
        cal = self.calulateCalorieNeeds()

        print(cal)
        carbs_lowerLimit = (45 / 100 * cal) / 4
        carbs_upperLimit = (60 / 100 * cal) / 4
        carbsNeeds = [carbs_lowerLimit, carbs_upperLimit]
        return carbsNeeds

    def calculateFasNeeds(self):
        cal = self.calulateCalorieNeeds()
        fat_Required = cal * 0.30 / 9
        return fat_Required
