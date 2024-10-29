import re

# Exemple de texte HTML pour la démonstration
input_html = '''
<strong>Listed on: </strong><span style="direction: ltr; unicode-bidi: embed">23 Feb. 2001</span>
                                                                (
                                                                amended on <span style="direction: ltr; unicode-bidi: embed">3 Sep. 2003, </span><span style="direction: ltr; unicode-bidi: embed">9 Jul. 2007, </span><span style="direction: ltr; unicode-bidi: embed">21 Sep. 2007, </span><span style="direction: ltr; unicode-bidi: embed">29 Nov. 2011</span>
                                                                )
                                                        <strong>Other information: </strong>
'''

# Modèle de l'expression régulière pour trouver "Listed on: " suivi de tout le reste
listed_on_pattern = re.compile(r'Listed on: .+', re.DOTALL)

# Recherche dans le texte avec l'expression régulière
listed_on_match = re.findall(listed_on_pattern, input_html)

if listed_on_match:
  
    
    # Appliquer les remplacements sur le texte extrait
    cleaned_listed_on = listed_on_match[0].replace('\n','').replace('<span style=\"direction: ltr; unicode-bidi: embed\">','').replace('</span>','').replace('</strong>','')
    
    print(f"Listed on: {cleaned_listed_on}")
else:
    print("Pas de correspondance trouvée.")
