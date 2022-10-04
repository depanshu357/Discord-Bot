import random
R_Eating = "I don't like eating 'coz I am a bot!"
def unknown():
    response = ["Could you please rephrase that?",
                 "...",
                 "What do you mean?",
                 "Hmm"
                 ][random.randrange(4)]
    return response