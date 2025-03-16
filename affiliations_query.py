from BaseXClient import BaseXClient

import xml.etree.ElementTree as ET

def get_author_affiliations_iter(author_name):
    """Fetch unique affiliations for a given author and return them as a plain string list."""
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    affiliations = []
    
    try:
        session.execute("OPEN dblp")  # Open the correct DB
        
        query_text = f"""
        let $author_name := '{author_name}'
        for $aff in distinct-values(
          //(article|inproceedings|book|incollection|phdthesis|mastersthesis|proceedings|www|data)[author = $author_name]/note[@type='affiliation']/text()
        )
        return <affiliation>{{$aff}}</affiliation>
        """
        
        query = session.query(query_text)
        
        # Add detailed debugging
        for typecode, item in query.iter():
            try:
                elem = ET.fromstring(item)
                affiliations.append(elem.text.strip())                
            except ET.ParseError as e:
                print("Parse error:", e, "on item:", item)
        
        query.close()
        return affiliations
    finally:
        session.close()



if __name__ == "__main__":
    author = "Christian Bizer"

    print("\n--- Affiliations ---")
    affiliations_list = get_author_affiliations_iter(author)
    print(affiliations_list)
