from xml.dom import minidom
import os

def xml2csv(nameXML,nameCSV):
    if not (isinstance(nameXML,str) and isinstance(nameCSV,str)):
        raise Exception('params must be a string')
    
    if not os.path.exists(nameXML):
        raise Exception('XML not found')
    
    doc = minidom.parse(nameXML)
    conversations = doc.getElementsByTagName('conversation')

    for conversation in conversations:
        if conversation.hasAttribute("id"):
            line_csv = ''
            conversation_id = conversation.getAttribute("id")
            line_csv+= str(conversation_id) + '|'
            messages = conversation.getElementsByTagName('message')
            author1=author2 = ''            
            for message in messages:                
                if author1 == '':
                    author1 = message.getElementsByTagName('author')[0].childNodes[0].data
                    line_csv+= str(author1) + '|'
                if author1 != message.getElementsByTagName('author')[0].childNodes[0].data:
                    if author2 == '':
                        author2 = message.getElementsByTagName('author')[0].childNodes[0].data
                        line_csv+= str(author2)
                        break
            print(line_csv)
            break
                





    return
