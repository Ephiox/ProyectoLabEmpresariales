class AtheleteList(list):
    def __init__(self, name='', dob='', times=[]):
        super().__init__([])
        self.name = name
        self.dob = dob
        self.times = times

    def fast3times(self):
        results = sorted(self.times)
        return results[0:3]

    def add_one_time(self, a_time):
        self.times.append(a_time)

    def add_times(self, list_times):
        self.times.extend(list_times)


vera = AtheleteList('Vera Vi')
vera.add_times(['2.13', '2.12', '3.01', '4.5'])
print(vera.fast3times())

