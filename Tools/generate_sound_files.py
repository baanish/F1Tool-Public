# Import the required module for text
# to speech conversion
from distutils.command.build_scripts import first_line_re
from gtts import gTTS

# The text to convert to audio
outlap = 'You are on your outlap.'
outlap_audio = gTTS(text=outlap, lang='en', slow=False)
outlap_audio.save(".\\sounds\\outlap.mp3")

first_lap = 'You have started your first lap.'
first_lap_audio = gTTS(text=first_lap, lang='en', slow=False)
first_lap_audio.save(".\\sounds\\first_lap.mp3")

lap_completed = 'You have completed a lap.'
lap_completed_audio = gTTS(text=lap_completed, lang='en', slow=False)
lap_completed_audio.save(".\\sounds\\lap_completed.mp3")

calculating_averages = 'Completed last lap. Calculating averages.'
calculating_averages_audio = gTTS(text=calculating_averages, lang='en', slow=False)
calculating_averages_audio.save(".\\sounds\\calculating_averages.mp3")
