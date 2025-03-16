from BaseXClient import BaseXClient
import xml.etree.ElementTree as ET

def get_author_publications_iter(author_name):
    """Fetch and parse publications for a given author into structured dicts."""
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    publications = []  # List to collect parsed publication dicts
    
    try:
        session.execute("OPEN dblp")  # Open the correct DB

        # Query to fetch publications of the author
        query_text = f"""
        let $author_name := '{author_name}'
        for $pub in //(article|inproceedings|book|incollection|phdthesis|mastersthesis|proceedings|www|data)
        where $pub/author = $author_name
        return $pub
        """

        query = session.query(query_text)

        # Iterate over results
        for typecode, item in query.iter():
            try:
                elem = ET.fromstring(item)  # Parse XML
                pub_dict = {
                    "type": elem.tag,
                    "key": elem.attrib.get("key"),
                    "mdate": elem.attrib.get("mdate"),
                    "publtype": elem.attrib.get("publtype"),
                    "authors": [],
                    "title": None,
                    "year": None,
                    "venue": None,
                    "ee": None,
                    "url": None
                }

                for child in elem:
                    if child.tag == "author":
                        pub_dict["authors"].append(child.text.strip())
                    elif child.tag == "title":
                        pub_dict["title"] = child.text.strip()
                    elif child.tag == "year":
                        pub_dict["year"] = child.text.strip()
                    elif child.tag == "journal":
                        pub_dict["venue"] = child.text.strip()
                    elif child.tag == "booktitle":
                        pub_dict["venue"] = child.text.strip()  # conference
                    elif child.tag == "ee":
                        pub_dict["ee"] = {
                            "type": child.attrib.get("type"),
                            "link": child.text.strip()
                        }
                    elif child.tag == "url":
                        pub_dict["url"] = child.text.strip()

                publications.append(pub_dict)  # Add parsed publication to the list

            except ET.ParseError as e:
                print("Parse error:", e, "on item:", item)

        query.close()
        return publications  # Return list of publication dicts
    finally:
        session.close()


if __name__ == "__main__":
    author = "Rainer Gemulla"
    publications = get_author_publications_iter(author)
    
    print("\n--- Publications ---")
    for pub in publications:
        print(pub['title'])
        break 
