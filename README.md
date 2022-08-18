# F1Tool-Public
 A quick script I made for a tool to use with the F1-2021 game

# Why to use:
Use this in practice to figure out your strategy for the race, I usually do 2/3 laps with this running to get the data. You are limited by your skill to drive consistent laps and how far you can stretech your ERS without running out of battery for increasing your laps.

The included strategy.txt is from Austria in F1 22 where I was in the Ferrari, driving pretty aggresively, using a fair bit of ERS 

# Usage:
Open a terminal in the main directory
install the requirted packages: ```pip install -r .\requirements.txt```

Generate the audio files: ```python .\Tools\generate_sound_files.py```

run the program: ```python .\run_program.py```

UDP settings which I use: [Image](https://i.imgur.com/LcxEuwv.png)

### Generating test data
To generate the test data run test data tool: ```python \Tools\generate_test_data.py```

Go into GrandPrix Mode, go out on track for the number of laps needed. Try to drive as consistenly as possible (Flashbacks should not break anything).

### Running tests

To run the tests for speed run: ```python \test\test_quick.py```

(Note this causes errors with the audio functionality, for testing audio functionality run: ```python \test\test_slow.py```)

## V 1.1 Changes
* Added Audio prompts as the app runs in the background.
* Added a way to generate data for testing.
  * Data needs to be generated as it is too large to share easily. Approx 300mb per minute of gameplay
* Vastly improved performance.
  * Time taken to run the tests - 20.2 sec to 0.07 sec
