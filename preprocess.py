import re

class preprocess():
    
    def totalPreprocess(self, text):

        # Remove all emojis
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        # Remove all links
        text = re.sub(r'http\S+', '', text)
        
        return text
    
if __name__ == "__main__":
    text = input("Enter text: ") 
    tp = preprocess() 
    print(tp.totalPreprocess(text))
