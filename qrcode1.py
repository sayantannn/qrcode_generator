# import nltk

# # Make sure you've downloaded the necessary nltk data files like 'punkt'
# nltk.download('punkt')  # Uncomment this if you haven't already downloaded it

# # Open the file using a correct file path and proper file handling
# with open(r"/Users/sayantanguha/Documents/qrcode/requirements.txt", "r", encoding="utf-8") as filename:
#     tokens = []  # Initialize an empty list to store tokens
    
#     # Read through the file line by line
#     for line in filename:
#         # Tokenize each line and extend the list with new tokens
#         tokens.extend(nltk.word_tokenize(line))

# # Join tokens into a single string with commas between tokens
# token_string = ",".join(tokens)

# print(token_string)