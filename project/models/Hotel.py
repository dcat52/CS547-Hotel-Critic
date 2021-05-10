class Hotel(object):

    def __init__(self):
        self.num_of_reviews = 0
        self.avg_rating = {}
        self.name = ''
        self.price = ''
        self.address = ''
        # self.city = ''
        # self.state = ''
        self.us = 0
        self.id = ''

    def __str__(self):
        return '{:40s}, Overall: {:.2f} '.format(self.name, self.avg_rating['Overall'])

    def __repr__(self):
        return '\n{}'.format(str(self))
