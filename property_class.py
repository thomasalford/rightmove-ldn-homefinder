

class Property():
    def __init__(self, bednumber, rent, link, agent, address, postcode, floorplan):
        self.beds = bednumber
        self.rent = f'{rent:,}'
        self.link = link
        self.agent = agent
        self.address = address
        self.postcode = postcode
        self.floorplan = floorplan
        self.pcm = round(rent / bednumber, 2)

    def serialize(self):
        return self.__dict__
