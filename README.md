# aiagent
With this project I am using the Google Gemini API to create an AI help Agent. I am writing functions to give it the ability to open / acquire info on files as well as write to those files. 

As an important safety feature, I am limiting its access to files outside of my defined working directory. 

The program will accept command line arguments from the user and call the Gemini API with those arguments as the prompt. The user will also have the option to set a "--verbose" flag after their provided arguments to print the prompt and response tokens. I have also provided specific prompts in the prompts.py file to direct the Agent how to use the provided functions to solve user questions without additional prompts.
