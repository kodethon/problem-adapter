from bs4 import BeautifulSoup
import os

def parse(raw_path, topic, output_path):
    """
    Args:
        raw_path: path to raw html files
        topic: name of the topic
        output_path: name of the folder to store generated files
    """

    files_parsed = 0
    raw_topic_path = os.path.join(raw_path, topic)
    for subtopic in os.listdir(raw_topic_path):
        print(subtopic)
        for file in os.listdir(os.path.join(raw_topic_path, subtopic)):
            if not file.endswith('.html'):
                continue

            print(file)

            with open(os.path.join(raw_topic_path, subtopic, file)) as f:
                soup = BeautifulSoup(f, 'html.parser')

            for i in soup.findAll('pre'):
                if 'class' not in i.attrs: # Check if tag object contains class attribute
                    continue

                if 'python;' not in i['class'] and 'python3;' not in i['class']: # Check if class attribute has python string
                    continue

                problem = file.replace(".html", "") 
                new_folder = os.path.join(output_path, topic, subtopic, problem)
                if not os.path.exists(new_folder): # If folder for problem doesn't already exist
                    os.makedirs(new_folder) # creates parent directories if necessary

                new_file = os.path.join(new_folder, problem+".py")
                if os.path.isfile(new_file):
                    o = open(os.path.join(new_folder, problem+"2.py"), "w")
                else:
                    o = open(new_file, "w")

                o.write(i.string.encode("utf-8"))
                o.close()

                for tag in soup.findAll("div", class_="entry-content"):
                    for p in tag.findAll("p"):
                        text = ""
                        text += tag.text
                        text +="\n"
                        o = open(os.path.join(new_folder, "description.txt"), "w")
                        o.write(text.encode("utf-8"))
                        o.close()

                files_parsed += 1

    print(files_parsed)

parse('raw', 'strings', 'output')

