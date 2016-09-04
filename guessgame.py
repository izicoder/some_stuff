class Game:
    def __init__(self):
        from random import randint
        self.number = randint(1, 100)
        self.main()

    def getguess(self):
        while True:
            guess = input('Ur guess: ')
            if guess.isdigit():
                self.guess = int(guess)
                break
            else:
                print('Uncorrect!')

    def main(self):
        while True:
            self.getguess()
            if self.guess == self.number:
                print('U win!')
                break
            elif self.guess < self.number:
                print('Too little!')
            else:
                print('Too big!')

Game()
