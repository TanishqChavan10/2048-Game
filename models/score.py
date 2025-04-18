import os

class ScoreManager:
    def __init__(self):
        self.current_score = 0
        self.best_score = self.load_high_score()
    
    def update_score(self, score):
        """Update the current score"""
        self.current_score = score
        if self.current_score > self.best_score:
            self.best_score = self.current_score
            self.save_high_score(self.best_score)
    
    def reset_score(self):
        """Reset the current score"""
        self.current_score = 0
    
    def save_high_score(self, score):
        """Save high score to a file"""
        try:
            with open("high_score.txt", "w") as file:
                file.write(str(score))
        except:
            # If there's an error saving, just continue
            pass
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists("high_score.txt"):
                with open("high_score.txt", "r") as file:
                    return int(file.read().strip())
            return 0
        except:
            # If there's an error loading, return 0
            return 0 